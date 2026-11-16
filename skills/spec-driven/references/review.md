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
- **Fixes from a Change Review:** the Findings they address have Dispositions, the fix tasks are in `tasks.md` inside one fix Ticket for that review, and the human says go.

Remote or destructive actions (push, deploy, production data) still need their own explicit go-ahead.

---

## After a reviewer returns

1. **Show** the report path and the reviewer's summary table (ID, severity, dimension, one-line Finding). Do not paste the whole report.
2. **Ask for Dispositions.** Accept shorthand: `accept all`, `accept F1 F2, reject F3: we never store card data, grill F4`. IDs may drop the run prefix.
3. **Grill** each Finding marked `grill`, one at a time, until the human accepts or rejects it:
   - Start from the Finding's evidence and its **Would change my mind** line. Re-run the queries, read the cited code, and report what you found.
   - You probably wrote the plan or the code under review. Lead with evidence, not with the reasons behind the original choice; give those reasons only when asked.
   - A grilled Finding still ends as `accept` or `reject: <reason>`.
4. **Record the Dispositions** in the report file, editing only the `**Disposition**` lines (`accept` or `reject: <reason>`) and, for grilled Findings, adding one `**Grill notes**:` line under it. Never edit the reviewer's text.
5. **Rewrite the Decisions the Dispositions changed**, in the Grilling Records that hold them. The full procedure is in [Dispositions and Decisions](#dispositions-and-decisions) below. Do this before the commit, so the report and the records always agree.
6. **Commit** the report together with the Grilling Records and the `summary.md` rows that step 5 changed: `docs(review): record dispositions for SR2` (or `CR1`). Nothing else goes in this commit. A later review needs a clean tree.
7. **Distill Lessons** with `python3 <skill-dir>/scripts/lessons.py add ...` (see [lessons.md](lessons.md)):
   - each accepted Finding whose lesson generalizes: `--signal spec_review_finding` or `--signal change_review_finding`, `--source "<report file> <ID>"`
   - each rejected Finding whose reason generalizes ("this repo uses Active Record on purpose"): `--signal review_rejection`, phrased as what reviewers should not raise here and why
   - one-off decisions produce no lesson; the 2-feature recurrence rule keeps them out anyway
8. **Next step:**
   - **Spec Review:** apply the accepted Findings to `spec.md`, `design.md` or `tasks.md`, so the plan matches the Decisions rewritten in step 5 (a changed Decision's row in the spec's `Decisions & Assumptions` table shows its new choice), and re-run the structural validators. Then stop and wait for Execution Approval. A new Spec Review after these edits is the human's call.
   - **Spec Review of a foreign plan:** the report and its Dispositions live under `.specs/reviews/<plan slug>/`. Never edit the foreign plan. List the accepted Findings so the human can take them to the plan's author; building from the plan starts with Specify ([decisions.md](decisions.md) section 4).
   - **Change Review:** turn the accepted Findings into fix tasks in **one fix Ticket for this review** ([Fix Ticket for a Change Review](#fix-ticket-for-a-change-review) below). A fix that changes behavior edits the Spec and its Scenarios first. Then wait for Execution Approval, execute, let the Verifier re-run, and leave re-review to the human.
   - **Change Review with `--no-spec`:** there is no `tasks.md`. List the accepted Findings as a fix plan in chat; the human decides how to proceed.

The order of steps 4 to 7 is fixed: record Dispositions, rewrite Decisions, commit, distill Lessons.

---

## Dispositions and Decisions

A **Decision** always shows its current choice. When a Disposition changes what was decided, the Decision's text is rewritten where it lives; git keeps the earlier text. The format is owned by the `domain-modeling` skill (`GRILLING-RECORD-FORMAT.md`, "Changing a Decision later"); this section says what the main session does after a review.

Go through the Findings one by one, after their Dispositions are recorded.

**1. An accepted Finding that changes an existing Decision: rewrite it in its original record.**

- Find the record that holds the Decision. It is the record the Decision's ID names (`D-csv-export.3` lives in `.specs/decisions/csv-export.md`), which may belong to another feature.
- Rewrite the Decision's **Choice** so that it states the new choice, and its **Reason** and **Trade-off** where they changed. The old choice is not kept beside the new one.
- Add one line at the end of that Decision:

  ```md
  - **Changed**: <YYYY-MM-DD> by <feature> (<source>): <what changed>
  ```

  `<feature>` is the feature under review. `<source>` names the review and the Finding, for example `spec-review-1 SR1-F2` or `change-review-1 CR1-F3`. A Decision that changes a second time gets a second `Changed` line.
- A `Decided by: agent` Decision that the human now chose becomes `Decided by: user`.

Example: `csv-export.md` holds `D-csv-export.3` "new Price type", and Finding `SR1-F2` recommends reusing `Money`. The human says "accept F2". Afterwards `D-csv-export.3` in `csv-export.md` chooses `Money`, and it ends with `- **Changed**: 2026-11-14 by csv-export (spec-review-1 SR1-F2): reuses Money instead of a new Price type`. The Decision keeps its ID and its place in the record.

**2. The Decision stays in the record that made it, whoever changes it.** The same rule holds when a later phase or a later feature changes a Decision, not only a review: the Decision is rewritten in its original record with a `Changed` line naming the feature that changed it, and the changing feature's own record does not restate the old choice as a new Decision. Example: `billing-retries.md` holds `D-billing-retries.2` "retry three times", and the Design of feature `invoice-pdf` decides to retry five times instead. Then `D-billing-retries.2` in `billing-retries.md` chooses five retries and has a `Changed` line naming `invoice-pdf` (source `Design`); `invoice-pdf.md` mentions the change in its Session path and Related section and adds no Decision of its own for it ([design.md](design.md) step 6). An accepted Finding of one feature's review that changes another record's Decision is handled the same way, with the review and Finding as the source.

**3. An accepted Finding that adds a rule no Decision covers: a new Decision under `## Review`.** Add a `## Review` section to the feature's record if it has none (after `## Design`, before `## Consequences`). Write the new Decision there with the next free ID of that record, in the usual shape (Choice, Reason, Trade-off, Binds, Decided by), and cite the Finding that caused it. Example: `csv-export.md`'s last Decision is `D-csv-export.8`, and the human accepts `SR1-F4`, which adds a rule no Decision covers. `csv-export.md` then has a `## Review` section holding `D-csv-export.9`, which cites `spec-review-1 SR1-F4`.

**4. A Finding that changes no Decision leaves only its Disposition.** A rejected Finding, and an accepted one that only fixes the plan or the code without changing a choice, touch no record.

**5. A grilled Finding is added to the Session path.** The Session path is never rewritten. A grill held during the review appends its own subsection to it, for example `### Spec Review SR1 grill (<date>)`, with one entry per Finding grilled: what was asked, the options, the recommendation, the answer, and the Decision IDs it touched.

**6. Update `summary.md` when the record's row changed.** If the rewrite changed what the record's Summary says, its Areas, its Binds or its Specs, correct the record's header and its row in `.specs/decisions/summary.md`. Otherwise leave the row alone. Add the review report to the record's Related section.

Rules that hold throughout:

- A record's Status is only `draft` or `active`. A Decision has no status of its own and is never marked as replaced, withdrawn or outdated, and no newer Decision is written to override an older one whose text stays. A Decision that stops applying is rewritten to say that it no longer applies and why, with a `Changed` line.
- Only the human changes a Decision. A Disposition of `accept` is that go-ahead for the Decisions the Finding names. Do not rewrite a Decision the Finding did not put in question.
- Legacy decision sources (`docs/adr/`, an old `## Decisions` section in `.specs/STATE.md`, a feature's `context.md`) are never written to. When an accepted Finding changes a choice that lives only there, record the new choice as a new Decision under `## Review` in the feature's record, saying which legacy entry it changes. A legacy plan with no record gets none created by a review: put the change in its `spec.md` and tell the human which legacy entry no longer holds.
- A foreign plan has no record of its own and is never edited. Its Dispositions stay in the report.

---

## Fix Ticket for a Change Review

Accepted Change Review Findings never go back into a finished Ticket. They become fix tasks, and all fix tasks of one Change Review go into **one new fix Ticket** ([tickets.md](tickets.md) section 2):

1. For each accepted Finding, append a fix task to the Task Breakdown of `tasks.md`: `#### T<n>: Fix CR1-F3 <short title>`, with a **`**Fixes**` field naming its Finding** (`**Fixes**: CR1-F3`). The normal `Tests`, `Scenarios` and `Gate` fields apply.
2. Append one Ticket at the end of `## Tickets`, with the next free `K` number, named after the review: `### K<n>: Fix CR<r>`. Its `**Tasks**` field lists every fix task of this review. Its `**Blocked by**` field names the Tickets it repairs, and its `**Covers**` field names the Scenarios it repairs.
3. Add a phase for the fix Ticket to the Execution Plan and run `python3 <skill-dir>/scripts/validate_tasks.py <feature>`.

Example: `tasks.md` has Tickets `K1` to `K3`, and the human accepted `CR1-F1` and `CR1-F2`. You append `T9: Fix CR1-F1 null total` with `**Fixes**: CR1-F1` and `T10: Fix CR1-F2 wrong rounding` with `**Fixes**: CR1-F2`, and the new Ticket `### K4: Fix CR1`, whose `**Tasks**` field reads `T9, T10`.

One review, one fix Ticket: a second Change Review adds its own (`Fix CR2`). Verifier rounds get their own fix Tickets the same way ([implement.md](implement.md) step 9). Building the fix Ticket still needs Execution Approval.

---

## Publishing Tickets needs a dispositioned Spec Review

Tickets are published to the tracker only when the human explicitly says "publish tickets", and only when a Spec Review exists and every Finding of the latest one has a Disposition. If no Spec Review exists, or a Finding is still `_(pending)_`, refuse, say why, and list the pending Findings. Recording Dispositions never publishes anything, and neither does Execution Approval. The procedure is in [tickets.md](tickets.md) section 3.

---

## If a reviewer touched more than its report

Reviewers may write only their own report file. After each review, check `git status`. If anything else changed, tell the human exactly which paths changed and the commit to restore them from (the pre-review commit for a Spec Review, `HEAD` for a Change Review). Do not restore anything without the human's go-ahead.
