# Spec Review SR1 · integrate-skills

- **Reviewed**: commit `23a89b3`
- **Inputs read**: spec.md, design.md, tasks.md, `.specs/decisions/0001-integrate-grill-into-spec-driven.md`, `.specs/decisions/summary.md`, `CONTEXT.md`, legacy `docs/adr/0001`-`0003` (no `.specs/STATE.md`, no `context.md`)
- **Evidence**: graph refreshed 2026-11-04 14:42 (1016 nodes, 1386 edges) · Sonar: not used (nothing built) · Structural checks: `validate_spec.py` 1 error (the renamed section, expected per the spec's Assumptions table), `validate_tasks.py` 0 errors / 15 warnings
- **Reviewer Lessons applied**: none (no lessons store)

## Dimensions

| Dimension | Status | Findings |
| --- | --- | --- |
| Functional Correctness | not assessable (nothing built yet) | 0 |
| Practical Judgment | assessed | 2 |
| Thought Partnership | assessed | 1 |
| Verification | assessed | 3 |
| Engineering Craft | assessed | 1 |
| Truthful Reporting | assessed | 1 |
| Communication | assessed | 1 |
| Production Risk | assessed | 2 |

## Previous run

First run.

## Findings

### SR1-F1 · 30 of 44 Scenarios rely on a UAT proof that the gates this plan runs under reject
- **Dimension**: Verification · **Severity**: Major · **Confidence**: high
- **Where**: `tasks.md:30` (matrix `uat` row), Tasks T7-T9, T11-T14, T17-T23; Grilling Record D-0001.30; `skills/spec-driven/references/implement.md:123-125`; `skills/spec-driven/references/validate.md:35`
- **Problem**: Every agent-behavior Scenario (30 of 44) is to be proven by "an interactive UAT walkthrough the Verifier records in `validation.md`" (D-0001.30). No task builds that mechanism. The Execute and Verifier rules this feature runs under treat a Scenario without a test as a failure. Several UAT Scenarios are also assigned to tasks that cannot exercise them yet.
- **Evidence**:
  - `implement.md:123-125`: the mandatory Gate Check runs `validate_scenarios.py <feature> --only <this task's Scenario IDs> --since HEAD`, which "fails when a Scenario has no test", and "Non-zero exit code = STOP". 14 tasks (T7, T8, T9, T11-T14, T17-T23) have `Tests: uat`, list Scenario IDs, and write no test file.
  - `validate.md:35`: the Verifier runs `validate_scenarios.py <feature> --since <diff base>` without `--only`, and "Any error (Scenario without a test ...) is a gap". That gives 30 gaps, so the verdict is FAIL. `implement.md:349` caps the loop at 3 fix iterations. `prep_review.py:363` runs the same check for `/code-review`, and `prep_change` stops on a FAIL verdict.
  - The existing UAT (`validate.md:18,136-146`) covers user-facing features and runs interactively with the human ("present one test at a time ... Wait for user response"). The Verifier is a sub-agent. No task changes `validate.md`, `implement.md` step 3 or `validate_scenarios.py`. `tasks.md:11` lists where this plan overrides the installed skill (Tickets, Decisions & Assumptions, `context.md`), and this conflict is not on that list.
  - Legacy `docs/adr/0002`, which `spec.md:45` treats as a Repo Standard: "`validate_scenarios.py` cross-checks tests against Scenarios: missing tests, ...".
  - Assignment: GRILL-01.S1-GRILL-03.S1 (T7) and REC-01.S1-REC-04.S1 (T8) start with "the user starts/answers Specify", but `specify.md` calls `grilling` only after T11. EDGE-01.S1 and READ-01.S1 (T9) start with "tdd starts a Task", which T18 wires. Ticket K3 (`tasks.md:60-64`) therefore covers Scenarios nobody can demonstrate until K4 or K5, which breaks D-0001.23's "demoable alone".
  - No task creates the UAT fixture repositories the Scenarios assume (an orders CSV exporter at `src/export/csv.py`, `docs/adr/0001-postgres.md`, a local-markdown tracker).
- **Failure scenario**: T7 is done. Its gate runs `validate_scenarios.py integrate-skills --only GRILL-01.S1,GRILL-02.S1,GRILL-03.S1` and exits 1 because no test proves them, so the executor must STOP or quietly skip a mandatory gate. After T25 the Verifier reports 30 gaps and a FAIL verdict. The three fix iterations cannot add tests for prose, so the run escalates, and `/code-review` refuses because `validation.md` says FAIL.
- **Recommendation**: The human decides how an agent-behavior Scenario is proven, and a task in K1 or K2 builds that before K3. One option is a recorded-UAT proof: `validation.md` UAT rows carry the Scenario ID and the observed transcript excerpt, `validate_scenarios.py` accepts them for Scenarios the matrix marks `uat`, and `implement.md` step 3 and `validate.md` §2/§7 change to match. Also add a task that builds the UAT fixture repository. Move each UAT Scenario to the task that wires its behavior (GRILL-01..03, REC-01..04, READ-02/03 to T11; READ-01 and EDGE-01 to T18) and re-slice the Tickets to match.
- **Would change my mind**: a spec-driven rule, in `implement.md` or `validate.md`, that already exempts UAT-proven Scenarios from `validate_scenarios.py`'s missing-proof check.
- **Disposition**: accept
- **Grill notes**: Scenarios a unit test cannot prove (markdown prompts, IaC, config) get proof type `inspect` (default `test`) in the matrix and on the Task; the per-Task gate excludes inspect IDs; the existing Verifier inspects each one and writes a validation.md row (ID, PASS/FAIL, file:line, one-sentence reason; IaC may cite command output); validate_scenarios.py accepts a PASS row as proof. Replaces manual UAT; no fixture repo. Inspection proves the text, not model obedience (accepted gap). New K1 Task builds the mechanism. Move GRILL-01..03, REC-01..04, READ-02/03 to T11; READ-01, EDGE-01 to T18; re-slice K3/K4 so each Ticket demos alone.

### SR1-F2 · Plans written under the old rules break, and their `context.md` decisions stop being read
- **Dimension**: Practical Judgment · **Severity**: Major · **Confidence**: high
- **Where**: Spec `GRILL-05.S2`, `REV-02.S1`; Task T3, T11; Grilling Record D-0001.17, D-0001.20
- **Problem**: The plan changes the plan shape every validator and reviewer expects, but has no rule for features planned under the old rules. Their specs fail `validate_spec.py` (GRILL-05.S2 makes this deliberate) and their `tasks.md` files fail `validate_tasks.py` because `## Tickets` becomes required. Their per-feature `context.md`, which holds the locked gray-area decisions, is no longer read by anyone.
- **Evidence**:
  - `spec.md:184-190` (GRILL-05.S2: the old heading exits 1); `tasks.md:175` (T3 adds `Tickets` to the required sections); `design.md:109`.
  - `spec.md:402-411` (REV-02.S1: "the demo feature folder still contains an old context.md ... output does not mention context.md"); `tasks.md:351` (T11: "no reference in `skills/spec-driven/` points at ... `context.md`").
  - Grilling Record line 307 (D-0001.17): the legacy check covers `docs/adr/` and `STATE.md ## Decisions` only. Line 330 (D-0001.20) calls `context.md` "legacy only", but no consumer's legacy list contains it.
  - Today `skills/spec-driven/references/design.md:11,192` says to load `context.md` if it exists, because "decisions there are locked".
  - `~/Projects/interest-rate-project`, which the Grilling Record cites at line 19: all 10 features under `.specs/features/` have `context.md` and an `Assumptions & Open Questions` heading. The sampled `tasks.md` files (01, 03, 06) have no `## Tickets`. `validation.md` for 04, 08, 09 and 10 holds FAIL verdict lines, so fix work on them is still pending.
  - Out of Scope (`spec.md:64-65`) excludes migrating ADRs and `AD-NNN` entries and editing that repo. It does not say how the new skills treat its plans.
- **Failure scenario**: After install, the user resumes fixes on `09-validation-suite`. Design and Execute no longer load its `context.md`, so a fix contradicts a locked decision there. `/spec-review` on the amended plan shows `missing required section: ## Decisions & Assumptions`, `missing required section: ## Tickets` and an orphan-task error for every task, and the reviewer never sees `context.md`. Any in-flight feature in a work repo hits the same.
- **Recommendation**: Add a transition rule with a Scenario. One option: a feature folder that has `context.md`, or a spec with no `**Grilling Record**:` line, is a legacy plan. The validators downgrade the heading and Tickets checks to WARN for it, and the read rule and REV-02 list its `context.md` as a legacy source. The other option is migrate-on-touch: the first spec-driven phase that touches a legacy feature converts `context.md` into Decisions & Assumptions rows and adds Tickets. The human should choose, since GRILL-05.S2 currently locks in the breaking behavior.
- **Would change my mind**: no repository the user works in has a spec-driven feature that is unfinished or will get fixes after this change.
- **Disposition**: accept
- **Grill notes**: three plan kinds. Native (spec has `**Grilling Record**:` line): full checks. Legacy spec-driven (.specs/features/<f>/spec.md without that line, or context.md present): heading and Tickets checks downgrade to WARN; context.md is a legacy decision source in the read rule and prep_review. Foreign (any other plan: teammate PRD, docs/ design doc, other tool's spec folder, ticket): no structural validators; content read as decision/requirement source; fd discovery notes foreign plan folders in the record Context; /spec-review <path> skips validators with reason, report in .specs/reviews/, foreign files never edited. Building from a foreign plan: Specify uses it as input, grills only the gaps, writes a native spec that links the source (commit or date) without copying it. New Scenarios prove each kind.

### SR1-F3 · Record numbers and `summary.md` rows collide when two branches plan at once
- **Dimension**: Production Risk · **Severity**: Major · **Confidence**: high
- **Where**: Spec `REC-01`, `REC-01.S1`; Grilling Record D-0001.7, D-0001.29 item 2
- **Problem**: A record's number is "one above the highest existing record" in the working tree (REC-01). Every feature grill now writes a record and a `summary.md` row (D-0001.7). In a shared repo, two branches planned at the same time pick the same number, and both add a row at the same place in the single `summary.md` table. The numbering rule is an agent default (D-0001.29 item 2) that nobody asked about.
- **Evidence**:
  - `spec.md:233-241` (REC-01, REC-01.S1). Grilling Record line 386 (D-0001.29 item 2, `Decided by: agent`). Line 247 (D-0001.7: every feature grill writes a record, and `D-NNNN.k` is used in both the record and the spec).
  - Shared team repos are a stated target: Grilling Record line 29; `spec.md:333` ("As a developer on a large team repository").
  - The same scheme rarely collided before, because ADRs were rare: `skills/domain-modeling/SKILL.md:66-68` says "Only offer to create an ADR when all three are true". After D-0001.7, every feature claims a number.
  - `.specs/decisions/summary.md` is one table, and new rows land just above `## Legacy decision paths`. No Scenario or Edge Case covers concurrent branches.
- **Failure scenario**: Two developers branch from `main`, where the highest record is 0003, and run Specify. Both write `0004-*.md` with `D-0004.1..k` and link those anchors from their specs. The second merge conflicts in `summary.md` (fixable by hand), but the two `0004` files merge silently. From then on, "D-0004.3" in reviews, Amendments (REC-05: "superseded by D-0004.7") and `summary.md` Status cells names two different Decisions. A later supersession can mark the wrong record, and READ-01's filter then reads the wrong Status.
- **Recommendation**: Put the ID scheme to the human. Options: (a) collision-free IDs, such as the slug or a timestamp (`D-<slug>.k`); (b) keep `NNNN` and add a rule with a Scenario: on rebase or merge, a record whose number already exists on the target branch is renumbered, along with its D-IDs and the spec and design links; (c) keep `summary.md` rows sorted by File so concurrent additions rarely touch the same lines.
- **Would change my mind**: the user confirms that the shared work repos never have two features planned in parallel on separate branches.
- **Disposition**: accept
- **Grill notes**: chose slug-based names. Record file `.specs/decisions/<slug>.md`, Decision IDs `D-<slug>.k`; slug 2-4 words, must be unique in decisions/ (agent checks at creation); same slug on two branches gives a loud add/add conflict. Date moves to record header and a new `Date` column in summary.md; rows sorted by date then file. Rename 0001 to `grill-in-spec-driven` (IDs D-grill-in-spec-driven.k). Rejected NNNN-with-renumber-on-merge and timestamp IDs.

### SR1-F4 · Publishing Tickets has no rule for re-runs, mid-way tracker failures or a missing Spec Review
- **Dimension**: Production Risk · **Severity**: Major · **Confidence**: high
- **Where**: Spec `TKT-06`, `TKT-07`; Grilling Record D-0001.25; `design.md:172-179`
- **Problem**: TKT-06 creates "one tracker issue per Ticket" every time the user says "publish tickets", through an external CLI. The spec does not say what happens when some Tickets already carry a Tracker ID (a second publish, or a retry after a failure), when the tracker call fails after K1 is created, or when no Spec Review exists. This is an outward-facing write the product team sees.
- **Evidence**:
  - `spec.md:520-530`: TKT-06.S1 covers only the happy path. `spec.md:532-540`: TKT-07 covers only pending Findings.
  - Grilling Record line 360 (D-0001.25): the drift rule applies only "when amendments later change a published Ticket".
  - `design.md:172-179` Error Handling has one publishing row, for pending Dispositions.
  - The reused sources have no failure or duplicate handling either: `skills/to-tickets/SKILL.md:60-63` (one issue per ticket, in dependency order) and `skills/setup-matt-pocock-skills/issue-tracker-github.md` (`gh issue create`). `rg -i "duplicate|already|retry|fail"` over `issue-tracker-*.md` finds nothing.
  - The precondition "every Finding of the latest Spec Review has a Disposition" is vacuously true when no `spec-review-<n>.md` exists. D-0001.25 implies a review must exist first.
- **Failure scenario**: `gh issue create` succeeds for K1 and K2 and then fails on K3 because the token expired. The user says "publish tickets" again. Read literally, TKT-06 creates K1 and K2 a second time, so the tracker holds duplicates and K3's Blocked-by edges point at one of each pair. Separately, a user who says "publish tickets" before ever running `/spec-review` passes the precondition.
- **Recommendation**: Extend TKT-06 and TKT-07, with a Scenario for each rule. Tickets that already have a Tracker ID are skipped, or diffed per D-0001.25. Each ID is written to `tasks.md` right after its issue is created, so a failure leaves a state that can be resumed. A tracker failure stops publishing and reports which Tickets were published. Publishing requires at least one Spec Review.
- **Would change my mind**: a rule in the text T14 reuses that already skips Tickets carrying an ID and writes each ID back as soon as the issue exists.
- **Disposition**: accept
- **Grill notes**: four rules, each with a Scenario: (1) write each Tracker ID to tasks.md right after its issue is created; (2) a Ticket with a Tracker ID is never re-created, changed content goes through the D-0001.25 drift rule with confirmation; (3) a tracker failure stops publishing and reports published vs unpublished, re-running resumes at the first unpublished Ticket; (4) publishing requires at least one Spec Review with all Findings of the latest one disposed.

### SR1-F5 · This Large spec skipped the mandatory implicit-requirement sweep
- **Dimension**: Thought Partnership · **Severity**: Major · **Confidence**: high
- **Where**: `spec.md` (no sweep anywhere); Grilling Record Session path Q1-Q30, D-0001.15, D-0001.16, D-0001.29 item 1
- **Problem**: `specify.md` requires a Large spec to resolve every implicit-requirement dimension to a requirement or an explicit `N/A because ...`. D-0001.29 item 1 keeps that sweep as the grill's closing branches. This spec has no sweep: no `N/A` lines and no failure-mode criterion. Neither the Session path nor the ten defaults at the shared-understanding check contains a sweep branch. SR1-F3 (concurrency) and SR1-F4 (external-dependency failure, idempotency) are two dimensions the sweep would have caught, and others are still open.
- **Evidence**:
  - `skills/spec-driven/references/specify.md:52-58` (Large: "Cover every dimension ... No blank entries allowed"); Grilling Record line 385 (D-0001.29 item 1).
  - `grep -n -i "N/A\|concurren\|idempot\|partial\|retry\|rollback\|crash"` over spec.md and design.md finds nothing. The Grilling Record matches only at line 272.
  - State-transition integrity: cross-file supersession is decided (line 295: "A later feature superseding a Decision writes its own record, with cross-file supersession"; line 301: "Superseding another record's Decision also updates that record and its `summary.md` row") but has no criterion or Scenario. REC-05 (`spec.md:273-283`) covers only an Amendment inside the same file. READ-01 (`spec.md:339-347`) relies on `summary.md` Status to skip superseded records.
  - Input validation: no criterion says what a consumer does with a `summary.md` row it cannot parse, or a row whose File does not exist.
- **Failure scenario**: Feature B's Design supersedes D-0001.18 but writes only its own record, so record 0001's `summary.md` row stays `active`. Every consumer keeps reading D-0001.18 as a Repo Standard (D-0001.17), and the change-reviewer then flags B's code for contradicting an "active" Decision (REV-06).
- **Recommendation**: Run the sweep now as closing branches, one question each per D-0001.2. Record each dimension as a criterion with a Scenario or as `N/A because ...`. At minimum, add a cross-file supersession criterion with a Scenario (the old record is marked and its `summary.md` row updated), plus whatever SR1-F3 and SR1-F4 settle.
- **Would change my mind**: a sweep for this feature, with each dimension resolved, that exists elsewhere and was simply not copied into spec.md.
- **Disposition**: accept
- **Grill notes**: sweep run now, every dimension resolved. Concurrency: F3. Idempotency/retry: F4. External dependency: F4 rule 3, missing fd pause-and-ask, missing graphify falls back to rg. State transition: add criterion + Scenario for cross-file supersession (old record and its summary.md row marked). Auth/rate limits: N/A, no service, tracker auth is the user's CLI login. Observability: N/A, records and validation.md are the audit trail. Data lifecycle: records never deleted, superseded kept, read rule filters by Status. Partial failure: record created at Q1 with Status draft, updated after each answer, resumed from Session path; summary.md row only at finish; consumers ignore drafts. Input validation: broken/missing summary.md row warns and falls back to listing .specs/decisions/*.md and reading each header; header is source of truth, summary.md is an index.

### SR1-F6 · Fix tasks have no Ticket, so the new Ticket check fails on every fix cycle
- **Dimension**: Engineering Craft · **Severity**: Major · **Confidence**: high
- **Where**: Spec `TKT-03`; Task T3, T17, T19; `skills/spec-driven/references/review.md:41`; `validate.md:16`
- **Problem**: TKT-03 makes "every task in exactly one Ticket" a hard validator error. Two existing flows append tasks without a Ticket: Change Review fixes and Verifier gaps. The tasks that rewrite those references (T17 `implement.md`, T19 `review.md`) say nothing about where fix tasks go. D-0001.25 also doesn't say whether fix work on a published Ticket reopens it, extends it, or becomes a new Ticket.
- **Evidence**:
  - `spec.md:490-498` (TKT-03); `tasks.md:175` (T3).
  - `review.md:41`: "turn each accepted Finding into a fix task appended to `tasks.md` (`### T<n>: Fix CR1-F3 <short title>` ...)". `validate.md:16` and `implement.md:349`: "Gaps become fix tasks".
  - T17's What (`tasks.md:466`) and T19's What (`tasks.md:506`) cover neither flow. `CONTEXT.md:20` now defines a Task as "inside exactly one Ticket".
  - `tasks.md:39-40`: the `plan` gate, which runs `validate_tasks.py`, is part of `full` for every task after T3.
- **Failure scenario**: In this very feature, the Verifier finds a gap after T25 and a fix task T26 is appended in the existing format. T26's `full` gate runs `validate_tasks.py`, which reports T26 is in no Ticket, exits 1, and the task STOPs. In other repos the same error appears at the next `/spec-review`, and the product team's tracker never shows the fix work.
- **Recommendation**: Decide where fix tasks live, for example one new Ticket per review or Verifier round (`### K<n>: Fix CR1`), Blocked by the Ticket it repairs and published only on a go-ahead. Write that into `review.md` step 7 and the Verifier fix flow (T17, T19). Add a validator Scenario in which a `tasks.md` with an appended fix task inside a fix Ticket passes.
- **Would change my mind**: a rule in the plan that exempts fix tasks from the Ticket check, for example the validator skipping tasks that have a `**Fixes**` field.
- **Disposition**: accept
- **Grill notes**: one fix Ticket per Change Review or Verifier round that produces fixes (`### K<n>: Fix CR1`, `### K<n>: Fix Verifier round 2`), Blocked by the Tickets it repairs, Covers the Scenarios it repairs, published only on "publish tickets" under the F4 rules. Written into review.md step 7 and the Verifier fix flow (T17, T19); validator Scenario: appended fix task inside a fix Ticket passes.

### SR1-F7 · Multi-context repos lose context-scoped decisions and block the review snapshot
- **Dimension**: Practical Judgment · **Severity**: Major · **Confidence**: medium
- **Where**: Grilling Record D-0001.13, D-0001.17, D-0001.18; Spec `REC-07`, `EDGE-01`, `REV-01`; `design.md:110`
- **Problem**: D-0001.13 keeps the multi-context layout that domain-modeling writes today: a root `CONTEXT-MAP.md`, a `CONTEXT.md` per context, and a `docs/adr/` per context. The new read rule checks only the root `docs/adr/` as a legacy path. Discovery stops at depth 3, and `src/<ctx>/docs/adr` is depth 4. prep_review's snapshot adds only the root `CONTEXT.md`. In the large repos the READ story targets, context-scoped decisions can be skipped silently, and a grill that edits a per-context glossary blocks `/spec-review`.
- **Evidence**:
  - `skills/domain-modeling/SKILL.md:24-38`: the layout includes `src/ordering/docs/adr/ ← context-specific decisions`.
  - `skills/setup-matt-pocock-skills/domain.md:9`: today's read rule says "In multi-context repos, also check `src/<context>/docs/adr/`".
  - Grilling Record line 283 (D-0001.13 keeps the layout); line 307 (D-0001.17's legacy check covers `docs/adr/` and `STATE.md` only); lines 315-316 (`--max-depth 3`). `spec.md:295` (REC-07) and `spec.md:618` (EDGE-01) name only the root `docs/adr/`.
  - `design.md:110` and `spec.md:391-399` (REV-01: `CONTEXT.md` only). `prep_review.py:212-216`: any dirty path outside the plan list raises `Stop`.
- **Failure scenario**: A work repo has `CONTEXT-MAP.md` and `src/billing/docs/adr/0002-integer-cents.md`. tdd starts a Task in `src/billing/`. Discovery lists `src/billing/docs/`, but nothing tells the agent to open it, and the legacy check looks only at `docs/adr/`, so the integer-cents decision is never read. Separately, Specify updates `src/billing/CONTEXT.md`, and `/spec-review` stops with "uncommitted changes outside the plan ... src/billing/CONTEXT.md".
- **Recommendation**: Make the legacy check and the snapshot follow the glossary layout. When `CONTEXT-MAP.md` exists, check every `docs/adr/` it points to (or every `*/docs/adr/` found with `fd -t d adr`). Add `CONTEXT-MAP.md` and every `CONTEXT.md` to prep_review's plan paths. Extend EDGE-01 and REV-01 with a multi-context Scenario.
- **Would change my mind**: none of the user's repos, work repos included, uses `CONTEXT-MAP.md` or a per-context `docs/adr/`.
- **Disposition**: accept
- **Grill notes**: new records stay in root .specs/decisions/ scoped by Areas. Legacy check follows CONTEXT-MAP.md to each context's docs/adr/, else one probe `fd -t d -p 'docs/adr$'` at any depth with the same excludes. prep_review treats CONTEXT-MAP.md and every CONTEXT.md as plan files. EDGE-01 and REV-01 gain multi-context Scenarios.

### SR1-F8 · The rewritten Decisions & Assumptions cell check is unspecified for the section's two tables and proven by no Scenario
- **Dimension**: Verification · **Severity**: Minor · **Confidence**: high
- **Where**: `design.md:108`; Task T2; `skills/spec-driven/scripts/validate_spec.py:197-217`; Spec `GRILL-05`, `GRILL-06`
- **Problem**: The renamed section holds two tables with different columns: Decisions (`ID | Decision | Choice | Rationale | Decided by | Binds`) and Assumptions (`Assumption | Chosen default | Rationale | Confirmed?`). The design says only "Choice and Rationale filled". No Scenario covers an empty cell. Today's check drops only the first header row and reads cells by position.
- **Evidence**: the two table headers at `spec.md:77` and `spec.md:113`. `validate_spec.py:203-210`: `data = data[1:]`, then `assumption, chosen, rationale = cells[0], cells[1], cells[2]`. GRILL-05.S1/S2 and GRILL-06.S1 (`spec.md:176-199`) test only that the section exists and that `none` is accepted.
- **Failure scenario**: An implementation reads Choice and Rationale at indexes 2 and 3 for every row. It then reads the Assumptions header as data with no error, and an Assumption row with an empty "Chosen default" passes, although `validate_spec.py:214-215` rejects that row today. All three planned tests and T2's "this spec exits 0" check still pass.
- **Recommendation**: In design.md, state that the check finds each table by its header names and checks Choice and Rationale in the Decisions table and Chosen default and Rationale in the Assumptions table. Add two Scenarios: a Large spec with a Decisions row whose Choice is empty exits 1 and names the row ID; an Assumption row with an empty Chosen default exits 1.
- **Would change my mind**: a design note or Scenario elsewhere in the plan that defines the two-table check.
- **Disposition**: accept
- **Grill notes**: check finds each table by header names; Decisions needs Choice and Rationale, Assumptions needs Chosen default and Rationale; two automated Scenarios in T2 (empty Choice exits 1 naming the row ID; empty Chosen default exits 1).

### SR1-F9 · Automated tests depend on the host's graphify and on a PATH without fd that the plan doesn't build
- **Dimension**: Verification · **Severity**: Minor · **Confidence**: high
- **Where**: `tasks.md:28-29` (Test Coverage Matrix); Tasks T1, T4, T5, T6; Spec `TKT-01.S1`, `READ-04.S1`
- **Problem**: The matrix stubs `graphify` only for the installer. `prep_review.py` exits before any plan check when `graphify` is missing, and runs `graphify update .` inside each fixture. READ-04.S1 needs a PATH without `fd`, but `install.sh` needs `bash` and coreutils from the same `/usr/bin`.
- **Evidence**: `prep_review.py:384-385` calls `ensure_graphify(root)` before `prep_spec`. `:128-131` raises `Stop("graphify is not installed ...")`. `:143-147` runs `[exe, "update", "."]`. `command -v fd cp rm bash` gives `/usr/bin/fd`, `/usr/bin/cp`, `/usr/bin/rm`, `/usr/bin/bash`. TKT-01.S1 expects the STOP output to name `tasks.md` (`spec.md:465-471`).
- **Failure scenario**: On a machine or CI runner without graphify, TKT-01.S1, TKT-02.S1/S2, REV-01.S1 and REV-02.S1 fail with "STOP: graphify is not installed". On this machine they pass but build a real graph in every test. A READ-04.S1 test that removes `/usr/bin` from PATH loses `bash` and `cp`, so `install.sh` fails before it reaches the fd check.
- **Recommendation**: T1's helper puts a stub `graphify` first on PATH for the prep_review tests (exit 0, printing `0 nodes, 0 edges`). For READ-04.S1 it builds a bin directory of symlinks to `node`, `bash` and the coreutils `install.sh` uses, without `fd`. Name both in the matrix.
- **Would change my mind**: the human intends these tests to require a real graphify and accepts that.
- **Disposition**: reject: tests require the real graphify (no stub), and the fd-missing check becomes an inspect Scenario with no automated test
- **Grill notes**: new project rule + criterion + inspect Scenario: graphify-out/ is the graph cache, often gitignored or in .git/info/exclude; ignored does not mean disposable; never delete or clean it; refresh with `graphify update .` (text in SKILL.md and standards.md §4). fd half: READ-04.S1 becomes `inspect` (Verifier reads install.sh), no automated test, no PATH tricks.

### SR1-F10 · The plan leaves two routes to implementation outside spec-driven, yet its Goal claims zero
- **Dimension**: Truthful Reporting · **Severity**: Minor · **Confidence**: high
- **Where**: `spec.md:57` (Goal), `spec.md:692-695` (Success Criteria); `skills/prototype/SKILL.md:26`; Task T14
- **Problem**: The Goal "0 installed skills offer an implementation path outside spec-driven" is not met. `prototype` stays installed and model-invocable, and it tells the agent to "Fold any validated decision into the real code". The text T14 reuses labels published Tickets `ready-for-agent`, "agent-grabbable by construction". The Success Criteria check only the retired skills, so the Goal would be reported as met.
- **Evidence**: `skills/prototype/SKILL.md:26` (rule 6). Its frontmatter (lines 1-4) has no `disable-model-invocation`, and no task touches `skills/prototype/`. `skills/to-tickets/SKILL.md:63`: "Apply the `ready-for-agent` triage label ... the tickets are agent-grabbable by construction". T14 reuses "to-tickets sections 3 and 5" (`tasks.md:407`).
- **Failure scenario**: A prototype session validates a state model and folds it into `src/` with no Spec, no review and no Execution Approval. Or a teammate's agent picks a `ready-for-agent` Ticket off the tracker and implements it directly.
- **Recommendation**: Add a task that makes `prototype` hand the validated decision to Specify, as T22 does for `diagnosing-bugs`, and have T14 drop the `ready-for-agent` label and the "agent-grabbable" wording. Alternatively, narrow the Goal and record `prototype` as an accepted exception.
- **Would change my mind**: the human does not consider prototype's "fold into the real code" step an implementation path.
- **Disposition**: accept
- **Grill notes**: prototype rule 6 changes to "record what the prototype proved, then start Specify with it" (prototype branch kept as evidence), new K6 Task; T14 drops the ready-for-agent label and "agent-grabbable" wording, each published Ticket says it is built through its Spec and links it.

### SR1-F11 · D-0001.29 bundles nine Decisions under one ID, which Amendments cannot supersede one at a time
- **Dimension**: Communication · **Severity**: Minor · **Confidence**: high
- **Where**: Grilling Record lines 383-396 (D-0001.29); `spec.md:107`; Task T8
- **Problem**: D-0001.29 holds nine separate choices under one Decision ID. Its one trade-off line ("none of them was grilled individually") describes the process, not a trade-off. Amendments supersede whole Decisions (REC-05), so accepting a Finding about one item (SR1-F3 targets item 2) means either superseding all nine or inventing a sub-ID the `D-NNNN.k` scheme doesn't define. T8 uses this record as the worked example for the new template, so the template would teach the bundle.
- **Evidence**: Grilling Record lines 383-396; line 247 (D-0001.7: one ID per Decision, `D-NNNN.k`). `spec.md:273-283` (REC-05: "D-0004.3 reads superseded by D-0004.7"). `spec.md:432` (REV-05 flags a Decision that "lacks a trade-off"). `tasks.md:283` (T8 reuses this record "as the worked example").
- **Failure scenario**: The human accepts SR1-F3. The Amendment must mark D-0001.29 superseded, which also retires the other eight defaults (the sweep rule, the validators, `install.sh`, `STATE.md`, ...), or else write an ad-hoc "D-0001.29.2" that `summary.md` Status cells and reviewers have no rule for.
- **Recommendation**: Split D-0001.29 into nine Decisions, each with its own trade-off, Binds and `Decided by: agent`, before T8 copies the record as its example.
- **Would change my mind**: a plan for GRILLING-RECORD-FORMAT.md to define sub-IDs (`D-NNNN.k.m`) that Amendments and `summary.md` Status cells can name.
- **Disposition**: accept
- **Grill notes**: user replaced supersession with in-place rewriting (git keeps history): no superseded status (summary.md Status is draft/active only), no Amendments section, a cross-record change edits the original record, Session path never rewritten, rewritten Decision gets a `Changed: <date> by <feature> (<source>)` line. Split D-0001.29 into nine Decisions for readability.
