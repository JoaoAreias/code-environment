"""Scenario tests for prep_review.py spec. Fixtures: cases under tests/fixtures/ laid over tests/fixtures/base/."""

import os
import subprocess
import unittest

import fixtures

READY = ("base", "design")  # a native feature `demo` with spec.md, design.md and tasks.md


def prep(repo, target):
    return fixtures.run_script(repo, "prep_review.py", "spec", target)


def edit(repo, *paths):
    """Leave an uncommitted edit in each tracked path."""
    for path in paths:
        with open(os.path.join(repo, path), "a", encoding="utf-8") as f:
            f.write("\nA line added after the last commit.\n")


def head_paths(repo):
    out = subprocess.run(["git", "-C", repo, "show", "--name-only", "--format=", "HEAD"],
                         check=True, capture_output=True, text=True).stdout
    return out.split()


class Snapshot(unittest.TestCase):

    def test_snapshot_includes_records_and_glossary(self):
        """
        Scenario: REV-01.S1 snapshot includes records and glossary
          Given a fixture repository with a committed spec and tasks for feature demo
          And uncommitted edits to .specs/decisions/demo.md, .specs/decisions/summary.md and CONTEXT.md
          When prep_review.py spec demo runs
          Then it exits 0
          And the HEAD commit contains those three paths
        """
        repo = fixtures.build_repo(self, *READY, "records")
        edited = [".specs/decisions/demo.md", ".specs/decisions/summary.md", "CONTEXT.md"]
        edit(repo, *edited)
        code, out = prep(repo, "demo")
        self.assertEqual(code, 0, out)
        self.assertEqual(sorted(head_paths(repo)), sorted(edited))

    def test_snapshot_includes_per_context_glossaries(self):
        """
        Scenario: REV-01.S2 snapshot includes per-context glossaries
          Given a fixture repository with a committed spec and tasks for feature demo
          And uncommitted edits to CONTEXT-MAP.md and src/billing/CONTEXT.md
          When prep_review.py spec demo runs
          Then it exits 0
          And the HEAD commit contains CONTEXT-MAP.md and src/billing/CONTEXT.md
        """
        repo = fixtures.build_repo(self, *READY, "context-map")
        edited = ["CONTEXT-MAP.md", "src/billing/CONTEXT.md"]
        edit(repo, *edited)
        code, out = prep(repo, "demo")
        self.assertEqual(code, 0, out)
        self.assertEqual(sorted(head_paths(repo)), sorted(edited))


class DecisionSources(unittest.TestCase):

    def test_review_context_lists_the_record(self):
        """
        Scenario: REV-02.S1 review context lists the record
          Given summary.md has a row for demo.md with Specs "demo"
          And the demo spec has a Grilling Record line and the feature folder has no context.md
          When prep_review.py spec demo runs
          Then its output lists .specs/decisions/demo.md
          And its output does not mention context.md
        """
        repo = fixtures.build_repo(self, *READY, "records")
        code, out = prep(repo, "demo")
        self.assertEqual(code, 0, out)
        self.assertRegex(out, r"(?m)^- Grilling Records: `\.specs/decisions/demo\.md`$")
        self.assertNotIn("context.md", out)

    def test_legacy_feature_keeps_its_context(self):
        """
        Scenario: REV-02.S2 legacy feature keeps its context
          Given a feature old-demo whose spec has no Grilling Record line and whose folder has a committed context.md
          When prep_review.py spec old-demo runs
          Then its output lists .specs/features/old-demo/context.md as a legacy decision source
        """
        repo = fixtures.build_repo(self, "feature-old-demo")
        code, out = prep(repo, "old-demo")
        self.assertEqual(code, 0, out)
        self.assertRegex(out, r"(?m)^- Legacy decision source: `\.specs/features/old-demo/context\.md`$")

    def test_native_feature_keeps_its_context(self):
        """
        Scenario: REV-02.S3 native feature keeps its context
          Given a feature re-demo whose spec has a Grilling Record line and whose folder has a committed context.md
          When prep_review.py spec re-demo runs
          Then its output lists .specs/features/re-demo/context.md as a legacy decision source
        """
        repo = fixtures.build_repo(self, "feature-re-demo")
        code, out = prep(repo, "re-demo")
        self.assertEqual(code, 0, out)
        self.assertRegex(out, r"(?m)^- Legacy decision source: `\.specs/features/re-demo/context\.md`$")


class MandatoryPlanFiles(unittest.TestCase):

    def test_small_spec_without_tasks(self):
        """
        Scenario: TKT-01.S1 small spec without tasks
          Given a fixture repository with a Small-scope spec for feature demo and no tasks.md
          When prep_review.py spec demo runs
          Then it exits 1
          And its output starts with "STOP" and names tasks.md
        """
        repo = fixtures.build_repo(self, "spec-small-none")
        code, out = prep(repo, "demo")
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"\ASTOP: .*tasks\.md")

    def test_medium_spec_without_design(self):
        """
        Scenario: TKT-02.S1 medium spec without design
          Given a fixture repository with a Medium-scope spec and a tasks.md for feature demo and no design.md
          When prep_review.py spec demo runs
          Then it exits 1
          And its output starts with "STOP" and names design.md
        """
        repo = fixtures.build_repo(self, "base", "spec-medium")
        code, out = prep(repo, "demo")
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"\ASTOP: .*design\.md")

    def test_small_spec_needs_no_design(self):
        """
        Scenario: TKT-02.S2 small spec needs no design
          Given a fixture repository with a Small-scope spec and a tasks.md for feature demo and no design.md
          When prep_review.py spec demo runs
          Then its output does not name design.md in a STOP message
        """
        repo = fixtures.build_repo(self, "base", "spec-small-none")
        code, out = prep(repo, "demo")
        self.assertEqual(code, 0, out)
        self.assertNotRegex(out, r"(?m)^STOP")
        self.assertIn("## Review context (Spec Review)", out)


if __name__ == "__main__":
    unittest.main()
