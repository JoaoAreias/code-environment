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
  python3 <skill-dir>/scripts/prep_review.py spec   [feature] [--root DIR]
  python3 <skill-dir>/scripts/prep_review.py change [feature] [--root DIR]
          [--base REF] [--no-spec] [--unverified]

spec:   commits the plan (.specs/features/<feature>/ plus .specs/STATE.md and the
        lessons store) so a reviewer's stray edit can always be undone, refusing
        when other uncommitted changes exist.
change: requires a clean tree, a non-empty Change, a Spec (unless --no-spec), and
        a PASS validation.md (unless --unverified). A FAIL verdict always stops.
Both:   refresh the graphify graph (graphify-out/ is kept out of git through
        .git/info/exclude) and pick the next run number for the report file.

Exit codes: 0 ready, 1 precondition failed (message says what to do), 2 usage error.
"""

import argparse
import datetime as _dt
import glob
import os
import re
import shutil
import subprocess
import sys

from scenarios_lib import git, spec_scope

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
STANDARD_SOURCES = [
    "AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md", "CODING_STANDARDS.md", "STYLEGUIDE.md",
    "docs/CONTRIBUTING.md", ".editorconfig", ".github/copilot-instructions.md",
]
STANDARD_GLOBS = ["docs/**/*standard*.md", "docs/**/*style*.md", "docs/**/*convention*.md",
                  "docs/**/*guideline*.md", ".cursor/rules/*", ".claude/rules/*"]
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


def prep_spec(args, root):
    feature = pick_feature(root, args.feature)
    fdir = os.path.join(features_dir(root), feature)
    rel = os.path.relpath(fdir, root)
    if not os.path.isfile(os.path.join(fdir, "spec.md")):
        raise Stop(f"{rel}/spec.md does not exist; finish Specify first")
    plan = [rel + "/", ".specs/STATE.md", ".specs/LESSONS.md", ".specs/lessons.json"]
    outside = [p for p in dirty_paths(root) if not any(p == x or p.startswith(x) for x in plan)]
    if outside:
        raise Stop("uncommitted changes outside the plan would not be protected by the pre-review commit:\n  "
                   + "\n  ".join(outside[:20]) + "\nCommit or stash them, then retry.")
    inside = [p for p in dirty_paths(root)]
    if inside:
        existing = [p for p in plan if os.path.exists(os.path.join(root, p.rstrip("/")))]
        must_git(root, "add", "--", *existing)
        msg = f"docs(spec): snapshot {feature} before spec review"
        rc, out, err = git(root, "commit", "-m", msg)
        if rc != 0:
            raise Stop(f"pre-review commit failed (hooks?):\n{err or out}")
        snap = "plan committed by prep (`" + msg + "`)"
    else:
        snap = "plan already committed"
    sha = must_git(root, "rev-parse", "--short", "HEAD")
    graph = refresh_graph(root)
    n, report, prev = next_run(fdir, "spec-review")
    standards, lint = standard_sources(root)
    present = [f for f in ("spec.md", "context.md", "design.md", "tasks.md") if os.path.isfile(os.path.join(fdir, f))]
    scope = spec_scope(open(os.path.join(fdir, "spec.md"), encoding="utf-8").read()) or "unknown"

    out = []
    header(out, "Spec Review", root)
    out += [
        f"- Feature: `{feature}` · scope: {scope}",
        f"- Plan files: {', '.join('`' + rel + '/' + f + '`' for f in present)}",
        f"- Reviewed commit: `{sha}` ({snap})",
        f"- Run: SR{n} · write the report to `{os.path.relpath(report, root)}` · Finding IDs `SR{n}-F1`, `SR{n}-F2`, ...",
        f"- Previous run: `{os.path.relpath(prev, root)}`" if prev else "- Previous run: none",
        "- Decisions log: `.specs/STATE.md`" if os.path.isfile(os.path.join(root, ".specs", "STATE.md")) else "- Decisions log: none",
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
    ]
    for script, target in (("validate_spec.py", feature), ("validate_tasks.py", feature)):
        if script == "validate_tasks.py" and "tasks.md" not in present:
            continue
        rc, text = script_summary(root, os.path.join(HERE, script), target, "--root", root)
        out += [f"`{script}` exit {rc}:", "```", text, "```"]
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
