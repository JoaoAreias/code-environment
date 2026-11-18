"""Scenario tests for install.sh. Fixtures: tests/fixtures/installed-*/ mirror a Claude config directory.

install.sh runs with CLAUDE_CONFIG_DIR, OPENCODE_CONFIG_DIR and HOME all pointing into one temp
directory, so it cannot reach the real configuration of the machine running the tests.
"""

import os
import shutil
import subprocess
import tempfile
import unittest

import fixtures

RETIRED = ("ask-matt", "implement", "to-spec", "to-tickets", "triage", "wayfinder", "wizard", "setup-matt-pocock-skills")


def sandbox(test):
    """Return (temp dir, Claude config dir inside it); the temp dir is removed when `test` finishes."""
    if shutil.which("graphify") is None:
        raise RuntimeError("graphify is not on PATH: without it install.sh would try to install it; install it first")
    tmp = tempfile.mkdtemp(prefix="install-fixture-")
    test.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
    claude = os.path.join(tmp, "claude")
    os.makedirs(os.path.join(claude, "skills"))
    return tmp, claude


def installed(case, *names):
    return os.path.join(fixtures.FIXTURES_DIR, case, "skills", *names)


def install(tmp, claude):
    """Run install.sh against the sandbox; return (exit code, stdout + stderr)."""
    home = os.path.join(tmp, "home")
    os.makedirs(home, exist_ok=True)
    env = {**os.environ, "CLAUDE_CONFIG_DIR": claude, "OPENCODE_CONFIG_DIR": os.path.join(tmp, "opencode"), "HOME": home}
    r = subprocess.run(["bash", os.path.join(fixtures.REPO_ROOT, "install.sh")], cwd=tmp, env=env, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def read(*parts):
    with open(os.path.join(*parts), "rb") as f:
        return f.read()


class RetiredSkills(unittest.TestCase):

    def test_retired_skills_removed(self):
        """
        Scenario: FLOW-01.S1 retired skills removed
          Given a temporary Claude config directory whose skills/ holds this repository's shipped copies of ask-matt, implement, to-spec, to-tickets, triage, wayfinder, wizard and setup-matt-pocock-skills
          When install.sh runs with that directory
          Then none of those eight skill directories exist
        """
        tmp, claude = sandbox(self)
        shutil.copytree(installed("installed-retired"), os.path.join(claude, "skills"), dirs_exist_ok=True)
        self.assertEqual(sorted(os.listdir(os.path.join(claude, "skills"))), sorted(RETIRED))
        code, out = install(tmp, claude)
        self.assertEqual(code, 0, out)
        left = [name for name in RETIRED if os.path.lexists(os.path.join(claude, "skills", name))]
        self.assertEqual(left, [], out)

    def test_another_sources_skill_survives(self):
        """
        Scenario: FLOW-01.S2 another source's skill survives
          Given a temporary Claude config directory whose skills/triage/SKILL.md was written by another source and lacks this repository's phrase
          When install.sh runs with that directory
          Then skills/triage/SKILL.md still exists with the same content
          And the output says "skipped triage: not installed by this repo"
        """
        tmp, claude = sandbox(self)
        shutil.copytree(installed("installed-other-triage"), os.path.join(claude, "skills"), dirs_exist_ok=True)
        code, out = install(tmp, claude)
        self.assertEqual(code, 0, out)
        self.assertEqual(read(claude, "skills", "triage", "SKILL.md"), read(installed("installed-other-triage", "triage", "SKILL.md")))
        self.assertEqual(os.listdir(os.path.join(claude, "skills", "triage")), ["SKILL.md"])
        self.assertIn("skipped triage: not installed by this repo", out)

    def test_a_symlinked_skill_survives(self):
        """
        Scenario: FLOW-01.S3 a symlinked skill survives
          Given a temporary Claude config directory whose skills/implement is a symlink to a directory holding this repository's shipped implement skill
          When install.sh runs with that directory
          Then skills/implement is still a symlink and its target is unchanged
          And the output says "skipped implement: not installed by this repo"
        """
        tmp, claude = sandbox(self)
        target = os.path.join(tmp, "elsewhere", "implement")
        shutil.copytree(installed("installed-retired", "implement"), target)
        link = os.path.join(claude, "skills", "implement")
        os.symlink(target, link)
        code, out = install(tmp, claude)
        self.assertEqual(code, 0, out)
        self.assertTrue(os.path.islink(link), out)
        self.assertEqual(os.readlink(link), target)
        self.assertEqual(os.listdir(target), ["SKILL.md"])
        self.assertEqual(read(target, "SKILL.md"), read(installed("installed-retired", "implement", "SKILL.md")))
        self.assertIn("skipped implement: not installed by this repo", out)


class NewSkills(unittest.TestCase):

    def test_new_skills_installed(self):
        """
        Scenario: FLOW-02.S1 new skills installed
          Given an empty temporary Claude config directory
          When install.sh runs with that directory
          Then skills/grilling/SKILL.md and skills/setup-spec-driven/SKILL.md exist in it
        """
        tmp, claude = sandbox(self)
        self.assertEqual(os.listdir(claude), ["skills"])
        self.assertEqual(os.listdir(os.path.join(claude, "skills")), [])
        code, out = install(tmp, claude)
        self.assertEqual(code, 0, out)
        for name in ("grilling", "setup-spec-driven"):
            self.assertTrue(os.path.isfile(os.path.join(claude, "skills", name, "SKILL.md")), out)


if __name__ == "__main__":
    unittest.main()
