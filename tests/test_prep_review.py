"""Scenario tests for prep_review.py spec. Fixtures: cases under tests/fixtures/ laid over tests/fixtures/base/."""

import hashlib
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


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, text=True).stdout


def head_paths(repo):
    return git(repo, "show", "--name-only", "--format=", "HEAD").split()


def read(root, path):
    with open(os.path.join(root, path), "rb") as f:
        return f.read()


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


class ForeignPlans(unittest.TestCase):

    def test_review_a_teammates_plan(self):
        """
        Scenario: PLAN-04.S1 review a teammate's plan
          Given a fixture repository with a committed docs/rfcs/042-billing.md and no .specs/features/ folder for it
          When prep_review.py spec docs/rfcs/042-billing.md runs
          Then it exits 0
          And its output says the structural validators were skipped because the plan is foreign
          And its output names the report path .specs/reviews/docs-rfcs-042-billing/spec-review-1.md
          And docs/rfcs/042-billing.md is unchanged
        """
        plan = "docs/rfcs/042-billing.md"
        repo = fixtures.build_repo(self, "foreign-rfc")
        code, out = prep(repo, plan)
        self.assertEqual(code, 0, out)
        self.assertRegex(out, r"(?m)^Skipped: the plan is foreign\b.*`validate_spec\.py` and `validate_tasks\.py`")
        self.assertNotRegex(out, r"validate_\w+\.py` exit")
        self.assertIn("write the report to `.specs/reviews/docs-rfcs-042-billing/spec-review-1.md`", out)
        self.assertEqual(read(repo, plan), read(os.path.join(fixtures.FIXTURES_DIR, "foreign-rfc"), plan))
        self.assertEqual(git(repo, "status", "--porcelain", "--", plan), "")
        self.assertEqual(git(repo, "log", "--format=%s", "--", plan).splitlines(), ["test: fixture foreign-rfc"])

    def test_same_named_plans_keep_separate_histories(self):
        """
        Scenario: PLAN-04.S2 same-named plans keep separate histories
          Given a fixture repository with committed .kiro/specs/payments/design.md and .kiro/specs/orders/design.md
          And .specs/reviews/kiro-specs-payments-design/spec-review-1.md already exists
          When prep_review.py spec .kiro/specs/orders/design.md runs
          Then its output names the report path .specs/reviews/kiro-specs-orders-design/spec-review-1.md
          And its output says there is no previous run
        """
        repo = fixtures.build_repo(self, "foreign-kiro", "foreign-kiro-reviewed")
        code, out = prep(repo, ".kiro/specs/orders/design.md")
        self.assertEqual(code, 0, out)
        self.assertIn("write the report to `.specs/reviews/kiro-specs-orders-design/spec-review-1.md`", out)
        self.assertRegex(out, r"(?m)^- Previous run: none$")

    def test_a_folder_is_one_plan(self):
        """
        Scenario: PLAN-04.S3 a folder is one plan
          Given a fixture repository with committed .kiro/specs/payments/requirements.md, design.md and tasks.md
          When prep_review.py spec .kiro/specs/payments/ runs
          Then it exits 0
          And its output lists all three files as the plan files
          And its output names the report path .specs/reviews/kiro-specs-payments/spec-review-1.md
        """
        repo = fixtures.build_repo(self, "foreign-kiro")
        code, out = prep(repo, ".kiro/specs/payments/")
        self.assertEqual(code, 0, out)
        self.assertRegex(out, r"(?m)^- Plan files: `\.kiro/specs/payments/design\.md`, "
                              r"`\.kiro/specs/payments/requirements\.md`, `\.kiro/specs/payments/tasks\.md`$")
        self.assertIn("write the report to `.specs/reviews/kiro-specs-payments/spec-review-1.md`", out)


    def test_colliding_slugs_keep_separate_histories(self):
        """
        Scenario: PLAN-04.S4 two plans whose slugs collide keep separate histories
          Given a fixture repository with committed docs/042_billing.md and docs/042-billing.md
          And .specs/reviews/docs-042-billing/ already holds a spec-review-1.md made for docs/042_billing.md
          When prep_review.py spec docs/042-billing.md runs
          Then its output names a report path under .specs/reviews/docs-042-billing-<hash>/ whose hash comes from the path docs/042-billing.md
          And its output says there is no previous run
        """
        repo = fixtures.build_repo(self, "foreign-slug-collide")
        code, out = prep(repo, "docs/042-billing.md")
        self.assertEqual(code, 0, out)
        digest = hashlib.sha1(b"docs/042-billing.md").hexdigest()[:8]
        self.assertIn(f"write the report to `.specs/reviews/docs-042-billing-{digest}/spec-review-1.md`", out)
        self.assertRegex(out, r"(?m)^- Previous run: none$")
        self.assertEqual(read(repo, f".specs/reviews/docs-042-billing-{digest}/source.txt"), b"docs/042-billing.md\n")
        self.assertEqual(read(repo, ".specs/reviews/docs-042-billing/source.txt"), b"docs/042_billing.md\n")


class FeaturePaths(unittest.TestCase):

    def test_a_path_into_a_feature_folder_names_the_feature(self):
        """
        Scenario: PLAN-06.S1 a path into a feature folder names the feature
          Given a fixture repository with a native feature demo
          When prep_review.py spec .specs/features/demo/spec.md runs
          Then it exits 0
          And its output names the feature demo and the report path .specs/features/demo/spec-review-1.md
        """
        repo = fixtures.build_repo(self, *READY)
        code, out = prep(repo, ".specs/features/demo/spec.md")
        self.assertEqual(code, 0, out)
        self.assertRegex(out, r"(?m)^- Feature: `demo` ")
        self.assertIn("write the report to `.specs/features/demo/spec-review-1.md`", out)

if __name__ == "__main__":
    unittest.main()
