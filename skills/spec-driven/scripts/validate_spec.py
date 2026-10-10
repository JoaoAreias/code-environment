#!/usr/bin/env python3
"""
validate_spec.py - deterministic closure-gate checks for a feature spec.md.

Turns the Requirement Closure Gate (Specify phase) into a checkable pass/fail
run BEFORE a spec is presented for confirmation, instead of trusting the model
to remember the checks. Pure standard library, zero dependencies. Operates only
on the spec.md markdown artifact - never on the target codebase - so it stays
stack-agnostic and tool-agnostic.

What it checks (heuristic markdown inspection, not a full parser):
  ERROR  - a required section is missing (Small scope has a shorter list)
  ERROR  - `Existing Capabilities` or `Standards` is empty or still a placeholder
  ERROR  - an acceptance criterion has no requirement ID or no SHALL (not EARS-shaped)
  ERROR  - an acceptance criterion has no Scenario, or a Scenario lacks Given/When/Then,
           sits under the wrong criterion, or reuses an ID
  ERROR  - an Assumptions row has an empty "Chosen default" or "Rationale" cell
  ERROR  - a Requirement Traceability row has a malformed ID, or a criterion ID is missing from it
  WARN   - no `**Scope**:` line (Medium+ rules applied)
  WARN   - an AC has SHALL but no recognizable EARS lead keyword
  WARN   - template placeholder rows are still present (spec not filled in)
  WARN   - open questions are not explicitly resolved

Usage:
  python3 <skill-dir>/scripts/validate_spec.py [target] [--root DIR] [--strict]

  Invoke from the skill directory that ships this script (not the project root).
  target    Path to a spec.md, a feature directory, or a project root.
            Omitted -> auto-detect the single feature under <root>/.specs/features/.
  --root    Project root that contains .specs/ (default: current dir).
  --strict  Treat warnings as errors.

Exit codes: 0 pass, 1 errors found (or warnings under --strict), 2 usage error.
"""

import argparse
import os
import re
import sys

from scenarios_lib import parse_spec, spec_scope

REQUIRED_SECTIONS = [
    "Problem Statement",
    "Existing Capabilities",
    "Standards",
    "Out of Scope",
    "Assumptions & Open Questions",
    "User Stories",
    "Requirement Traceability",
]
REQUIRED_SECTIONS_SMALL = [
    "Problem Statement",
    "Existing Capabilities",
    "Standards",
    "Acceptance Criteria",
    "Steps",
]

ID_RE = re.compile(r"^[A-Z][A-Z0-9]*-\d+$")
PLACEHOLDER_RE = re.compile(r"^\s*\[.+\]\s*$")
STATUS_VALUES = {"pending", "in design", "in tasks", "implementing", "verified"}


def resolve_spec(target, root):
    """Return the path to a spec.md from a file, dir, or auto-detect."""
    if target:
        if os.path.isfile(target):
            return target
        if os.path.isdir(target):
            cand = os.path.join(target, "spec.md")
            if os.path.isfile(cand):
                return cand
            # maybe it's a project root
            return _autodetect(target)
        # Not a path: treat as a feature name under <root>/.specs/features/<name>/
        cand = os.path.join(root, ".specs", "features", target, "spec.md")
        if os.path.isfile(cand):
            return cand
        return None
    return _autodetect(root)


def _autodetect(root):
    base = os.path.join(root, ".specs", "features")
    if not os.path.isdir(base):
        return None
    features = [
        d for d in sorted(os.listdir(base))
        if os.path.isfile(os.path.join(base, d, "spec.md"))
    ]
    if len(features) == 1:
        return os.path.join(base, features[0], "spec.md")
    if len(features) == 0:
        return None
    # Ambiguous: signal the caller with the list.
    raise SystemExit(
        "validate_spec: multiple features found; pass one explicitly:\n  "
        + "\n  ".join(os.path.join(base, f, "spec.md") for f in features)
    )


def split_row(line):
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def is_separator(line):
    return bool(re.match(r"^\s*\|?[\s:|-]+\|?\s*$", line)) and "-" in line


def section_bounds(lines, name):
    """Return (start, end) line indices for a `## name` section body."""
    start = None
    for i, ln in enumerate(lines):
        if re.match(r"^#{1,3}\s+" + re.escape(name) + r"\s*$", ln.strip()):
            start = i + 1
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start, len(lines)):
        if re.match(r"^#{1,3}\s+\S", lines[j]):
            end = j
            break
    return (start, end)


def classify_ears(text):
    """Return (ok, note). ok requires a SHALL; note records the EARS pattern."""
    t = text.strip()
    low = t.lower()
    has_shall = bool(re.search(r"\bshall\b", low))
    if not has_shall:
        return (False, "no SHALL")
    kws = []
    if re.search(r"\bwhile\b", low):
        kws.append("WHILE")
    if re.search(r"\bwhen\b", low):
        kws.append("WHEN")
    if re.match(r"^\s*if\b", low) or re.search(r"\bif\b.*\bthen\b", low):
        kws.append("IF/THEN")
    if re.search(r"\bwhere\b", low):
        kws.append("WHERE")
    if len(kws) >= 2:
        return (True, "complex (" + "+".join(kws) + ")")
    if kws:
        pattern = {
            "WHILE": "state-driven",
            "WHEN": "event-driven",
            "IF/THEN": "unwanted-behavior",
            "WHERE": "optional-feature",
        }[kws[0]]
        return (True, pattern)
    if re.match(r"^\s*the\b", low):
        return (True, "ubiquitous")
    return (True, "warn: SHALL present but no EARS lead keyword")


def check(spec_path):
    with open(spec_path, "r", encoding="utf-8") as f:
        text = f.read()
    lines = text.splitlines()
    errors, warnings = [], []
    scope = spec_scope(text)
    if scope is None:
        warnings.append("no '**Scope**: Small|Medium|Large|Complex' line - Medium+ rules applied")
    small = scope == "Small"

    # 1. Required sections.
    for name in (REQUIRED_SECTIONS_SMALL if small else REQUIRED_SECTIONS):
        if section_bounds(lines, name) is None:
            errors.append(f"missing required section: ## {name}")
    for name in ("Existing Capabilities", "Standards"):
        b = section_bounds(lines, name)
        if b:
            body = [lines[i].strip() for i in range(*b) if lines[i].strip() and not lines[i].strip().startswith(">")]
            if not body or all(PLACEHOLDER_RE.match(ln) for ln in body):
                errors.append(f"## {name} is empty or still a template placeholder")

    # 2. Acceptance criteria: ID + EARS shape, each with Scenarios.
    parsed = parse_spec(text)
    for line, msg in parsed["problems"]:
        errors.append(f"L{line}: {msg}")
    for ac in parsed["acs"]:
        ok, note = classify_ears(ac["text"])
        if not ok:
            errors.append(f"L{ac['line']}: {ac['id']} has no SHALL (not testable): {ac['text'][:70]}")
        elif note.startswith("warn"):
            warnings.append(f"L{ac['line']}: {ac['id']} has SHALL but no EARS keyword (WHEN/WHILE/WHERE/IF or ubiquitous 'The … shall'): {ac['text'][:60]}")
    if not parsed["acs"]:
        warnings.append("no acceptance criteria with IDs parsed - is the spec filled in?")

    if small:
        return errors, warnings

    # 3. Assumptions table cells filled.
    b = section_bounds(lines, "Assumptions & Open Questions")
    if b:
        rows = [lines[i] for i in range(*b) if lines[i].strip().startswith("|")]
        data = [r for r in rows if not is_separator(r)]
        # drop the header row (first table row)
        if data:
            data = data[1:]
        template_seen = False
        for r in data:
            cells = split_row(r)
            if len(cells) < 3:
                continue
            assumption, chosen, rationale = cells[0], cells[1], cells[2]
            if PLACEHOLDER_RE.match(assumption) and PLACEHOLDER_RE.match(chosen):
                template_seen = True
                continue
            if not chosen or PLACEHOLDER_RE.match(chosen):
                errors.append(f"assumption '{assumption[:40]}' has empty 'Chosen default'")
            if not rationale or PLACEHOLDER_RE.match(rationale):
                errors.append(f"assumption '{assumption[:40]}' has empty 'Rationale'")
        if template_seen:
            warnings.append("Assumptions table still contains template placeholder rows")
        # open questions line
        oq = [lines[i] for i in range(*b) if "open questions" in lines[i].lower()]
        oq_clean = re.sub(r"[*_]", "", " ".join(oq)).lower()
        if not oq:
            warnings.append("no 'Open questions:' line in Assumptions section")
        elif not re.search(r"open questions.*:\s*none", oq_clean):
            warnings.append("open questions do not read as resolved ('Open questions: none')")

    # 4. Requirement traceability IDs.
    b = section_bounds(lines, "Requirement Traceability")
    if b:
        rows = [lines[i] for i in range(*b) if lines[i].strip().startswith("|")]
        data = [r for r in rows if not is_separator(r)]
        if data:
            data = data[1:]
        template_seen = False
        real_ids = 0
        for r in data:
            cells = split_row(r)
            if not cells:
                continue
            rid = cells[0]
            if PLACEHOLDER_RE.match(rid) or "[" in rid:
                template_seen = True
                continue
            if not rid:
                continue
            if not ID_RE.match(rid):
                errors.append(f"malformed requirement ID: '{rid}' (expected e.g. AUTH-01)")
            else:
                real_ids += 1
        if template_seen and real_ids == 0:
            warnings.append("Requirement Traceability has only template rows (no real IDs yet)")
        listed = {split_row(r)[0] for r in data if split_row(r)}
        for ac in parsed["acs"]:
            if ac["id"] not in listed:
                errors.append(f"{ac['id']} is missing from Requirement Traceability")

    return errors, warnings


def main(argv=None):
    p = argparse.ArgumentParser(prog="validate_spec.py", description="Closure-gate checks for a feature spec.md.")
    p.add_argument("target", nargs="?", default=None)
    p.add_argument("--root", default=".")
    p.add_argument("--strict", action="store_true")
    args = p.parse_args(argv)

    spec = resolve_spec(args.target, args.root)
    if not spec:
        print("validate_spec: could not locate a spec.md. Pass a path or run from the project root.", file=sys.stderr)
        return 2

    errors, warnings = check(spec)
    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  ERROR {e}")
    fail = errors or (warnings and args.strict)
    print(f"\nvalidate_spec: {len(errors)} error(s), {len(warnings)} warning(s) in {spec}")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
