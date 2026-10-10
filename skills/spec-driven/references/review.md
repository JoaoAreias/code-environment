# Reviews: what the main session does

Two independent reviewers sit around Execute:

- **Spec Review** judges the plan (Spec, design, tasks) once planning ends, before anything is built. Agent: `spec-reviewer`. Trigger: `/spec-review`.
- **Change Review** judges the built Change after the Verifier passed. Agent: `change-reviewer`. Trigger: `/code-review`.

Only the human starts a review. Never run `/spec-review` or `/code-review` yourself, never dispatch either reviewer agent on your own initiative, and never re-run a review because the plan changed: whether to review again is the human's call.

Report format: [finding-format.md](finding-format.md). Rule list both reviewers apply: [standards.md](standards.md).

---

## Execution Approval

Nothing gets built without the human's explicit go-ahead to execute. Agreeing to a Spec, a design or a task list along the way is provisional ("show me the rest"), and accepting a Finding is not a go-ahead either.

- **New feature:** before Execute, the latest `spec-review-<n>.md` exists and every Finding in it has a Disposition. If no Spec Review exists, remind the human that `/spec-review` comes first and wait. If Findings lack Dispositions, list them and wait.
- **Fixes from a Change Review:** the Findings they address have Dispositions, the fix tasks are in `tasks.md`, and the human says go.

Remote or destructive actions (push, deploy, production data) still need their own explicit go-ahead.

---

## After a reviewer returns

1. **Show** the report path and the reviewer's summary table (ID, severity, dimension, one-line Finding). Do not paste the whole report.
2. **Ask for Dispositions.** Accept shorthand: `accept all`, `accept F1 F2, reject F3: we never store card data, grill F4`. IDs may drop the run prefix.
3. **Grill** each Finding marked `grill`, one at a time, until the human accepts or rejects it:
   - Start from the Finding's evidence and its **Would change my mind** line. Re-run the queries, read the cited code, and report what you found.
   - You probably wrote the plan or the code under review. Lead with evidence, not with the reasons behind the original choice; give those reasons only when asked.
   - A grilled Finding still ends as `accept` or `reject: <reason>`.
4. **Record** the decisions in the report file, editing only the `**Disposition**` lines (`accept` or `reject: <reason>`) and, for grilled Findings, adding one `**Grill notes**:` line under it. Never edit the reviewer's text.
5. **Commit** the report: `docs(review): record dispositions for SR2` (or `CR1`). Only the report file goes in this commit. A later review needs a clean tree.
6. **Distill Lessons** with `python3 <skill-dir>/scripts/lessons.py add ...` (see [lessons.md](lessons.md)):
   - each accepted Finding whose lesson generalizes: `--signal spec_review_finding` or `--signal change_review_finding`, `--source "<report file> <ID>"`
   - each rejected Finding whose reason generalizes ("this repo uses Active Record on purpose"): `--signal review_rejection`, phrased as what reviewers should not raise here and why
   - one-off decisions produce no lesson; the 2-feature recurrence rule keeps them out anyway
7. **Next step:**
   - **Spec Review:** apply the accepted Findings to `spec.md`, `design.md` or `tasks.md` and re-run the structural validators. Then stop and wait for Execution Approval. A new Spec Review after these edits is the human's call.
   - **Change Review:** turn each accepted Finding into a fix task appended to `tasks.md` (`### T<n>: Fix CR1-F3 <short title>` with a `**Fixes**: CR1-F3` field; normal `Tests`, `Scenarios` and `Gate` fields apply). A fix that changes behavior edits the Spec and its Scenarios first. Then wait for Execution Approval, execute, let the Verifier re-run, and leave re-review to the human.
   - **Change Review with `--no-spec`:** there is no `tasks.md`. List the accepted Findings as a fix plan in chat; the human decides how to proceed.

---

## If a reviewer touched more than its report

Reviewers may write only their own report file. After each review, check `git status`. If anything else changed, tell the human exactly which paths changed and the commit to restore them from (the pre-review commit for a Spec Review, `HEAD` for a Change Review). Do not restore anything without the human's go-ahead.
