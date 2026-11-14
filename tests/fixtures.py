"""
fixtures.py - build a throwaway git repository for the script tests.

A case is a folder under tests/fixtures/<case>/ that mirrors a repository root
(for example tests/fixtures/base/.specs/features/demo/spec.md). build_repo copies
one or more cases into a temp dir, later cases overlaying earlier ones, so a case
only holds the files that differ from `base`.

Sample specs, tasks and validation files stay in those .md files. Never put sample
Scenario text inside a test function: scenarios_lib.parse_test_file reads every
line of a test function as a possible Scenario claim.
"""

import os
import shutil
import subprocess
import sys
import tempfile

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
FIXTURES_DIR = os.path.join(TESTS_DIR, "fixtures")
REPO_ROOT = os.path.dirname(TESTS_DIR)
SCRIPTS_DIR = os.path.join(REPO_ROOT, "skills", "spec-driven", "scripts")


def build_repo(test, *cases):
    """Copy the named fixture cases into a new committed git repo; return its path.

    The repo is removed when `test` (a unittest.TestCase) finishes.
    """
    if shutil.which("graphify") is None:
        raise RuntimeError("graphify is not on PATH: the script tests run against the real graphify; install it first")
    repo = tempfile.mkdtemp(prefix="spec-driven-fixture-")
    test.addCleanup(shutil.rmtree, repo, ignore_errors=True)
    for case in cases:
        src = os.path.join(FIXTURES_DIR, case)
        if not os.path.isdir(src):
            raise RuntimeError(f"no fixture case at {src}")
        shutil.copytree(src, repo, dirs_exist_ok=True)
    for args in (("init", "-q"), ("add", "-A"),
                 ("-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false",
                  "commit", "-q", "--no-verify", "-m", "test: fixture " + "+".join(cases))):
        subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, text=True)
    return repo


def run_script(repo, script, *args):
    """Run skills/spec-driven/scripts/<script> inside `repo`; return (exit code, stdout + stderr)."""
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS_DIR, script), *args],
                       cwd=repo, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr
