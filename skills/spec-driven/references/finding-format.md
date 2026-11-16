# Review Report Format

Both reviewers write one new file per run, using this layout. A Finding must stand on its own: someone reading it weeks later, without the reviewer, can check it and decide. There is no overall verdict; the human's Dispositions are the verdict.

````markdown
# Spec Review SR2 · <feature>            <!-- or: # Change Review CR1 · <feature or branch> -->

- **Reviewed**: commit `abc1234`          <!-- Change Review: `base...head` -->
- **Inputs read**: spec.md, design.md, tasks.md, `.specs/decisions/csv-export.md` (D-csv-export.1 to .9), `.specs/decisions/money.md` (D-money.1), spec-review-1.md    <!-- name every Grilling Record and legacy decision source you read -->
- **Outside sources**: `docs/rfcs/0007-ledger.md`    <!-- planning material from other flows that discovery found and that bears on this review; or: none -->
- **Evidence**: graph refreshed 2026-10-09 14:02 · Sonar: analysis 2026-10-09 13:40 of `shop-api` (current) · Scenario check: 0 errors
- **Reviewer Lessons applied**: L-004 (1 Finding suppressed)    <!-- or: none -->

## Dimensions

| Dimension | Status | Findings |
| --- | --- | --- |
| Functional Correctness | assessed | 1 |
| Practical Judgment | assessed | 0 |
| Thought Partnership | assessed | 1 |
| Verification | assessed | 2 |
| Engineering Craft | assessed | 1 |
| Truthful Reporting | assessed | 0 |
| Communication | assessed | 0 |
| Production Risk | assessed | 1 |

<!-- Status is one of: assessed · not assessable (<why>) · unverified (<why>) -->

## Previous run

| Finding | Disposition | Now |
| --- | --- | --- |
| SR1-F2 | accept | resolved: design.md "Components" now reuses `Money.from_str` |
| SR1-F4 | reject: card data never stored | not re-raised |

<!-- or: "First run." -->

## Findings

### SR2-F1 · Webhook acknowledged before the event is persisted
- **Dimension**: Production Risk · **Severity**: Blocker · **Confidence**: high
- **Where**: `src/webhooks/stripe.py:42-58`; Spec `PAY-03`, Scenario `PAY-03.S1`
- **Problem**: The handler returns 200 before it writes the event to the outbox.
- **Evidence**:
  - `stripe.py:47` `return Response(200)` runs before `outbox.save(event)` at `:55`
  - `graphify path "handle_webhook" "save"`: the only path runs after the return
  - Sonar: no rule covers ordering
- **Failure scenario**: DB timeout at `:55` → Stripe sees 200, never retries → the payment update is lost for good.
- **Recommendation**: Persist to the outbox first, then acknowledge; process asynchronously with internal retries.
- **Would change my mind**: proof that middleware writes the outbox before this handler runs.
- **Disposition**: _(pending)_
````

## Rules

- **IDs** carry the run: `SR<n>-F<k>` for Spec Reviews, `CR<n>-F<k>` for Change Reviews. Never reuse an ID.
- **Order** Findings Blocker first, then Major, Minor, Cosmetic.
- **Severity**:
  - **Blocker**: data loss, security or privacy exposure, wrong money or state, a Redundant Feature, or a flaw that invalidates the plan.
  - **Major**: wrong behavior in a plausible case, a missing failure-mode test, an Implementation-Coupled Test on core logic, a Semantic Duplicate of non-trivial logic, a false Claim.
  - **Minor**: a Smell Baseline judgment call, a local duplicate, unclear naming, a small gap.
  - **Cosmetic**: wording and format.
- **Confidence**: `high` when you read the code or ran the query that proves it; `medium` when one link is inferred; `low` when it is a suspicion. A low-confidence Finding names the check that would settle it.
- **Evidence** is quoted, located (`file:line`, Spec ID, Scenario ID, query and result, Sonar rule and issue key) and reproducible. No location, no Finding.
- **Decisions are cited by ID.** A Finding about a Decision names it by its ID (`D-csv-export.3`) and the Grilling Record that holds it, in **Where**. A Finding that the plan dropped or contradicts an answer cites both places: the Session path question in the record and the Spec criterion. A Finding that a Change contradicts a Decision cites the Decision ID and the code's `file:line`. A decision from a legacy decision source is cited by its file name or its entry number.
- **Inputs read** lists the Grilling Records and legacy decision sources you opened through the read rule ([decisions.md](decisions.md)), so the human can see what the review was judged against.
- **Would change my mind** names one checkable fact. It is the target when the human grills the Finding.
- **Disposition** stays `_(pending)_`. Only the main session edits it, after the human decides: `accept` or `reject: <reason>`, plus an optional `**Grill notes**:` line. When an accepted Finding changes a Decision, the main session also rewrites that Decision in its Grilling Record ([review.md](review.md)); the reviewer never edits a record.
- **The report path** is the one the Review context names. For a feature it is inside the feature folder; for a foreign plan it is `.specs/reviews/<plan slug>/spec-review-<n>.md`, and the plan itself is never edited.
- A dimension you could not assess is marked `not assessable (<why>)`, never left out and never guessed.

## Final message to the main session

After writing the file, return only this:

```markdown
## Spec Review SR2 · <feature>: 4 Findings (1 Blocker, 2 Major, 1 Minor)

Report: `.specs/features/<feature>/spec-review-2.md`

| ID | Severity | Dimension | Finding |
| --- | --- | --- | --- |
| SR2-F1 | Blocker | Production Risk | Webhook acknowledged before the event is persisted |
| ... | | | |

Not assessable: <dimensions and why, or "none">.
Next: the main session collects Dispositions per `references/review.md`.
```
