"""Scenario tests for validate_scenarios.py (inspect proofs). Fixtures: tests/fixtures/proof-*/."""

import unittest

import fixtures


def validate(test, *cases):
    repo = fixtures.build_repo(test, *cases)
    return fixtures.run_script(repo, "validate_scenarios.py", "demo", "--root", repo)


class InspectProofs(unittest.TestCase):

    def test_pass_row_proves_an_inspect_scenario(self):
        """
        Scenario: PROOF-01.S1 pass row proves an inspect scenario
          Given a spec whose Scenario DEMO-01.S1 has proof type inspect and no test claims it
          And validation.md has a table with headers "Scenario | Spec-defined outcome (Then) | file:line + assertion expression | Result"
          And that table has the row "DEMO-01.S1 | the rule is stated | skills/demo/SKILL.md:12 - the rule is stated in step 3 | PASS"
          When validate_scenarios.py runs on the feature
          Then it exits 0
        """
        code, out = validate(self, "base")
        self.assertEqual(code, 0, out)

    def test_missing_row_fails(self):
        """
        Scenario: PROOF-01.S2 missing row fails
          Given a spec whose Scenario DEMO-01.S1 has proof type inspect and no test claims it
          And validation.md has the Scenario-Anchored table with no row for DEMO-01.S1
          When validate_scenarios.py runs on the feature
          Then it exits 1
          And its output names DEMO-01.S1
        """
        code, out = validate(self, "base", "proof-missing-row")
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"ERROR .*DEMO-01\.S1.*validation\.md")

    def test_gap_row_fails(self):
        """
        Scenario: PROOF-01.S3 gap row fails
          Given a spec whose Scenario DEMO-01.S1 has proof type inspect
          And the Scenario-Anchored table has the row "DEMO-01.S1 | the rule is stated | skills/demo/SKILL.md:12 - the rule is missing | ❌ GAP"
          When validate_scenarios.py runs on the feature
          Then it exits 1
          And its output names DEMO-01.S1
        """
        code, out = validate(self, "base", "proof-gap-row")
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"ERROR .*DEMO-01\.S1.*validation\.md")

    def test_pass_with_the_check_mark_is_accepted(self):
        """
        Scenario: PROOF-01.S4 pass with the check mark is accepted
          Given a spec whose Scenario DEMO-01.S1 has proof type inspect and no test claims it
          And the Scenario-Anchored table has the row "DEMO-01.S1 | the rule is stated | skills/demo/SKILL.md:12 - the rule is stated in step 3 | ✅ PASS"
          When validate_scenarios.py runs on the feature
          Then it exits 0
        """
        code, out = validate(self, "base", "proof-check-mark")
        self.assertEqual(code, 0, out)

    def test_duplicate_rows_fail(self):
        """
        Scenario: PROOF-01.S5 duplicate rows fail
          Given a spec whose Scenario DEMO-01.S1 has proof type inspect
          And the Scenario-Anchored table has two rows for DEMO-01.S1, one with Result "✅ PASS" and one with Result "❌ GAP"
          When validate_scenarios.py runs on the feature
          Then it exits 1
          And its output says DEMO-01.S1 has more than one row
        """
        code, out = validate(self, "base", "proof-duplicate-rows")
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"ERROR .*DEMO-01\.S1 has more than one row")


if __name__ == "__main__":
    unittest.main()
