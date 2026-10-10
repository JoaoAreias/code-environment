---
name: spec-review
description: Human-triggered Spec Review of a spec-driven feature plan (spec, design, tasks) before Execution Approval. Runs the independent spec-reviewer agent. Use only when the user types /spec-review.
disable-model-invocation: true
argument-hint: "[feature]"
---

Spec Review of a spec-driven feature plan. `SD` = `{{SPEC_DRIVEN_DIR}}`. `<arguments>` = whatever the user typed after the command (may be empty).

1. From the repository root, run `python3 SD/scripts/prep_review.py spec <arguments>`.
   - Exit 1 (`STOP: ...`): show the message to the user verbatim and stop.
   - Exit 0: the output is the **Review context**.
2. Delegate to the `spec-reviewer` subagent with the Review context, verbatim, as its whole prompt. Add nothing: no summary, no opinion about the plan.
3. When it returns, follow `SD/references/review.md` from "After a reviewer returns".
