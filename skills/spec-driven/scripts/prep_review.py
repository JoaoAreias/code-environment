#!/usr/bin/env python3
"""
prep_review.py - deterministic preparation for a Spec Review or a Change Review.

Every precondition the review skills promise runs here, in code, so neither the
human-facing skill nor the reviewer agent has to remember it. On success it
prints a "Review context" block that the trigger pastes, verbatim, into the
reviewer's prompt. On a failed precondition it prints why and exits 1: the
trigger shows that to the human and stops. Missing evidence never degrades
silently.

Usage:
  python3 <skill-dir>/scripts/prep_review.py spec   [feature | path] [--root DIR]
  python3 <skill-dir>/scripts/prep_review.py change [feature] [--root DIR]
          [--base REF] [--no-spec] [--unverified]

spec:   requires tasks.md at every scope and design.md at Medium, Large or Complex;
        commits the plan (.specs/features/<feature>/ plus .specs/decisions/,
        .specs/STATE.md, the lessons store, CONTEXT-MAP.md and every CONTEXT.md)
        so a reviewer's stray edit can always be undone, refusing when other
        uncommitted changes exist.
        A path to a file or folder outside .specs/features/ is a foreign plan
        (a folder is one plan made of every *.md in it): it is never written or
        committed, the validators are skipped, and the report goes to
        .specs/reviews/<slug of the path>/spec-review-<n>.md.
change: requires a clean tree, a non-empty Change, a Spec (unless --no-spec), and
        a PASS validation.md (unless --unverified). A FAIL verdict always stops.
Both:   refresh the graphify graph (graphify-out/ is kept out of git through
        .git/info/exclude) and pick the next run number for the report file.

Exit codes: 0 ready, 1 precondition failed (message says what to do), 2 usage error.
"""

import argparse
import datetime as _dt
import glob
import hashlib
import os
import re
import shutil
import subprocess
import sys

from scenarios_lib import find_tables, git, spec_is_native, spec_scope

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
STANDARD_SOURCES = [
    "AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md", "CODING_STANDARDS.md", "STYLEGUIDE.md",
    "docs/CONTRIBUTING.md", ".editorconfig", ".github/copilot-instructions.md",
]
STANDARD_GLOBS = ["docs/**/*standard*.md", "docs/**/*style*.md", "docs/**/*convention*.md",
                  "docs/**/*guideline*.md", ".cursor/rules/*", ".claude/rules/*"]
# Shared planning files the pre-review commit protects next to the feature folder.
# Every file named CONTEXT.md is protected too (see in_plan).
SHARED_PLAN_PATHS = [".specs/decisions/", ".specs/STATE.md", ".specs/LESSONS.md", ".specs/lessons.json", "CONTEXT-MAP.md"]
LINT_CONFIGS = [".eslintrc*", "eslint.config.*", "biome.json*", "ruff.toml", ".ruff.toml", "pyproject.toml",
                ".golangci.y*ml", ".rubocop.yml", "detekt.yml", ".pre-commit-config.yaml", "tsconfig.json"]


class Stop(Exception):
    pass


def run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def must_git(root, *args):
    rc, out, err = git(root, *args)
    if rc != 0:
        raise Stop(f"`git {' '.join(args)}` failed:\n{err or out}")
    return out.strip()


def features_dir(root):
    return os.path.join(root, ".specs", "features")


def list_features(root):
    base = features_dir(root)
    if not os.path.isdir(base):
        return []
    return [d for d in sorted(os.listdir(base)) if os.path.isdir(os.path.join(base, d))]


def dirty_paths(root):
    rc, out, err = git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    if rc != 0:
        raise Stop(f"`git status` failed:\n{err}")
    entries = out.split("\0")
    paths, i = [], 0
    while i < len(entries):
        e = entries[i]
        i += 1
        if len(e) < 4:
            continue
        paths.append(e[3:])
        if e[0] in "RC":
            i += 1  # skip the rename/copy source path
    return paths


def next_run(fdir, prefix):
    nums = [int(m.group(1)) for f in os.listdir(fdir) for m in [re.match(prefix + r"-(\d+)\.md$", f)] if m] if os.path.isdir(fdir) else []
    n = max(nums) + 1 if nums else 1
    prev = os.path.join(fdir, f"{prefix}-{n - 1}.md") if nums else None
    return n, os.path.join(fdir, f"{prefix}-{n}.md"), prev


def disposition_status(path):
    """Return (findings, undisposed IDs) for a review file."""
    if not path or not os.path.isfile(path):
        return 0, []
    text = open(path, encoding="utf-8", errors="replace").read()
    ids = re.findall(r"^#{2,4}\s+((?:SR|CR)\d+-F\d+)\b", text, re.MULTILINE)
    open_ids = []
    blocks = re.split(r"^(?=#{2,4}\s+(?:SR|CR)\d+-F\d+\b)", text, flags=re.MULTILINE)
    for b in blocks:
        m = re.match(r"^#{2,4}\s+((?:SR|CR)\d+-F\d+)\b", b)
        if not m:
            continue
        d = re.search(r"\*\*Disposition\*\*\s*:\s*(.*)", b)
        val = (d.group(1).strip().lower() if d else "")
        if not (val.startswith("accept") or val.startswith("reject")):
            open_ids.append(m.group(1))
    return len(ids), open_ids


def latest(fdir, prefix):
    if not os.path.isdir(fdir):
        return None
    nums = sorted(int(m.group(1)) for f in os.listdir(fdir) for m in [re.match(prefix + r"-(\d+)\.md$", f)] if m)
    return os.path.join(fdir, f"{prefix}-{nums[-1]}.md") if nums else None


def ensure_graphify(root):
    """Fail early when graphify is missing; keep graphify-out/ out of git without touching .gitignore."""
    exe = shutil.which("graphify")
    if not exe:
        raise Stop("graphify is not installed, so duplicate detection has no evidence.\n"
                   "Install it with `uv tool install graphifyy` (or re-run code-environment's install.sh), then retry.")
    exclude = os.path.join(must_git(root, "rev-parse", "--absolute-git-dir"), "info", "exclude")
    os.makedirs(os.path.dirname(exclude), exist_ok=True)
    current = open(exclude, encoding="utf-8").read() if os.path.exists(exclude) else ""
    if "graphify-out/" not in current.split():
        with open(exclude, "a", encoding="utf-8") as f:
            f.write(("" if current.endswith("\n") or not current else "\n") + "graphify-out/\n")
    return exe


def refresh_graph(root):
    exe = ensure_graphify(root)
    rc, out, err = run([exe, "update", "."], root)
    if rc != 0:
        raise Stop(f"`graphify update .` failed:\n{err or out}")
    stats = re.search(r"(\d+ nodes, \d+ edges)", out + err)
    return f"`graphify-out/graph.json` refreshed {_dt.datetime.now().strftime('%Y-%m-%d %H:%M')}" + (f" ({stats.group(1)})" if stats else "")


def standard_sources(root):
    found = [p for p in STANDARD_SOURCES if os.path.isfile(os.path.join(root, p))]
    for g in STANDARD_GLOBS:
        found += [os.path.relpath(p, root) for p in glob.glob(os.path.join(root, g), recursive=True) if os.path.isfile(p)]
    lint = [os.path.relpath(p, root) for g in LINT_CONFIGS for p in glob.glob(os.path.join(root, g))]
    return sorted(set(found)), sorted(set(lint))


def reviewer_lessons(root):
    if not os.path.isfile(os.path.join(root, ".specs", "lessons.json")):
        return "(no lessons store)"
    rc, out, err = run([sys.executable, os.path.join(HERE, "lessons.py"), "--root", root, "list",
                        "--status", "confirmed", "--audience", "reviewer"], root)
    return out or err


def script_summary(root, *args, keep=25):
    r = subprocess.run([sys.executable, *args], cwd=root, capture_output=True, text=True)
    rc, lines = r.returncode, (r.stdout + r.stderr).splitlines()
    body = [ln for ln in lines if ln.strip()]
    if len(body) > keep:
        body = body[:keep] + [f"... ({len(lines) - keep} more lines; re-run the command for the full list)"]
    return rc, "\n".join(body)


def in_plan(path, plan):
    return os.path.basename(path) == "CONTEXT.md" or any(path == x or path.startswith(x) for x in plan)


def feature_records(root, feature):
    """Repo-relative paths of the Grilling Records whose summary.md row names `feature` in its Specs cell."""
    path = os.path.join(root, ".specs", "decisions", "summary.md")
    if not os.path.isfile(path):
        return []
    records = []
    for table in find_tables(open(path, encoding="utf-8", errors="replace").read().splitlines(), "File", "Specs"):
        for row in table:
            if feature not in re.findall(r"[\w.-]+", row.get("specs", "")):
                continue
            link = re.search(r"\]\(([^)]+)\)", row.get("file", ""))
            name = link.group(1) if link else row.get("file", "").strip("` ")
            records.append(os.path.normpath(os.path.join(".specs", "decisions", name)))
    return records


def pick_feature(root, feature, changed=None):
    feats = list_features(root)
    if feature:
        if feature not in feats:
            raise Stop(f"no feature `{feature}` under .specs/features/ (have: {', '.join(feats) or 'none'})")
        return feature
    if changed is not None:
        touched = sorted({p.split("/")[2] for p in changed if p.startswith(".specs/features/") and p.count("/") >= 3})
        if len(touched) == 1:
            return touched[0]
        if len(touched) > 1:
            raise Stop(f"the Change touches several features ({', '.join(touched)}); pass one explicitly")
        return None
    dirty = sorted({p.split("/")[2] for p in dirty_paths(root) if p.startswith(".specs/features/") and p.count("/") >= 3})
    if len(dirty) == 1:
        return dirty[0]
    if len(feats) == 1:
        return feats[0]
    raise Stop("cannot tell which feature to review; pass its name "
               f"(features: {', '.join(feats) or 'none'})")


def header(lines, title, root):
    lines.append(f"## Review context ({title})")
    lines.append("")
    lines.append(f"- Repository: `{root}`")
    lines.append(f"- spec-driven skill: `{SKILL_DIR}` (scripts in `scripts/`, references in `references/`)")


def feature_in_path(root, target):
    """Feature name for a path inside .specs/features/<f>/ (the folder or any file in it), else None."""
    if not target:
        return None
    for path in (os.path.realpath(target), os.path.realpath(os.path.join(root, target))):
        parts = os.path.relpath(path, os.path.realpath(features_dir(root))).split(os.sep)
        if parts[0] not in (".", "..") and os.path.exists(path):
            return parts[0]
    return None


def foreign_plan(root, target):
    """Repo-relative path of a foreign plan: `target` names a file or folder outside .specs/features/.

    Returns None when `target` is empty or names a feature (by name or by a path inside its folder).
    """
    if not target or target in list_features(root) or feature_in_path(root, target):
        return None
    path = next((p for p in (os.path.realpath(target), os.path.realpath(os.path.join(root, target))) if os.path.exists(p)), None)
    if path is None:
        raise Stop(f"no feature `{target}` under .specs/features/ and no file or folder at that path "
                   f"(features: {', '.join(list_features(root)) or 'none'})")
    rel = os.path.relpath(path, os.path.realpath(root))
    parts = rel.split(os.sep)
    if rel == "." or parts[0] == "..":
        raise Stop(f"`{target}` is not a plan inside this repository; pass a feature name or the path of a plan file or folder")
    if parts[:2] == [".specs", "features"] and len(parts) > 2:
        return None
    return rel.replace(os.sep, "/")


def snapshot(root, plan, name):
    """Commit the uncommitted plan paths so a stray edit can be undone; return the Reviewed commit line."""
    dirty = dirty_paths(root)
    outside = [p for p in dirty if not in_plan(p, plan)]
    if outside:
        raise Stop("uncommitted changes outside the plan would not be protected by the pre-review commit:\n  "
                   + "\n  ".join(outside[:20]) + "\nCommit or stash them, then retry.")
    if dirty:
        must_git(root, "add", "--", *dirty)
        msg = f"docs(spec): snapshot {name} before spec review"
        rc, out, err = git(root, "commit", "-m", msg)
        if rc != 0:
            raise Stop(f"pre-review commit failed (hooks?):\n{err or out}")
        snap = "plan committed by prep (`" + msg + "`)"
    else:
        snap = "plan already committed"
    return f"- Reviewed commit: `{must_git(root, 'rev-parse', '--short', 'HEAD')}` ({snap})"


def feature_target(root, feature):
    """Return (name, report dir, intro lines, decision lines, structural check lines) for a feature's plan."""
    fdir = os.path.join(features_dir(root), feature)
    rel = os.path.relpath(fdir, root)
    if not os.path.isfile(os.path.join(fdir, "spec.md")):
        raise Stop(f"{rel}/spec.md does not exist; finish Specify first")
    spec_text = open(os.path.join(fdir, "spec.md"), encoding="utf-8").read()
    scope = spec_scope(spec_text) or "unknown"
    if not os.path.isfile(os.path.join(fdir, "tasks.md")):
        raise Stop(f"{rel}/tasks.md does not exist; every feature needs Tasks and Tickets before a Spec Review. Run the Tasks phase first")
    if scope in ("Medium", "Large", "Complex") and not os.path.isfile(os.path.join(fdir, "design.md")):
        raise Stop(f"{rel}/design.md does not exist; a {scope} feature needs a Design before a Spec Review. Run the Design phase first")
    present = [f for f in ("spec.md", "design.md", "tasks.md") if os.path.isfile(os.path.join(fdir, f))]
    intro = [f"- Feature: `{feature}` · scope: {scope}",
             f"- Plan files: {', '.join('`' + rel + '/' + f + '`' for f in present)}"]
    records = feature_records(root, feature)
    decisions = ["- Grilling Records: " + (", ".join(f"`{r}`" for r in records)
                                           or "none named for this feature in `.specs/decisions/summary.md`")]
    if os.path.isfile(os.path.join(fdir, "context.md")):
        decisions.append(f"- Legacy decision source: `{rel}/context.md`")
    if not spec_is_native(spec_text):
        decisions.append("- Decisions log: `.specs/STATE.md`" if os.path.isfile(os.path.join(root, ".specs", "STATE.md")) else "- Decisions log: none")
    checks = []
    for script in ("validate_spec.py", "validate_tasks.py"):
        rc, text = script_summary(root, os.path.join(HERE, script), feature, "--root", root)
        checks += [f"`{script}` exit {rc}:", "```", text, "```"]
    return feature, fdir, intro, decisions, checks


def report_slug(root, rel, slug):
    """Report folder slug for a foreign plan. Each folder records its plan in `source.txt`; when the folder
    already belongs to a different plan path, append a short hash of `rel` so two plans never share history.
    Writes `source.txt` for the folder it returns when the file is missing."""
    def owner(name):
        src = os.path.join(root, ".specs", "reviews", name, "source.txt")
        return open(src, encoding="utf-8").read().strip() if os.path.isfile(src) else None
    taken = owner(slug)
    if taken is not None and taken != rel:
        slug = f"{slug}-{hashlib.sha1(rel.encode('utf-8')).hexdigest()[:8]}"
    if owner(slug) is None:
        folder = os.path.join(root, ".specs", "reviews", slug)
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, "source.txt"), "w", encoding="utf-8") as f:
            f.write(rel + "\n")
    return slug


def foreign_target(root, rel):
    """Return the same tuple as feature_target for a foreign plan. The plan is only read, never written or committed."""
    path = os.path.join(root, rel)
    if os.path.isdir(path):
        files = sorted(os.path.relpath(p, root).replace(os.sep, "/")
                       for p in glob.glob(os.path.join(glob.escape(path), "**", "*.md"), recursive=True) if os.path.isfile(p))
        if not files:
            raise Stop(f"`{rel}` holds no markdown files, so there is no plan to review")
        stem = rel
    else:
        files, stem = [rel], os.path.splitext(rel)[0]
    dirty = [p for p in dirty_paths(root) if p in files]
    if dirty:
        raise Stop("the foreign plan has uncommitted changes, and prep never commits a plan it does not own:\n  "
                   + "\n  ".join(dirty) + "\nCommit or stash them, then retry.")
    slug = report_slug(root, rel, re.sub(r"[^A-Za-z0-9]+", "-", stem).strip("-"))
    intro = [f"- Plan: `{rel}` · foreign (not written by spec-driven): review it as it is and never edit it",
             f"- Plan files: {', '.join('`' + f + '`' for f in files)}"]
    checks = ["Skipped: the plan is foreign (not written by spec-driven), so `validate_spec.py` and `validate_tasks.py`, "
              "which check spec-driven's own file format, do not apply."]
    return slug, os.path.join(root, ".specs", "reviews", slug), intro, [], checks


def prep_spec(args, root):
    foreign = foreign_plan(root, args.feature)
    name, rdir, intro, decisions, checks = (foreign_target(root, foreign) if foreign
                                            else feature_target(root, pick_feature(root, feature_in_path(root, args.feature) or args.feature)))
    reviewed = snapshot(root, [os.path.relpath(rdir, root) + "/", *SHARED_PLAN_PATHS], name)
    graph = refresh_graph(root)
    n, report, prev = next_run(rdir, "spec-review")
    standards, lint = standard_sources(root)

    out = []
    header(out, "Spec Review", root)
    out += [
        *intro,
        reviewed,
        f"- Run: SR{n} · write the report to `{os.path.relpath(report, root)}` · Finding IDs `SR{n}-F1`, `SR{n}-F2`, ...",
        f"- Previous run: `{os.path.relpath(prev, root)}`" if prev else "- Previous run: none",
        *decisions,
        f"- Repo Standard sources: {', '.join('`' + s + '`' for s in standards) or 'none found'}",
        f"- Lint/format configs: {', '.join('`' + s + '`' for s in lint) or 'none found'}",
        f"- Graph: {graph}",
        "",
        "### Reviewer Lessons (confirmed)",
        "",
        reviewer_lessons(root),
        "",
        "### Structural checks",
        "",
        *checks,
    ]
    return "\n".join(out)


def resolve_base(root, base):
    if base:
        return must_git(root, "rev-parse", "--verify", base + "^{commit}"), base
    for ref in ("origin/HEAD", "origin/main", "origin/master", "main", "master"):
        rc, out, _ = git(root, "rev-parse", "--verify", "--quiet", ref + "^{commit}")
        if rc == 0:
            rc, mb, _ = git(root, "merge-base", "HEAD", ref)
            if rc == 0 and mb.strip():
                return mb.strip(), f"merge-base with {ref}"
    raise Stop("cannot find a base for the Change; pass --base <ref>")


def prep_change(args, root):
    if dirty_paths(root):
        raise Stop("the working tree has uncommitted changes. A Change Review reads committed history only;\n"
                   "commit (or stash) them, then retry. Recovery from a reviewer's stray edit relies on a clean start.")
    base_sha, base_label = resolve_base(root, args.base)
    head = must_git(root, "rev-parse", "HEAD")
    if base_sha == head:
        raise Stop(f"the Change is empty: HEAD equals the base ({base_label})")
    changed = [p for p in must_git(root, "diff", "--name-only", "--no-ext-diff", f"{base_sha}...HEAD").splitlines() if p]
    if not changed:
        raise Stop(f"the Change is empty against {base_label}")

    feature, fdir = None, None
    if not args.no_spec:
        feature = pick_feature(root, args.feature, changed=changed)
        if not feature:
            raise Stop("no feature Spec found for this Change (no `.specs/features/<feature>/` touched).\n"
                       "Pass the feature name, or re-run with `--no-spec`: Spec-dependent checks are then marked "
                       "\"not assessable\" and the PR description and commits serve as Claims.")
        fdir = os.path.join(features_dir(root), feature)
        if not os.path.isfile(os.path.join(fdir, "spec.md")):
            raise Stop(f".specs/features/{feature}/spec.md does not exist; pass the right feature or use --no-spec")

    verifier = "not applicable (--no-spec)"
    if fdir:
        vpath = os.path.join(fdir, "validation.md")
        if not os.path.isfile(vpath):
            if not args.unverified:
                raise Stop("no validation.md: the Verifier never ran for this feature. Choose one:\n"
                           "  1. run the Verifier first (spec-driven Execute step 9), then retry; or\n"
                           "  2. re-run with `--unverified`: Functional Correctness and Verification are marked \"unverified\".")
            verifier = "MISSING - reviewing with --unverified: mark Functional Correctness and Verification \"unverified\""
        else:
            sys.path.insert(0, HERE)
            from validate_state import _verdict  # noqa: E402
            v = _verdict(open(vpath, encoding="utf-8", errors="replace").read())
            if v == "fail":
                raise Stop("validation.md says FAIL. Fix the Verifier's ranked gaps first; reviewing a Change known to be broken wastes the review.")
            if v != "pass":
                raise Stop("validation.md has no filled PASS verdict; complete the Verifier run first (or use --unverified).")
            verifier = f"PASS (`{os.path.relpath(vpath, root)}`)"

    graph = refresh_graph(root)
    if fdir:
        rdir = fdir
    else:
        branch = re.sub(r"[^A-Za-z0-9._-]+", "-", must_git(root, "rev-parse", "--abbrev-ref", "HEAD")) or "detached"
        rdir = os.path.join(must_git(root, "rev-parse", "--absolute-git-dir"), "spec-driven", "reviews", branch)
        os.makedirs(rdir, exist_ok=True)
    n, report, prev = next_run(rdir, "change-review")
    standards, lint = standard_sources(root)
    commits = must_git(root, "log", "--oneline", "--no-decorate", f"{base_sha}..HEAD")
    stat = must_git(root, "diff", "--shortstat", f"{base_sha}...HEAD")

    out = []
    header(out, "Change Review", root)
    out += [
        f"- Feature: `{feature}` (`.specs/features/{feature}/`)" if feature else "- Feature: none (`--no-spec`): Spec-dependent checks are \"not assessable\"; use the PR description and commit messages as Claims",
        f"- Base: `{base_sha[:12]}` ({base_label}) · Head: `{head[:12]}` · {stat}",
        f"- Diff: `git diff {base_sha[:12]}...HEAD`",
        f"- Verifier: {verifier}",
    ]
    if fdir:
        sr = latest(fdir, "spec-review")
        if not sr:
            out.append("- Spec Review: NONE ran for this feature - flag it under Truthful Reporting; it does not block")
        else:
            total, open_ids = disposition_status(sr)
            out.append(f"- Spec Review: `{os.path.relpath(sr, root)}` · {total} Finding(s)"
                       + (f" · WITHOUT Disposition: {', '.join(open_ids)} (flag it)" if open_ids else " · all have Dispositions"))
    out += [
        f"- Run: CR{n} · write the report to `{report if not fdir else os.path.relpath(report, root)}` · Finding IDs `CR{n}-F1`, ...",
        f"- Previous run: `{prev if not fdir else os.path.relpath(prev, root)}`" if prev else "- Previous run: none",
        f"- Repo Standard sources: {', '.join('`' + s + '`' for s in standards) or 'none found'}",
        f"- Lint/format configs: {', '.join('`' + s + '`' for s in lint) or 'none found'}",
        f"- Graph: {graph}",
        "",
        "### Commits",
        "",
        "```",
        commits,
        "```",
        "",
        "### Reviewer Lessons (confirmed)",
        "",
        reviewer_lessons(root),
    ]
    if feature:
        rc, text = script_summary(root, os.path.join(HERE, "validate_scenarios.py"), feature, "--root", root, "--since", base_sha)
        out += ["", "### Scenario check", "", f"`validate_scenarios.py {feature} --since {base_sha[:12]}` exit {rc}:", "```", text, "```"]
    return "\n".join(out)


def main(argv=None):
    p = argparse.ArgumentParser(prog="prep_review.py", description="Preconditions and context for a review run.")
    p.add_argument("mode", choices=["spec", "change"])
    p.add_argument("feature", nargs="?", default=None)
    p.add_argument("--root", default=".")
    p.add_argument("--base", default=None)
    p.add_argument("--no-spec", action="store_true")
    p.add_argument("--unverified", action="store_true")
    args = p.parse_args(argv)
    root = os.path.abspath(args.root)
    rc, top, _ = git(root, "rev-parse", "--show-toplevel")
    if rc != 0:
        print("STOP: not inside a git repository.", file=sys.stderr)
        return 1
    root = top.strip()
    try:
        ensure_graphify(root)
        text = prep_spec(args, root) if args.mode == "spec" else prep_change(args, root)
    except Stop as e:
        print(f"STOP: {e}")
        return 1
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
