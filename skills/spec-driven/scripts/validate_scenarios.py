#!/usr/bin/env python3
"""
validate_scenarios.py - cross-check tests against the Spec's Scenarios.

Scenarios, not tests, are the contract. Every test proves exactly one Scenario
and carries its ID plus Given/When/Then text in a comment or docstring:

    def test_rejects_expired_card():
        \"\"\"
        Scenario: PAY-01.S2
          Given a card that expired last month
          When the customer pays
          Then the payment is declined with "card_expired"
        \"\"\"

What it checks (heuristic, stack-agnostic):
  ERROR  - a test names a Scenario ID that no spec defines
  ERROR  - a test's Given/When/Then text drifted from the spec (or is missing)
  ERROR  - a test claims more than one Scenario
  ERROR  - a Scenario of this feature has no test proving it (skip with --no-missing)
  ERROR  - with --since: a test added or modified since REF claims no Scenario
           (Unclaimed Test touched by the Change; claim it or drop it)
  WARN   - several tests claim the same Scenario
  INFO   - count of Grandfathered Tests (no Scenario, untouched)

Usage:
  python3 <skill-dir>/scripts/validate_scenarios.py [feature] [--root DIR]
          [--since REF] [--only ID[,ID...]] [--no-missing] [--tests PATH ...]

  feature       Feature name under .specs/features/ (auto-detected when only one).
  --since REF   Git ref; tests touched between REF and the working tree must be claimed.
  --only IDS    Limit the missing-proof check to these Scenario IDs (per-task gate).
  --no-missing  Skip the missing-proof check (e.g. before Execute).
  --tests       Explicit test files (default: git-tracked + untracked files that look like tests).

Exit codes: 0 pass, 1 errors found, 2 usage error.
"""

import argparse
import os
import sys

from scenarios_lib import (changed_lines, is_test_path, load_all_specs, parse_spec,
                           parse_test_file, tracked_and_untracked)


def resolve_feature(root, feature):
    base = os.path.join(root, ".specs", "features")
    if feature:
        path = feature if os.path.isfile(os.path.join(feature, "spec.md")) else os.path.join(base, feature)
        return os.path.basename(os.path.normpath(path)), os.path.join(path, "spec.md")
    feats = [d for d in sorted(os.listdir(base)) if os.path.isfile(os.path.join(base, d, "spec.md"))] if os.path.isdir(base) else []
    if len(feats) == 1:
        return feats[0], os.path.join(base, feats[0], "spec.md")
    return None, None


def run(root, feature, since=None, only=None, check_missing=True, tests=None):
    errors, warnings, infos = [], [], []
    name, spec_path = resolve_feature(root, feature)
    if not spec_path or not os.path.isfile(spec_path):
        raise SystemExit("validate_scenarios: could not locate the feature spec; pass the feature name")
    own = parse_spec(open(spec_path, encoding="utf-8", errors="replace").read())["scenarios"]
    index = load_all_specs(root)

    files = tests if tests else [f for f in tracked_and_untracked(root) if is_test_path(f)]
    touched = changed_lines(root, since, files) if since else {}
    claimed_by = {}
    grandfathered = 0
    for rel in files:
        path = os.path.join(root, rel)
        if not os.path.isfile(path):
            continue
        for t in parse_test_file(open(path, encoding="utf-8", errors="replace").read()):
            where = f"{rel}:{t['line']} {t['name']}"
            claims = t["claims"]
            if len(claims) > 1:
                errors.append(f"{where}: claims {len(claims)} Scenarios ({', '.join(sorted(claims))}); a test proves exactly one")
            for sid, steps in claims.items():
                claimed_by.setdefault(sid, []).append(where)
                if sid not in index:
                    errors.append(f"{where}: Scenario {sid} is not defined in any spec")
                    continue
                spec_steps = index[sid][1]["steps"]
                if not steps:
                    errors.append(f"{where}: Scenario {sid} has no Given/When/Then text; copy it from the spec")
                elif steps != spec_steps:
                    errors.append(f"{where}: Scenario {sid} text drifted from the spec\n"
                                  f"      spec: {' | '.join(spec_steps)}\n"
                                  f"      test: {' | '.join(steps)}")
            if not claims:
                lines = touched.get(rel, set())
                if since and any(t["start"] <= ln <= t["end"] for ln in lines):
                    errors.append(f"{where}: Unclaimed Test touched since {since}; back-fill a Scenario in the spec or drop the test")
                else:
                    grandfathered += 1

    wanted = set(own) if not only else {s for s in only if s in own}
    for sid in sorted(set(only or ()) - set(own)):
        errors.append(f"--only names {sid}, which {name}'s spec does not define")
    if check_missing:
        for sid in sorted(wanted):
            if sid not in claimed_by:
                errors.append(f"Scenario {sid} has no test proving it")
    for sid, where in sorted(claimed_by.items()):
        if len(where) > 1 and sid in own:
            warnings.append(f"Scenario {sid} is claimed by {len(where)} tests: {', '.join(where)}")
    infos.append(f"{len(own)} Scenario(s) in {name}; {sum(1 for s in own if s in claimed_by)} proven; "
                 f"{grandfathered} test(s) without a Scenario left untouched (Grandfathered or outside --since)")
    return errors, warnings, infos


def main(argv=None):
    p = argparse.ArgumentParser(prog="validate_scenarios.py", description="Cross-check tests against spec Scenarios.")
    p.add_argument("feature", nargs="?", default=None)
    p.add_argument("--root", default=".")
    p.add_argument("--since", default=None)
    p.add_argument("--only", default="")
    p.add_argument("--no-missing", action="store_true")
    p.add_argument("--tests", nargs="*", default=None)
    args = p.parse_args(argv)
    root = os.path.abspath(args.root)
    only = [s.strip() for s in args.only.split(",") if s.strip()] or None
    errors, warnings, infos = run(root, args.feature, args.since, only, not args.no_missing, args.tests)
    for i in infos:
        print(f"  INFO  {i}")
    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  ERROR {e}")
    print(f"\nvalidate_scenarios: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
