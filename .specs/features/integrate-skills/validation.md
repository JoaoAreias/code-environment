# Integrate Skills Validation

**Date**: 2026-11-16
**Spec**: `.specs/features/integrate-skills/spec.md`
**Diff range**: `abd3b89..HEAD` (`abd3b89` = last planning commit; HEAD = `232ecc9`, 39 commits). Closest attention on the K8 fix range `8b8776e..HEAD` (5 commits: CR1 dispositions, K8 plan, T32 `e31ed9b`, T33 `7277983`, T34 `232ecc9`).
**Verifier**: independent sub-agent (author ≠ verifier), re-verification after fix Ticket K8 (Fix CR1). Every row below was re-derived from the files at `232ecc9`; nothing was carried over from the previous report.

## Validation: integrate-skills - PASS

All 83 Scenarios are proven: 33 `test` Scenarios by tests whose assertions target the exact Then outcome, 50 `inspect` Scenarios by the final skill, agent and installer text. Every gate exits 0. The discrimination sensor killed 8 of 8 mutants, four of them aimed at the K8 code. K8 broke no earlier Scenario: PLAN-04.S1 to S3 and the GRILL/PLAN validator Scenarios still pass, and the refactored traceability reader is discriminated by four existing tests. Interactive UAT (validate.md section 7) and Lessons distillation (section 10) were skipped on the orchestrator's instruction.

---

## Task Completion

| Task | Status | Notes |
| ---- | ------ | ----- |
| T1-T31 | ✅ Done | unchanged since the previous round; every Done-when box ticked |
| T32 | ✅ Done | `e31ed9b` adds `feature_in_path` (`skills/spec-driven/scripts/prep_review.py:236-244`) and uses it in `foreign_plan` and `prep_spec` |
| T33 | ✅ Done | `7277983` adds `report_slug` with `source.txt` ownership and a SHA-1 suffix (`prep_review.py:315-330`), plus fixture `tests/fixtures/foreign-slug-collide/` |
| T34 | ✅ Done | `232ecc9` reads Requirement Traceability through `scenarios_lib.find_tables` by header (`validate_spec.py:236-263`); `split_row`/`is_separator` are gone |

`tasks.md` has 0 unchecked `[ ]` boxes. K8 lists T32, T33, T34; `validate_tasks.py` exits 0.

---

## Scenario-Anchored Check

One row per Scenario, `test` and `inspect` alike. An `inspect` row cites the `file:line` read and a one-sentence reason in place of a test assertion.

| Scenario | Spec-defined outcome (Then) | `file:line` + assertion | Result |
| -------- | --------------------------- | ----------------------- | ------ |
| GRILL-01.S1 | every agent turn holds exactly one question; every question lists options and marks one recommended | `skills/spec-driven/references/specify.md:76-77` - states "Every turn of yours contains exactly one question" and "Every question lists its options and marks one as recommended"; `skills/grilling/SKILL.md:16-22` says the same | ✅ PASS |
| GRILL-02.S1 | "you decide" gives a Decision choosing the recommended option, reading `Decided by: agent` | `skills/spec-driven/references/specify.md:102` - the recommended option becomes the answer and is recorded as a Decision that reads `Decided by: agent` | ✅ PASS |
| GRILL-03.S1 | next turn lists one default per unasked branch; nothing written to spec.md until the user replies | `skills/spec-driven/references/specify.md:103` - the next turn lists one default for every unasked branch, then "Write nothing to `spec.md` until the user replies" | ✅ PASS |
| GRILL-04.S1 | first message names the existing file as a capability and asks what is needed beyond it before any other question | `skills/spec-driven/references/specify.md:53,69` - step 1.3 searches for a Redundant Feature before any question, and the first message names it by file path and makes "what does the user need beyond it" its one question | ✅ PASS |
| GRILL-05.S1 | exit 1; output names "Decisions & Assumptions" | `tests/test_validate_spec.py:24-26` - `assertEqual(code, 1)`, `assertRegex(out, r"ERROR .*Decisions & Assumptions")`, exactly 1 error | ✅ PASS |
| GRILL-05.S2 | exit 1; output names "Decisions & Assumptions" | `tests/test_validate_spec.py:37-39` - `assertEqual(code, 1)`, `assertRegex(out, r"ERROR .*Decisions & Assumptions")`, exactly 1 error | ✅ PASS |
| GRILL-06.S1 | exit 0 | `tests/test_validate_spec.py:49` - `assertEqual(code, 0, out)` | ✅ PASS |
| GRILL-07.S1 | feature folder has spec.md and no context.md; Decisions row chooses "download, not email" | `skills/spec-driven/references/specify.md:5,155,158` - Specify never writes `context.md`, a choice such as "download, not email" becomes a Decisions row, and the folder gets `spec.md` and nothing else | ✅ PASS |
| GRILL-08.S1 | without a skill-loading tool, the agent reads grilling/SKILL.md beside spec-driven before the first question | `skills/spec-driven/references/specify.md:57` - with no tool to load a skill by name, read `<skill-dir>/../grilling/SKILL.md`, and have read it "before your first question" | ✅ PASS |
| GRILL-09.S1 | exit 1; output names "D-demo.2" | `tests/test_validate_spec.py:60-62` - `assertEqual(code, 1)`, `assertRegex(out, r"ERROR .*D-demo\.2")`, exactly 1 error | ✅ PASS |
| GRILL-09.S2 | exit 1; output names "rows fit in memory" | `tests/test_validate_spec.py:73-75` - `assertEqual(code, 1)`, `assertRegex(out, r"ERROR .*rows fit in memory")`, exactly 1 error | ✅ PASS |
| GRILL-10.S1 | asks each unresolvable dimension; spec lists every dimension with criterion ID or "N/A because" | `skills/spec-driven/references/specify.md:115-121` - Large/Complex go through every dimension, ask each one not resolvable from earlier answers, and the spec lists every dimension with its criterion ID or `N/A because` reason (template table at `:323-335`) | ✅ PASS |
| REC-01.S1 | csv-export.md exists with `Status: draft`; Session path holds the question, options, recommendation and answer | `skills/spec-driven/references/specify.md:107` - at the first answer create `.specs/decisions/<slug>.md` with `Status: draft`, Session path holding the question, its options, the recommendation and the answer; `skills/domain-modeling/GRILLING-RECORD-FORMAT.md:107` agrees | ✅ PASS |
| REC-01.S2 | a record with a different slug; existing csv-export.md unchanged | `skills/spec-driven/references/specify.md:107` - if `<slug>.md` already belongs to other work, create the record under a different slug and leave the existing file unchanged; `GRILLING-RECORD-FORMAT.md:12` agrees | ✅ PASS |
| REC-02.S1 | three answered questions on disk before the fourth question is shown | `skills/spec-driven/references/specify.md:108` - append before the next question; "After the third answer the file holds three answered questions; the fourth question comes after that write" | ✅ PASS |
| REC-03.S1 | header `Status: active`; summary row after billing-retries with all fields; spec rows link D-csv-export anchors | `skills/spec-driven/references/specify.md:144-154` - at confirmation set `Status: active`, add the summary row in Date order with File, Date, 1-2 sentence Summary, Status `active`, Binds, Areas, Specs, before writing `spec.md`, whose rows link `D-<slug>.k` anchors | ✅ PASS |
| REC-04.S1 | five sections; rejected "email the file" listed; every Decision one choice with five fields | `skills/spec-driven/references/specify.md:109-110,146` and `skills/domain-modeling/GRILLING-RECORD-FORMAT.md:17,94-97` - all five sections required, rejected options stay listed, one choice per Decision with Choice, Reason, Trade-off, Binds, Decided by | ✅ PASS |
| REC-05.S1 | D-csv-export.3 chooses Money; Changed line cites spec-review-1 SR1-F2; no Decision reads "superseded" | `skills/spec-driven/references/review.md:56-69,83` - rewrite the Decision's Choice in place, add `Changed` line naming the review and Finding (the same worked example), never mark a Decision replaced; `GRILLING-RECORD-FORMAT.md:118-126` agrees | ✅ PASS |
| REC-05.S2 | D-billing-retries.2 chooses five retries with Changed line naming invoice-pdf; invoice-pdf's record adds no Decision restating it | `skills/spec-driven/references/review.md:71` - the same worked example: rewritten in its original record with a `Changed` line naming `invoice-pdf`, and `invoice-pdf.md` adds no Decision of its own; `GRILLING-RECORD-FORMAT.md:125` agrees | ✅ PASS |
| REC-05.S3 | Review section holds D-csv-export.9 citing SR1-F4 | `skills/spec-driven/references/review.md:73` - a new Decision under `## Review` with the next free ID citing the Finding; the example is exactly D-csv-export.9 citing SR1-F4 | ✅ PASS |
| REC-06.S1 | Design section with D-csv-export.7 choosing streaming; design.md Tech Decisions links it | `skills/spec-driven/references/design.md:92-93,110` - add `## Design` with the next ID (record ending at D-csv-export.6 gets D-csv-export.7), and the `## Tech Decisions` table links each Decision's anchor | ✅ PASS |
| REC-07.S1 | summary.md has legacy lines naming docs/adr/ and .specs/STATE.md | `skills/spec-driven/references/specify.md:149` - when this is the first Grilling Record, create `summary.md` with a line naming `docs/adr/` and one naming `.specs/STATE.md` when it has `## Decisions`; `GRILLING-RECORD-FORMAT.md:160` agrees | ✅ PASS |
| REC-08.S1 | no new file under docs/adr/; no AD entry in STATE.md; Decision in the Grilling Record | `skills/spec-driven/references/design.md:12,108` - a project-binding Decision goes into the record with `Binds: project` and "no new file under `docs/adr/`, no `AD-NNN` entry in `.specs/STATE.md`", even where those exist | ✅ PASS |
| REC-09.S1 | a new Grilling Record exists; its summary row reads Specs "none" | `skills/grill-with-docs/SKILL.md:26-30` - creates the record at the first answer, finishes it at confirmation, adds the summary row whose "Specs cell of that row reads `none`" | ✅ PASS |
| REC-10.S1 | first question is the next unanswered branch after five; no second record | `skills/spec-driven/references/specify.md:61,70` - resume a draft for this feature, take every answer as given, first question is the next unanswered branch, "Do not create another record"; `GRILLING-RECORD-FORMAT.md:109` agrees | ✅ PASS |
| READ-01.S1 | opens billing-rules.md and money.md; not dark-mode.md or billing-ledger.md | `skills/tdd/SKILL.md:21,30` - open exactly the `active` records binding the project with overlapping Areas or `*`, or naming the feature, skip drafts; the worked example is this exact case; `skills/spec-driven/references/decisions.md:46-55` agrees | ✅ PASS |
| READ-02.S1 | names .kiro/specs/payments/ and docs/rfcs/ before the first question; record Context cites the sources | `skills/spec-driven/references/decisions.md:16-17,30,32` - listings use `--no-ignore-vcs` (gitignored paths shown), name outside material by path before the first question, cite used sources in Context; `specify.md:45,68,111` agrees | ✅ PASS |
| READ-03.S1 | first message asks to install fd; no planning question until fd is available | `skills/spec-driven/references/specify.md:44,67` - if `fd` is missing the first message asks to install it "and contains nothing else"; no planning question until available; `decisions.md:34` agrees | ✅ PASS |
| READ-04.S1 | warning naming fd when missing; install continues | `install.sh:86-88` - `if ! command -v fd` prints `WARNING: fd not found ...` and has no `exit`; an `if` condition does not trip `set -e` (`install.sh:6`), so step 5 follows | ✅ PASS |
| READ-05.S1 | warns gone.md missing and billing-rules.md has no row; opens billing-rules.md | `skills/spec-driven/references/specify.md:47` - warn with exactly these two example messages and open an `active` project record with covering Areas even without a row; `decisions.md:61-75` agrees | ✅ PASS |
| READ-06.S1 | graphify-out/graph.json still exists; refreshed only with `graphify update .` | `skills/spec-driven/SKILL.md:39` - Critical Rule 11: never delete, clean or move `graphify-out/` even when gitignored, `graph.json` is still there at phase end, refresh with `graphify update .`; `references/standards.md:117` agrees | ✅ PASS |
| REV-01.S1 | exit 0; HEAD commit contains the three edited paths | `tests/test_prep_review.py:52-53` - `assertEqual(code, 0)`, `assertEqual(sorted(head_paths(repo)), sorted(edited))` with the record, summary and `CONTEXT.md` | ✅ PASS |
| REV-01.S2 | exit 0; HEAD commit contains CONTEXT-MAP.md and src/billing/CONTEXT.md | `tests/test_prep_review.py:68-69` - `assertEqual(code, 0)`, `assertEqual(sorted(head_paths(repo)), sorted(edited))` | ✅ PASS |
| REV-02.S1 | output lists .specs/decisions/demo.md; does not mention context.md | `tests/test_prep_review.py:86-87` - `assertRegex(out, r"(?m)^- Grilling Records: \`\.specs/decisions/demo\.md\`$")`, `assertNotIn("context.md", out)` | ✅ PASS |
| REV-02.S2 | old-demo/context.md listed as legacy decision source | `tests/test_prep_review.py:99` - `assertRegex(out, r"(?m)^- Legacy decision source: \`\.specs/features/old-demo/context\.md\`$")` | ✅ PASS |
| REV-02.S3 | re-demo/context.md listed as legacy decision source | `tests/test_prep_review.py:111` - `assertRegex(out, r"(?m)^- Legacy decision source: \`\.specs/features/re-demo/context\.md\`$")` | ✅ PASS |
| REV-03.S1 | Finding citing the Session path question and the spec criterion | `agents/spec-reviewer.md:50` - go answer by answer through the Session path; a dropped or contradicted answer gets a Finding citing both the question and the criterion ID, with the "download, not email" example | ✅ PASS |
| REV-04.S1 | Thought Partnership Finding naming D-csv-export.5 | `agents/spec-reviewer.md:40` - every `Decided by: agent` Decision that changes behavior, data or cost gets a Thought Partnership Finding naming its ID | ✅ PASS |
| REV-05.S1 | Communication Finding naming D-csv-export.2 | `agents/spec-reviewer.md:52-53` - a Decision whose Trade-off is missing or empty gets a Communication Finding naming it, example `D-csv-export.2` | ✅ PASS |
| REV-05.S2 | Communication Finding naming D-csv-export.4 | `agents/spec-reviewer.md:52,54` - a bundled Decision gets a Communication Finding naming it, example "five unrelated defaults under `D-csv-export.4`" | ✅ PASS |
| REV-06.S1 | Finding citing D-money.1 and the float's file:line | `agents/change-reviewer.md:46-47` - a contradicted, un-rewritten active Decision gets a Finding citing its ID and the contradicting `file:line`, with the D-money.1 float example | ✅ PASS |
| TKT-01.S1 | exit 1; output starts with STOP and names tasks.md | `tests/test_prep_review.py:126-127` - `assertEqual(code, 1)`, `assertRegex(out, r"\ASTOP: .*tasks\.md")` | ✅ PASS |
| TKT-02.S1 | exit 1; output starts with STOP and names design.md | `tests/test_prep_review.py:139-140` - `assertEqual(code, 1)`, `assertRegex(out, r"\ASTOP: .*design\.md")` | ✅ PASS |
| TKT-02.S2 | no STOP message naming design.md | `tests/test_prep_review.py:151-153` - `assertEqual(code, 0)`, `assertNotRegex(out, r"(?m)^STOP")`, review context printed | ✅ PASS |
| TKT-03.S1 | exit 1; output names T2 | `tests/test_validate_tasks.py:24-26` - `assertEqual(code, 1)`, `assertRegex(out, r"ERROR T2\b.*Ticket")`, exactly 1 error | ✅ PASS |
| TKT-03.S2 | exit 0 | `tests/test_validate_tasks.py:37` - `assertEqual(code, 0, out)` | ✅ PASS |
| TKT-04.S1 | exit 1; output names T2, K1 and K2 | `tests/test_validate_tasks.py:48-50` - `assertEqual(code, 1)`, `assertRegex(out, r"ERROR T2\b.*\bK1\b.*\bK2\b")`, exactly 1 error | ✅ PASS |
| TKT-05.S1 | exit 1; output names K1 and K2 | `tests/test_validate_tasks.py:61-63` - `assertEqual(code, 1)`, `assertRegex(out, r"ERROR K1\b.*\bK2\b")`, exactly 1 error | ✅ PASS |
| TKT-06.S1 | one issue for K1 then K2; both Tickets name their IDs; each issue links the spec, no ready-for-agent label | `skills/spec-driven/references/tickets.md:118-126,158-160` - one issue per unpublished Ticket in listing order, ID written back immediately (K1/K2 example), each issue links its Spec, says it is built through it, carries no "ready for agent" label | ✅ PASS |
| TKT-06.S2 | only one new issue, for K2; K1 still names 41 | `skills/spec-driven/references/tickets.md:130-134` - Rule 3 skips a Ticket with a Tracker ID; the example is K1 issue 41 / K2 only | ✅ PASS |
| TKT-06.S3 | K1, K2 have IDs, K3 none; K3 reported and stop; retry creates only K3 | `skills/spec-driven/references/tickets.md:142-152` - Rule 4 stops at the first failure, keeps written IDs, reports what was and was not published, resumes on the next "publish tickets"; the example is this exact case | ✅ PASS |
| TKT-07.S1 | no issue created; SR1-F3 listed as pending | `skills/spec-driven/references/tickets.md:106-108` - any Finding of the latest Spec Review without a Disposition: refuse, create no issue, list every pending Finding by ID ("SR1-F3 is still pending") | ✅ PASS |
| TKT-07.S2 | no issue created; says a Spec Review must run first | `skills/spec-driven/references/tickets.md:105` - no `spec-review-<n>.md`: refuse, create no issue, say a Spec Review must run first | ✅ PASS |
| TKT-08.S1 | tasks.md has a Tickets section with one Ticket listing every task | `skills/spec-driven/references/tasks.md:5,149` - Tasks runs at every scope; a Small feature gets exactly one Ticket `K1` listing every Task; `tickets.md:29` agrees | ✅ PASS |
| TKT-09.S1 | new Ticket "K3: Fix Verifier round 1" listing both fix tasks, Blocked by K2, covering the two Scenarios | `skills/spec-driven/references/implement.md:349-366` - one new Ticket titled `Fix Verifier round <r>` listing every fix task, Blocked by the Tickets with the gaps, Covers the gap Scenarios; example K3 at `:359`; `validate.md` section 8 and `tickets.md:68` agree | ✅ PASS |
| TKT-09.S2 | new Ticket "K4: Fix CR1" listing both fix tasks; each fix task has a Fixes field | `skills/spec-driven/references/review.md:90-98` - each accepted Finding becomes a fix task with `**Fixes**: CR1-Fn`, all in one `### K<n>: Fix CR<r>` Ticket; the example is K4 with T9, T10 | ✅ PASS |
| PLAN-01.S1 | exit 0; output warns about "Decisions & Assumptions" | `tests/test_validate_spec.py:89-90` - `assertEqual(code, 0)`, `assertRegex(out, r"WARN .*Decisions & Assumptions")` | ✅ PASS |
| PLAN-02.S1 | exit 0; output warns about "Tickets" | `tests/test_validate_tasks.py:77-78` - `assertEqual(code, 0)`, `assertRegex(out, r"WARN .*Tickets")` | ✅ PASS |
| PLAN-03.S1 | agent reads 09-validation-suite/context.md before writing the test | `skills/tdd/SKILL.md:24,33` - read the feature's `context.md` whenever it exists, whatever the plan kind, before the first test; the 09-validation-suite example is this case | ✅ PASS |
| PLAN-04.S1 | exit 0; validators skipped because foreign; report path docs-rfcs-042-billing/spec-review-1.md; plan unchanged | `tests/test_prep_review.py:171-177` - exit 0, `assertRegex(out, r"(?m)^Skipped: the plan is foreign\b...")`, report path `assertIn`, plan bytes equal to the fixture, no porcelain change, git log shows only the fixture commit | ✅ PASS |
| PLAN-04.S2 | report path kiro-specs-orders-design/spec-review-1.md; no previous run | `tests/test_prep_review.py:190-192` - exit 0, `assertIn("write the report to \`.specs/reviews/kiro-specs-orders-design/spec-review-1.md\`")`, `assertRegex(out, r"(?m)^- Previous run: none$")` | ✅ PASS |
| PLAN-04.S3 | exit 0; all three files listed as plan files; report path kiro-specs-payments/spec-review-1.md | `tests/test_prep_review.py:205-208` - exit 0, `assertRegex` on the exact `- Plan files:` line with all three files, report path `assertIn` | ✅ PASS |
| PLAN-04.S4 | report path under docs-042-billing-<hash>/ with the hash from docs/042-billing.md; no previous run | `tests/test_prep_review.py:222-227` - exit 0; `digest = sha1(b"docs/042-billing.md")[:8]` computed independently in the test; `assertIn(f"write the report to \`.specs/reviews/docs-042-billing-{digest}/spec-review-1.md\`")`; `assertRegex(out, r"(?m)^- Previous run: none$")`; both `source.txt` files checked | ✅ PASS |
| PLAN-05.S1 | asks about the retry rule only; spec links the RFC with its commit; RFC unchanged | `skills/spec-driven/references/specify.md:125-132` - read the foreign plan fully, ask only about its gaps and never about what it answers, never edit it, link it with its commit on a `**Source plan**:` line and copy none of it | ✅ PASS |
| PLAN-06.S1 | exit 0; output names feature demo and report path .specs/features/demo/spec-review-1.md | `tests/test_prep_review.py:242-244` - `assertEqual(code, 0)`, `assertRegex(out, r"(?m)^- Feature: \`demo\` ")`, `assertIn("write the report to \`.specs/features/demo/spec-review-1.md\`")` | ✅ PASS |
| PROOF-01.S1 | exit 0 | `tests/test_validate_scenarios.py:25` - `assertEqual(code, 0, out)`; fixture `tests/fixtures/base/.specs/features/demo/validation.md:13` holds the Given's header and PASS row | ✅ PASS |
| PROOF-01.S2 | exit 1; output names DEMO-01.S1 | `tests/test_validate_scenarios.py:37-38` - `assertEqual(code, 1)`, `assertRegex(out, r"ERROR .*DEMO-01\.S1.*validation\.md")` | ✅ PASS |
| PROOF-01.S3 | exit 1; output names DEMO-01.S1 | `tests/test_validate_scenarios.py:50-51` - `assertEqual(code, 1)`, `assertRegex(out, r"ERROR .*DEMO-01\.S1.*validation\.md")` | ✅ PASS |
| PROOF-01.S4 | exit 0 | `tests/test_validate_scenarios.py:62` - `assertEqual(code, 0, out)` with the `✅ PASS` fixture row | ✅ PASS |
| PROOF-01.S5 | exit 1; output says DEMO-01.S1 has more than one row | `tests/test_validate_scenarios.py:74-75` - `assertEqual(code, 1)`, `assertRegex(out, r"ERROR .*DEMO-01\.S1 has more than one row")` | ✅ PASS |
| PROOF-02.S1 | gate calls validate_scenarios.py with --only CSV-01.S1; validation.md later has exactly one row for CSV-02.S1 with file:line, reason, PASS/GAP | `skills/spec-driven/references/implement.md:123` - pass only `test` IDs to `--only`, never an `inspect` ID; `skills/spec-driven/references/validate.md:41,61` - the Verifier records each `inspect` Scenario in the one table, one row, `file:line` plus one-sentence reason, Result PASS or GAP | ✅ PASS |
| FLOW-01.S1 | none of the eight skill directories exist | `tests/test_install.py:58-62` - precondition lists all eight, exit 0, `assertEqual(left, [])` using `os.path.lexists` | ✅ PASS |
| FLOW-01.S2 | triage/SKILL.md still exists with the same content; output says "skipped triage: not installed by this repo" | `tests/test_install.py:75-78` - byte-equal content, directory holds only `SKILL.md`, `assertIn("skipped triage: not installed by this repo", out)` | ✅ PASS |
| FLOW-01.S3 | implement is still a symlink with unchanged target; output says "skipped implement: ..." | `tests/test_install.py:94-99` - `assertTrue(islink)`, `assertEqual(readlink, target)`, target content byte-equal, `assertIn("skipped implement: not installed by this repo", out)` | ✅ PASS |
| FLOW-02.S1 | skills/grilling/SKILL.md and skills/setup-spec-driven/SKILL.md exist | `tests/test_install.py:112-117` - empty precondition asserted, exit 0, `assertTrue(os.path.isfile(...SKILL.md))` for both | ✅ PASS |
| FLOW-03.S1 | agent reports a failing run of the test before any production edit, and a passing run after it | `skills/tdd/SKILL.md:61` - "see it fail before you edit any production file. Report that failing run ... then ... report the passing run"; `skills/spec-driven/references/implement.md:77` agrees | ✅ PASS |
| FLOW-04.S1 | agent starts a Small Specify whose first Scenario is the repro; no production file changed | `skills/diagnosing-bugs/SKILL.md:118,136-143,150,156` - "Do not apply the fix", revert every production edit and check `git status`, start Specify at Small, "The repro is the spec's first Scenario" | ✅ PASS |
| FLOW-05.S1 | message says /code-review is available; no change-review file created | `skills/spec-driven/references/implement.md:368-370` - on PASS say `/code-review` is available and stop; never run it or dispatch `change-reviewer`, so no change-review file is written | ✅ PASS |
| FLOW-06.S1 | prototype committed to a throwaway branch; Specify started with the verdict; nothing outside the prototype changed on main | `skills/prototype/SKILL.md:26-34` - commit to a throwaway branch, leave main unchanged (check `git status`), start Specify with the verdict, and this rule takes precedence over anything `LOGIC.md`/`UI.md` say about folding a winner in (see Edge Cases note on `UI.md:100`) | ✅ PASS |
| EDGE-01.S1 | agent reads docs/adr/0002-integer-cents.md before writing the test | `skills/tdd/SKILL.md:22,31` - root ADRs are read with or without `.specs/decisions/`; the example is this exact case | ✅ PASS |
| EDGE-01.S2 | agent reads src/billing/docs/adr/0002-integer-cents.md before the test | `skills/tdd/SKILL.md:23,32` - with `CONTEXT-MAP.md`, read `<context>/docs/adr/` for each context the paths fall under; the example names this file | ✅ PASS |
| EDGE-01.S3 | agent runs the docs/adr probe and reads the ADR | `skills/tdd/SKILL.md:23,32` - without a map, run `fd -t d -p 'docs/adr$' ...` and read every directory above the Task's paths "however deep it is"; `decisions.md:90-96` agrees | ✅ PASS |
| EDGE-02.S1 | Specify appends to billing-events.md; its summary row reads Specs "billing-events" | `skills/spec-driven/references/specify.md:62,136-139` - continue the `Specs: none` record, append, and change the record's Specs header and its `summary.md` row from `none` to the feature name; `skills/grill-with-docs/SKILL.md:38` agrees | ✅ PASS |

`validate_scenarios.py integrate-skills --root . --since abd3b89` (run after this table was written): 0 errors, exit 0. See "Closing gates" below.

**Status**: ✅ All Scenarios proven (33 `test` + 50 `inspect` = 83 PASS, 0 GAP, 0 spec-precision gaps)

---

## Discrimination Sensor

Run in a temporary `git worktree` (detached at `232ecc9`) under the session scratchpad; each mutant applied alone after `git checkout -- .` inside the worktree; the worktree was removed with `git worktree remove --force`. `git status --porcelain` of the real repo was empty before and after (identical). Installer tests ran against temp config dirs only.

| Mutation | File:line | Description | Killed? |
| -------- | --------- | ----------- | ------- |
| M1 (K8) | `skills/spec-driven/scripts/prep_review.py:237` | `feature_in_path` returns `None` always | ✅ Killed (`test_a_path_into_a_feature_folder_names_the_feature`) |
| M2 (K8) | `skills/spec-driven/scripts/prep_review.py:324` | hash suffix dropped (`slug = slug`) | ✅ Killed (`test_colliding_slugs_keep_separate_histories`) |
| M3 (K8) | `skills/spec-driven/scripts/prep_review.py:321` | `source.txt` ignored (`owner` returns `None`) | ✅ Killed (`test_colliding_slugs_keep_separate_histories`) |
| M4 (K8) | `skills/spec-driven/scripts/validate_spec.py:241` | traceability ID read from the last column (`key = "status"`) | ✅ Killed (4 failures: GRILL-05.S2, GRILL-09.S1, GRILL-09.S2, PLAN-01.S1 tests) |
| M5 | `skills/spec-driven/scripts/validate_scenarios.py:91` | Result check removed: a `❌ GAP` row proves an inspect Scenario | ✅ Killed (`test_gap_row_fails`) |
| M6 | `skills/spec-driven/scripts/validate_tasks.py:165` | forward `Blocked by` check disabled | ✅ Killed (`test_forward_blocking_edge`) |
| M7 | `install.sh:44` | symlink guard `[ ! -L "$dest" ]` removed from retirement | ✅ Killed (`test_a_symlinked_skill_survives`) |
| M8 | `install.sh:44` | shipped-phrase `grep -qF` removed from retirement | ✅ Killed (`test_another_sources_skill_survives`) |

**Sensor depth**: lightweight plus (8 mutations; 4 on the K8 diff, 4 on earlier scripts and the installer)
**Result**: 8/8 killed - PASS ✅

---

## Interactive UAT Results

Skipped on the orchestrator's instruction (validate.md section 7). The Change is skill prose, scripts and an installer; the `inspect` rows above are the proof for the prose.

---

## Code Quality

Focused on the K8 diff (`git diff 8b8776e..HEAD -- skills tests`).

| Principle        | Status |
| ---------------- | ------ |
| Minimum code     | ✅ `feature_in_path` (9 lines) and `report_slug` (16 lines) do one job each; T34 deletes 2 helpers and reuses `scenarios_lib.find_tables` |
| Surgical changes | ✅ only `prep_review.py`, `validate_spec.py`, `tests/test_prep_review.py` and one fixture folder changed in code |
| No scope creep   | ✅ each change maps to CR1-F1, CR1-F2 or CR1-F5 |
| Matches patterns | ✅ same subprocess-and-fixture test style; `find_tables` is the shared header-name reader the feature already uses |
| Spec-anchored outcome check (asserted values match spec) | ✅ PLAN-04.S4 computes the expected hash independently from the path in the Then step; PLAN-06.S1 asserts the feature line and the exact report path |
| Per-layer Coverage Expectation met | ✅ every `test` Scenario of the scripts and installer has exactly one test (33/33) |
| Every test proves exactly one Scenario - no Unclaimed Tests touched | ✅ `validate_scenarios.py --since abd3b89` reports 0 errors |
| Behavior Tests, not Implementation-Coupled | ✅ tests run the scripts as subprocesses on fixture repos and read only stdout, exit code and files on disk; the `source.txt` reads in the PLAN-04.S4 test check a documented on-disk artifact (design.md:120) |
| Repo Standards + Smell Baseline: spec `## Standards` (stdlib only, fixtures as `.md`/`.txt`, real graphify) | ✅ no new dependencies; `hashlib` is stdlib; the new fixture is `.md`/`.txt` |

Advisory (not gaps):

- `report_slug` writes `source.txt` before `snapshot` runs; if the snapshot then fails, an uncommitted `source.txt` stays behind. Harmless: the next run reads it as the same owner.
- T34's What says the table is found "by its `Requirement ID` and `Status` headers", but `validate_spec.py:242` requires only `Requirement ID`. Behavior matches the old reader, which is what T34 promised.
- The Task Granularity and Test Co-location tables in `tasks.md` do not list T32-T34. Plan bookkeeping only.
- Sonar-style note: `hashlib.sha1` used for a folder-name suffix, not for security.

---

## Edge Cases

Spec edge cases (EDGE-01, EDGE-02) are proven in the table above. Additional K8 probes, run on throwaway fixture repos in the scratchpad:

- [x] Path to the feature folder with a trailing slash (`.specs/features/demo/`): resolves to feature `demo`, report `.specs/features/demo/spec-review-1.md`.
- [x] Relative path from a subdirectory (`cd .specs && prep_review.py spec features/demo/spec.md`): resolves to feature `demo`.
- [x] A file directly under `.specs/features/` (`README.md`): `STOP: no feature \`README.md\` under .specs/features/ (have: demo)`, a clear message.
- [x] Foreign review: `source.txt` lands in the pre-review snapshot commit (`docs(spec): snapshot docs-rfcs-042-billing before spec review` contains `.specs/reviews/docs-rfcs-042-billing/source.txt`), tree clean afterwards.
- [x] A report folder from before K8 with no `source.txt`, holding a review of `docs/042_billing.md`: a review of `docs/042-billing.md` adopts that folder and is numbered SR2 with the other plan's report as Previous run. This is the documented choice in T33 ("Existing folders without `source.txt` are treated as owned by the current target") and `design.md:120`; such folders could only come from this unmerged branch's PLAN-04 S1-S3 builds. Advisory, not a gap.
- [x] `skills/prototype/UI.md:100` still says "Fold the winner into the real code". `skills/prototype/SKILL.md:34` declares its hand-off rule takes precedence over `LOGIC.md`/`UI.md` and names folding a winner in as Execute's work, so the instructions taken together give FLOW-06.S1's outcome. Advisory: rewording `UI.md` step 6 would remove the contradiction a reader sees first.

---

## Gate Check

- **quick**: `python3 -m unittest discover -s tests -v` - exit 0; 33 passed, 0 failed, 0 skipped (real `graphify` on PATH)
- **build**: `bash -n install.sh && node --check render-adapters.js && python3 -m py_compile skills/spec-driven/scripts/*.py` - exit 0
- **plan**: `validate_spec.py integrate-skills --root .` - exit 0 (0 errors, 0 warnings); `validate_tasks.py integrate-skills --root .` - exit 0 (0 errors, 26 warnings: multi-file `Where` granularity smells and `Tests: none` confirmations, each matching the Task Granularity and Test Co-location tables)
- **Test count before feature**: 0 (the base `abd3b89` had no `tests/`)
- **Test count after previous round** (`8b8776e`): 31
- **Test count after feature**: 33
- **Delta**: +33 over the feature, +2 in K8 (PLAN-04.S4, PLAN-06.S1); no test removed or weakened
- **Skipped tests**: none
- **Failures**: none

### Closing gates

- `python3 skills/spec-driven/scripts/validate_scenarios.py integrate-skills --root . --since abd3b89`: exit 0, `validate_scenarios: 0 error(s), 0 warning(s)` (83 Scenarios: 33 `test` with one test each, 50 `inspect` with one PASS row each)
- `python3 skills/spec-driven/scripts/validate_state.py integrate-skills`: exit 0

---

## Fix Plans

None. No gaps were found in this round, so no fix Ticket is proposed.

---

## Requirement Traceability Update

The spec's Requirement Traceability still shows the two requirements K8 touched as planned. The Verifier does not edit `spec.md`; the orchestrator should apply:

| Requirement | Previous Status | New Status   |
| ----------- | --------------- | ------------ |
| PLAN-04     | Tasks / Pending | ✅ Verified (Execute) |
| PLAN-06     | Tasks / Pending | ✅ Verified (Execute) |
| all other 54 requirements | Execute / Verified | ✅ Verified (unchanged) |

---

## Summary

**Overall**: ✅ Ready

**Spec-anchored check**: 83/83 Scenarios matched the spec outcome (33 `test`, 50 `inspect`); 0 spec-precision gaps
**Sensor**: 8/8 mutations killed
**Gate**: 33 passed, 0 failed; build, plan and closing gates exit 0

**What works**: `/spec-review .specs/features/<f>/...` now reviews feature `<f>` (CR1-F1); two foreign plans whose slugs collide get separate report folders keyed by `source.txt` plus a path hash (CR1-F2); `validate_spec.py` reads the traceability table by header name with the old first-column behavior as fallback (CR1-F5). All 81 earlier Scenarios still hold.

**Issues found**: none blocking. Advisory: pre-K8 report folders without `source.txt` are adopted by the current target (documented choice); `skills/prototype/UI.md:100` still reads as folding the winner into real code, overridden by `SKILL.md:34`; set PLAN-04 and PLAN-06 to Verified in the spec's traceability table.

**Next steps**: the orchestrator commits this report and tells the human that `/code-review` is available.
