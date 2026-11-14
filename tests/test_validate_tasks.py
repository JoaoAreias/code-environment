"""Scenario tests for validate_tasks.py. Fixtures: tests/fixtures/tasks-*/ laid over tests/fixtures/base/."""

import unittest

import fixtures


def validate(test, *cases):
    repo = fixtures.build_repo(test, *cases)
    return fixtures.run_script(repo, "validate_tasks.py", "demo", "--root", repo)


class Tickets(unittest.TestCase):

    def test_orphan_task(self):
        """
        Scenario: TKT-03.S1 orphan task
          Given a native tasks.md with tasks T1 and T2 and one Ticket K1 listing only T1
          When validate_tasks.py runs on it
          Then it exits 1
          And its output names T2
        """
        code, out = validate(self, "base", "tasks-orphan")
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"ERROR T2\b.*Ticket")
        self.assertIn("validate_tasks: 1 error(s)", out)

    def test_fix_task_inside_a_fix_ticket(self):
        """
        Scenario: TKT-03.S2 fix task inside a fix ticket
          Given a native tasks.md with Ticket K1 listing T1 and T2
          And an appended fix task "T3: Fix CR1-F1 null total" with a Fixes field, listed in Ticket "K2: Fix CR1" Blocked by K1
          When validate_tasks.py runs on it
          Then it exits 0
        """
        code, out = validate(self, "base", "tasks-fix-ticket")
        self.assertEqual(code, 0, out)

    def test_task_in_two_tickets(self):
        """
        Scenario: TKT-04.S1 task in two tickets
          Given a native tasks.md whose Tickets K1 and K2 both list T2
          When validate_tasks.py runs on it
          Then it exits 1
          And its output names T2, K1 and K2
        """
        code, out = validate(self, "base", "tasks-two-tickets")
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"ERROR T2\b.*\bK1\b.*\bK2\b")
        self.assertIn("validate_tasks: 1 error(s)", out)

    def test_forward_blocking_edge(self):
        """
        Scenario: TKT-05.S1 forward blocking edge
          Given a native tasks.md whose Ticket K1 is Blocked by K2 and K2 is listed after K1
          When validate_tasks.py runs on it
          Then it exits 1
          And its output names K1 and K2
        """
        code, out = validate(self, "base", "tasks-forward-block")
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"ERROR K1\b.*\bK2\b")
        self.assertIn("validate_tasks: 1 error(s)", out)


if __name__ == "__main__":
    unittest.main()
