"""Scenario tests for validate_spec.py. Fixtures: tests/fixtures/spec-*/ laid over tests/fixtures/base/."""

import unittest

import fixtures


def validate(test, *cases):
    repo = fixtures.build_repo(test, *cases)
    return fixtures.run_script(repo, "validate_spec.py", "demo", "--root", repo)


class DecisionsAndAssumptions(unittest.TestCase):

    def test_small_spec_without_the_section(self):
        """
        Scenario: GRILL-05.S1 small spec without the section
          Given a Small-scope spec.md with a Grilling Record line and every Small section except "Decisions & Assumptions"
          When validate_spec.py runs on it
          Then it exits 1
          And its output names "Decisions & Assumptions"
        """
        code, out = validate(self, "base", "spec-small-no-decisions")
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"ERROR .*Decisions & Assumptions")
        self.assertIn("validate_spec: 1 error(s)", out)

    def test_large_spec_with_the_old_heading(self):
        """
        Scenario: GRILL-05.S2 large spec with the old heading
          Given a Large-scope spec.md with a Grilling Record line whose assumptions section is titled "Assumptions & Open Questions"
          When validate_spec.py runs on it
          Then it exits 1
          And its output names "Decisions & Assumptions"
        """
        code, out = validate(self, "base", "spec-old-heading")
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"ERROR .*Decisions & Assumptions")
        self.assertIn("validate_spec: 1 error(s)", out)

    def test_none_is_allowed(self):
        """
        Scenario: GRILL-06.S1 none is allowed
          Given a valid Small-scope spec.md with a Grilling Record line whose "Decisions & Assumptions" section reads "none"
          When validate_spec.py runs on it
          Then it exits 0
        """
        code, out = validate(self, "base", "spec-small-none")
        self.assertEqual(code, 0, out)

    def test_empty_choice_in_the_decisions_table(self):
        """
        Scenario: GRILL-09.S1 empty choice in the decisions table
          Given a Large-scope spec.md with a Grilling Record line whose Decisions table has a row "D-demo.2" with an empty Choice cell
          When validate_spec.py runs on it
          Then it exits 1
          And its output names "D-demo.2"
        """
        code, out = validate(self, "base", "spec-empty-choice")
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"ERROR .*D-demo\.2")
        self.assertIn("validate_spec: 1 error(s)", out)

    def test_empty_chosen_default_in_the_assumptions_table(self):
        """
        Scenario: GRILL-09.S2 empty chosen default in the assumptions table
          Given a Large-scope spec.md with a Grilling Record line whose Assumptions table has a row "rows fit in memory" with an empty Chosen default cell
          When validate_spec.py runs on it
          Then it exits 1
          And its output names "rows fit in memory"
        """
        code, out = validate(self, "base", "spec-empty-default")
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"ERROR .*rows fit in memory")
        self.assertIn("validate_spec: 1 error(s)", out)


class LegacySpecs(unittest.TestCase):

    def test_legacy_spec_only_warns(self):
        """
        Scenario: PLAN-01.S1 legacy spec only warns
          Given a Large-scope spec.md with no Grilling Record line, an "Assumptions & Open Questions" section and every other required section
          When validate_spec.py runs on it
          Then it exits 0
          And its output warns about "Decisions & Assumptions"
        """
        code, out = validate(self, "base", "spec-legacy")
        self.assertEqual(code, 0, out)
        self.assertRegex(out, r"WARN .*Decisions & Assumptions")


if __name__ == "__main__":
    unittest.main()
