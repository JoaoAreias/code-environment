---
name: code-review
description: Human-triggered Change Review of committed work against its spec-driven Spec, after the Verifier passed. Runs the independent change-reviewer agent with graphify and SonarQube evidence. Use only when the user types /code-review.
disable-model-invocation: true
argument-hint: "[feature] [--base REF] [--no-spec] [--unverified] [--sonar-project KEY]"
---

Change Review of committed work. `SD` = `{{SPEC_DRIVEN_DIR}}`. `<arguments>` = whatever the user typed after the command (may be empty).

1. **SonarQube check.** Look for SonarQube MCP tools among the tools available to you: names containing `sonar`, such as `search_sonar_issues_in_projects`. Some harnesses list them as deferred tools. If there are none, tell the user "SonarQube MCP is not configured or not connected; fix it, then re-run /code-review", and stop.
2. From the repository root, run `python3 SD/scripts/prep_review.py change <arguments>`, leaving out any `--sonar-project KEY` pair.
   - Exit 1 (`STOP: ...`): show the message to the user verbatim and stop.
   - Exit 0: the output is the **Review context**. If the user passed `--sonar-project KEY`, append the line `- Sonar project: KEY`.
3. Delegate to the `change-reviewer` subagent with the Review context, verbatim, as its whole prompt. Add nothing: no summary, no opinion about the code.
4. When it returns: if its reply starts with `STOP:`, show it and stop. Otherwise follow `SD/references/review.md` from "After a reviewer returns".
