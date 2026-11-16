# Integrate Skills Validation

**Date**: 2026-11-16
**Spec**: `.specs/features/integrate-skills/spec.md`
**Diff range**: `abd3b89..HEAD` (`abd3b89` = last planning commit; HEAD = `e6cb82f`, 33 build commits)
**Verifier**: independent sub-agent (author ≠ verifier)

## Validation: integrate-skills - PASS

All 81 Scenarios are proven: 31 `test` Scenarios by tests whose assertions target the exact Then outcome, 50 `inspect` Scenarios by the final skill and agent text. Every gate exits 0. The discrimination sensor killed 17 of 18 mutants; the one survivor is an equivalent mutant (another guard produces the same behavior). Interactive UAT (validate.md section 7) and Lessons distillation (section 10) were skipped on the orchestrator's instruction.

---

## Task Completion

| Task | Status | Notes |
| ---- | ------ | ----- |
| T1-T31 | ✅ Done | all 31 Tasks in `tasks.md` have every Done-when box ticked (74 `[x]`, 0 `[ ]`); one commit each in `git log abd3b89..HEAD` plus a plan repair (`fa0c455`) |

---

## Scenario-Anchored Check

One row per Scenario, `test` and `inspect` alike. An `inspect` row cites the `file:line` read and a one-sentence reason in place of a test assertion.

| Scenario | Spec-defined outcome (Then) | `file:line` + assertion | Result |
| -------- | --------------------------- | ----------------------- | ------ |
| GRILL-01.S1 | every agent turn holds exactly one question; every question lists options and marks one recommended | `skills/spec-driven/references/specify.md:76-77` (and `skills/grilling/SKILL.md:16-22`) - both state "every turn contains exactly one question" and that each question lists concrete options with exactly one marked recommended | ✅ PASS |
| GRILL-02.S1 | "you decide" records the recommended option as a Decision with `Decided by: agent` | `skills/spec-driven/references/specify.md:102` - the recommended option becomes the answer and is recorded as a Decision reading `Decided by: agent` (same in `skills/grilling/SKILL.md:30`, `skills/domain-modeling/GRILLING-RECORD-FORMAT.md:141`) | ✅ PASS |
| GRILL-03.S1 | next turn lists one default per unasked branch; nothing written to spec.md until the user replies | `skills/spec-driven/references/specify.md:103` - next turn lists one default for every unasked branch, then waits, and "Write nothing to `spec.md` until the user replies" | ✅ PASS |
| GRILL-04.S1 | first message names the existing capability by path and asks what is needed beyond it before any other question | `skills/spec-driven/references/specify.md:53,69` - step 1.3 runs the graphify search before the first question, and first-message rule 3 names the capability by file path and makes "what does the user need beyond it?" the only question until answered | ✅ PASS |
| GRILL-05.S1 | exit 1; output names "Decisions & Assumptions" | `tests/test_validate_spec.py:24-26` - `assertEqual(code, 1)`, `assertRegex(out, r"ERROR .*Decisions & Assumptions")`, `assertIn("validate_spec: 1 error(s)", out)` | ✅ PASS |
| GRILL-05.S2 | exit 1; output names "Decisions & Assumptions" | `tests/test_validate_spec.py:37-39` - `assertEqual(code, 1)`, `assertRegex(out, r"ERROR .*Decisions & Assumptions")`, exactly 1 error | ✅ PASS |
| GRILL-06.S1 | exit 0 | `tests/test_validate_spec.py:49` - `assertEqual(code, 0, out)` | ✅ PASS |
| GRILL-07.S1 | feature folder has spec.md and no context.md; a Decisions row chooses "download, not email" | `skills/spec-driven/references/specify.md:5,154-158` - Specify never writes `context.md` ("The feature folder gets `spec.md` and nothing else"), every record Decision gets a Decisions & Assumptions row, with "download, not email" as the worked example | ✅ PASS |
| GRILL-08.S1 | agent reads grilling/SKILL.md next to spec-driven before its first question | `skills/spec-driven/references/specify.md:57` - without a load-by-name tool, read `<skill-dir>/../grilling/SKILL.md` (plus domain-modeling), "Either way, you have read the grilling rules ... before your first question" | ✅ PASS |
| GRILL-09.S1 | exit 1; output names "D-demo.2" | `tests/test_validate_spec.py:60-62` - `assertEqual(code, 1)`, `assertRegex(out, r"ERROR .*D-demo\.2")`, exactly 1 error | ✅ PASS |
| GRILL-09.S2 | exit 1; output names "rows fit in memory" | `tests/test_validate_spec.py:73-75` - `assertEqual(code, 1)`, `assertRegex(out, r"ERROR .*rows fit in memory")`, exactly 1 error | ✅ PASS |
| GRILL-10.S1 | asks about each dimension it cannot resolve; spec lists every dimension with a criterion ID or "N/A because" | `skills/spec-driven/references/specify.md:115-121` - at Large/Complex every dimension is a closing branch, unresolved ones asked one per turn, and the spec's Decisions & Assumptions lists every dimension with a criterion ID or `N/A because` reason | ✅ PASS |
| REC-01.S1 | `.specs/decisions/csv-export.md` exists with "Status: draft"; Session path holds question, options, recommendation, answer | `skills/spec-driven/references/specify.md:107` - at the first answer create `.specs/decisions/<slug>.md` with `Status: draft` and the first question, options, recommendation and answer in the Session path (format: `skills/domain-modeling/GRILLING-RECORD-FORMAT.md:153`) | ✅ PASS |
| REC-01.S2 | a record with a different slug is created; existing csv-export.md unchanged | `skills/spec-driven/references/specify.md:107` - "If `<slug>.md` already exists and belongs to other work ... create the record under a different slug and leave the existing file unchanged" (also `GRILLING-RECORD-FORMAT.md:58`) | ✅ PASS |
| REC-02.S1 | three answered questions on disk before the fourth question is shown | `skills/spec-driven/references/specify.md:108` - append before the next question, with this exact example: "After the third answer the file holds three answered questions; the fourth question comes after that write" | ✅ PASS |
| REC-03.S1 | header "Status: active"; summary row after billing-retries with Date, 1-2 sentence Summary, active, Binds, Areas, Specs csv-export; spec rows link D-csv-export anchors | `skills/spec-driven/references/specify.md:144-148,153-154` - at confirmation complete the record, set `Status: active`, insert the summary row in Date order with every listed column, and only then write spec rows linking `D-<slug>.k` anchors | ✅ PASS |
| REC-04.S1 | sections Context, Session path, Decisions, Consequences, Related; rejected option listed; each Decision one choice with all five fields | `skills/domain-modeling/GRILLING-RECORD-FORMAT.md:63,140-143` - the five sections are required and never empty, rejected options stay in the Session path, one choice per Decision, all five fields (echoed in `specify.md:109-110,146`) | ✅ PASS |
| REC-05.S1 | D-csv-export.3 chooses Money; has a Changed line citing spec-review-1 SR1-F2; nothing reads "superseded" | `skills/spec-driven/references/review.md:56-69,83` - rewrite the Choice in place, add `Changed: <date> by <feature> (spec-review-1 SR1-F2)`, never mark a Decision replaced; the worked example is this Scenario | ✅ PASS |
| REC-05.S2 | D-billing-retries.2 in billing-retries.md chooses five retries; Changed line names invoice-pdf; invoice-pdf's record does not restate it | `skills/spec-driven/references/design.md:115` - rewrite in the other record with a `Changed` line naming this feature; "It does not restate the old choice as a new Decision of its own" (also `review.md:71`, `GRILLING-RECORD-FORMAT.md:171`) | ✅ PASS |
| REC-05.S3 | csv-export.md has a Review section holding D-csv-export.9 citing SR1-F4 | `skills/spec-driven/references/review.md:73` - an accepted Finding adding an uncovered rule becomes a Decision under `## Review` with the next free ID citing the Finding; worked example `D-csv-export.9` / `SR1-F4` | ✅ PASS |
| REC-06.S1 | Design section with D-csv-export.7 choosing streaming; design.md Tech Decisions links D-csv-export.7 | `skills/spec-driven/references/design.md:93,99-104,110` - Design Decisions continue the numbering (`.6` → `.7`) under `## Design`, and `design.md`'s `## Tech Decisions` links each one; the example is streaming rows | ✅ PASS |
| REC-07.S1 | summary.md has a legacy line naming docs/adr/ and one naming .specs/STATE.md | `skills/spec-driven/references/specify.md:149` - creating the first `summary.md` adds one legacy line for `docs/adr/` and one for `.specs/STATE.md` when it has `## Decisions` (also `GRILLING-RECORD-FORMAT.md:206`) | ✅ PASS |
| REC-08.S1 | no new file under docs/adr/; STATE.md gains no AD entry; the Decision is in the feature's record | `skills/spec-driven/references/design.md:12,108` - a project-binding Design Decision goes only into the record, "no new file under `docs/adr/`, no `AD-NNN` entry in `.specs/STATE.md`", even in repos that have both (also `memory.md:7-9`) | ✅ PASS |
| REC-09.S1 | a new Grilling Record exists; its summary.md row reads Specs "none" | `skills/grill-with-docs/SKILL.md:26-30` - the session creates `.specs/decisions/<slug>.md` with `Specs: none`, and at confirmation adds the summary row whose Specs cell reads `none` | ✅ PASS |
| REC-10.S1 | first question is the next unanswered branch after the five; no second record | `skills/spec-driven/references/specify.md:61,70` - a draft for this feature is resumed, answers taken as given, "Your first question is the next unanswered branch. Do not create another record." | ✅ PASS |
| READ-01.S1 | opens billing-rules.md and money.md; not dark-mode.md or billing-ledger.md | `skills/tdd/SKILL.md:21,30` - open only `active` records binding the project with overlapping Areas or `*`, or naming the feature; skip drafts; the worked example is this Scenario (rule source `decisions.md:46-55`) | ✅ PASS |
| READ-02.S1 | names .kiro/specs/payments/ and docs/rfcs/ before the first question; record Context cites sources used | `skills/spec-driven/references/decisions.md:16,30,32` - `fd -H --no-ignore-vcs` sees gitignored folders, found material is named by path before the first question, and used sources are cited in the record Context (`specify.md:68,111`) | ✅ PASS |
| READ-03.S1 | first message asks the user to install fd; no planning question until fd is available | `skills/spec-driven/references/specify.md:44,67` - if `fd` is missing the first message asks to install it "and contains nothing else"; no planning question until `fd` is available (`decisions.md:34`) | ✅ PASS |
| READ-04.S1 | the check prints a warning naming fd when fd is not on PATH; install continues | `install.sh:86-88` - `if ! command -v fd` prints `WARNING: fd not found ...` with no `exit`, and the script continues to the hooks step | ✅ PASS |
| READ-05.S1 | warns gone.md is missing and billing-rules.md has no row; opens billing-rules.md | `skills/spec-driven/references/decisions.md:63-72` - a missing file or a row-less active record breaks the index; warn one line per problem (both example messages given) and decide from headers, which opens the active project record covering `src/billing/` (`specify.md:47`) | ✅ PASS |
| READ-06.S1 | graphify-out/graph.json still exists; refreshed with graphify update . if needed | `skills/spec-driven/SKILL.md:39` - Critical Rule 11: `graphify-out/` is the graph cache, may be gitignored, is never deleted, `graph.json` still exists after a phase, refresh only with `graphify update .` (also `SKILL.md:99`, `standards.md:117`) | ✅ PASS |
| REV-01.S1 | exit 0; HEAD commit contains the three edited paths | `tests/test_prep_review.py:51-52` - `assertEqual(code, 0)`, `assertEqual(sorted(head_paths(repo)), sorted(edited))` | ✅ PASS |
| REV-01.S2 | exit 0; HEAD commit contains CONTEXT-MAP.md and src/billing/CONTEXT.md | `tests/test_prep_review.py:67-68` - `assertEqual(code, 0)`, `assertEqual(sorted(head_paths(repo)), sorted(edited))` | ✅ PASS |
| REV-02.S1 | output lists .specs/decisions/demo.md; does not mention context.md | `tests/test_prep_review.py:84-86` - `assertRegex(out, r"(?m)^- Grilling Records: `\.specs/decisions/demo\.md`$")`, `assertNotIn("context.md", out)` | ✅ PASS |
| REV-02.S2 | output lists old-demo/context.md as a legacy decision source | `tests/test_prep_review.py:97-98` - `assertRegex(out, r"(?m)^- Legacy decision source: `\.specs/features/old-demo/context\.md`$")` | ✅ PASS |
| REV-02.S3 | output lists re-demo/context.md as a legacy decision source | `tests/test_prep_review.py:109-110` - `assertRegex(out, r"(?m)^- Legacy decision source: `\.specs/features/re-demo/context\.md`$")` | ✅ PASS |
| REV-03.S1 | report has a Finding citing the Session path question and the spec criterion | `agents/spec-reviewer.md:50` - walk the Session path answer by answer; a dropped or contradicted answer is a Finding citing the record question and the criterion ID; the example is "download, not email" vs a criterion that emails (`finding-format.md:65`) | ✅ PASS |
| REV-04.S1 | Thought Partnership Finding naming D-csv-export.5 | `agents/spec-reviewer.md:40` - every `Decided by: agent` Decision that changes behavior, data or cost raises a Thought Partnership Finding naming its ID (example `D-csv-export.5`) | ✅ PASS |
| REV-05.S1 | Communication Finding naming D-csv-export.2 | `agents/spec-reviewer.md:52-53` - a Decision whose Trade-off line is missing or empty raises a Communication Finding naming it (example `D-csv-export.2`) | ✅ PASS |
| REV-05.S2 | Communication Finding naming D-csv-export.4 | `agents/spec-reviewer.md:54` - one ID holding several unrelated choices raises a Communication Finding naming it (example: five unrelated defaults under `D-csv-export.4`) | ✅ PASS |
| REV-06.S1 | Finding citing D-money.1 and the float's file:line | `agents/change-reviewer.md:47` - a contradicted active Decision with no `Changed` line raises a Finding citing the Decision ID and the code `file:line`; the example is `D-money.1` vs a float total | ✅ PASS |
| TKT-01.S1 | exit 1; output starts with "STOP" and names tasks.md | `tests/test_prep_review.py:125-126` - `assertEqual(code, 1)`, `assertRegex(out, r"\ASTOP: .*tasks\.md")` | ✅ PASS |
| TKT-02.S1 | exit 1; output starts with "STOP" and names design.md | `tests/test_prep_review.py:138-139` - `assertEqual(code, 1)`, `assertRegex(out, r"\ASTOP: .*design\.md")` | ✅ PASS |
| TKT-02.S2 | output does not name design.md in a STOP message | `tests/test_prep_review.py:150-152` - `assertEqual(code, 0)`, `assertNotRegex(out, r"(?m)^STOP")`, Review context printed | ✅ PASS |
| TKT-03.S1 | exit 1; output names T2 | `tests/test_validate_tasks.py:24-26` - `assertEqual(code, 1)`, `assertRegex(out, r"ERROR T2\b.*Ticket")`, exactly 1 error | ✅ PASS |
| TKT-03.S2 | exit 0 | `tests/test_validate_tasks.py:37` - `assertEqual(code, 0, out)` | ✅ PASS |
| TKT-04.S1 | exit 1; output names T2, K1 and K2 | `tests/test_validate_tasks.py:48-50` - `assertEqual(code, 1)`, `assertRegex(out, r"ERROR T2\b.*\bK1\b.*\bK2\b")`, exactly 1 error | ✅ PASS |
| TKT-05.S1 | exit 1; output names K1 and K2 | `tests/test_validate_tasks.py:61-63` - `assertEqual(code, 1)`, `assertRegex(out, r"ERROR K1\b.*\bK2\b")`, exactly 1 error | ✅ PASS |
| TKT-06.S1 | one issue for K1 then K2; both Tickets name their issue ID; each issue links the spec, no ready-for-agent label | `skills/spec-driven/references/tickets.md:118-126,158-160` - one issue per unpublished Ticket in listing order, ID written back immediately, issue links the Spec and says it is built through it, no "ready for agent" label; the K1/K2 example is this Scenario | ✅ PASS |
| TKT-06.S2 | only one new issue, for K2; K1 still names 41 | `skills/spec-driven/references/tickets.md:130-134` - a Ticket with a Tracker ID is skipped and its line left as is; example: K1 names 41, only K2 is created | ✅ PASS |
| TKT-06.S3 | K1, K2 name IDs and K3 none; K3 reported not published, stop; rerun creates only K3 | `skills/spec-driven/references/tickets.md:142-152` - stop at the first failure, keep written IDs, report published and not published, next run resumes; the K1-K3 example is this Scenario | ✅ PASS |
| TKT-07.S1 | no tracker issue created; SR1-F3 listed as pending | `skills/spec-driven/references/tickets.md:106-108` - a `(pending)` Disposition makes the agent refuse, create no issue and list each pending Finding by ID ("SR1-F3 is still pending") | ✅ PASS |
| TKT-07.S2 | no tracker issue created; agent says a Spec Review must run first | `skills/spec-driven/references/tickets.md:105` - with no `spec-review-<n>.md`, refuse, create no issue, and say a Spec Review must run first (also `review.md:106`) | ✅ PASS |
| TKT-08.S1 | tasks.md has a Tickets section with one Ticket listing every task | `skills/spec-driven/references/tasks.md:5,149` - Tasks runs at every scope; "A Small feature ... gets exactly one Ticket, `K1`, and every Task in `tasks.md` is listed in that Ticket" (also `tickets.md:29`) | ✅ PASS |
| TKT-09.S1 | new Ticket "K3: Fix Verifier round 1" listing both fix tasks; Blocked by K2; covers the two Scenarios | `skills/spec-driven/references/implement.md:349-359` - one Ticket per failed round titled `Fix Verifier round <r>`, Tasks = all fix tasks, Blocked by the Tickets with the gaps, Covers the gap Scenarios; example `K3` (also `validate.md:188-196`) | ✅ PASS |
| TKT-09.S2 | new Ticket "K4: Fix CR1" listing both fix tasks; each has a Fixes field naming its Finding | `skills/spec-driven/references/review.md:94-98` - each accepted Finding becomes `T<n>: Fix CR1-F<k>` with `**Fixes**: CR1-F<k>`, all in one Ticket `### K<n>: Fix CR<r>`; example K4 with T9, T10 | ✅ PASS |
| PLAN-01.S1 | exit 0; output warns about "Decisions & Assumptions" | `tests/test_validate_spec.py:89-90` - `assertEqual(code, 0)`, `assertRegex(out, r"WARN .*Decisions & Assumptions")` | ✅ PASS |
| PLAN-02.S1 | exit 0; output warns about "Tickets" | `tests/test_validate_tasks.py:77-78` - `assertEqual(code, 0)`, `assertRegex(out, r"WARN .*Tickets")` | ✅ PASS |
| PLAN-03.S1 | agent reads 09-validation-suite/context.md before writing the test | `skills/tdd/SKILL.md:24,33` - if the feature's `context.md` exists read it whole, whatever the plan kind, before the first test; the example is this Scenario | ✅ PASS |
| PLAN-04.S1 | exit 0; validators skipped because foreign; report path docs-rfcs-042-billing/spec-review-1.md; plan unchanged | `tests/test_prep_review.py:170-176` - exit 0, `assertRegex(... "^Skipped: the plan is foreign ...")`, no `exit` line, report path asserted, plan bytes equal the fixture, clean status, only the fixture commit touches it | ✅ PASS |
| PLAN-04.S2 | report path kiro-specs-orders-design/spec-review-1.md; no previous run | `tests/test_prep_review.py:189-191` - exit 0, `assertIn("write the report to `.specs/reviews/kiro-specs-orders-design/spec-review-1.md`")`, `assertRegex(out, r"(?m)^- Previous run: none$")` | ✅ PASS |
| PLAN-04.S3 | exit 0; all three files listed as plan files; report path kiro-specs-payments/spec-review-1.md | `tests/test_prep_review.py:204-207` - exit 0, `assertRegex` on the exact `- Plan files:` line with all three paths, report path asserted | ✅ PASS |
| PLAN-05.S1 | asks about the retry rule and nothing the RFC answers; spec links the RFC with its commit; RFC unchanged | `skills/spec-driven/references/specify.md:125-132` - read the foreign plan first, ask only about its gaps, never edit it, link it on a `**Source plan**:` line with `git log -1` commit, copy none of it | ✅ PASS |
| PROOF-01.S1 | exit 0 | `tests/test_validate_scenarios.py:25` - `assertEqual(code, 0, out)` on the `base` fixture whose row reads `PASS` | ✅ PASS |
| PROOF-01.S2 | exit 1; output names DEMO-01.S1 | `tests/test_validate_scenarios.py:37-38` - `assertEqual(code, 1)`, `assertRegex(out, r"ERROR .*DEMO-01\.S1.*validation\.md")` | ✅ PASS |
| PROOF-01.S3 | exit 1; output names DEMO-01.S1 | `tests/test_validate_scenarios.py:50-51` - `assertEqual(code, 1)`, `assertRegex(out, r"ERROR .*DEMO-01\.S1.*validation\.md")` | ✅ PASS |
| PROOF-01.S4 | exit 0 | `tests/test_validate_scenarios.py:62` - `assertEqual(code, 0, out)` on the `✅ PASS` fixture | ✅ PASS |
| PROOF-01.S5 | exit 1; output says DEMO-01.S1 has more than one row | `tests/test_validate_scenarios.py:74-75` - `assertEqual(code, 1)`, `assertRegex(out, r"ERROR .*DEMO-01\.S1 has more than one row")` | ✅ PASS |
| PROOF-02.S1 | gate calls validate_scenarios.py with --only CSV-01.S1; validation.md has exactly one row for CSV-02.S1 with file:line, reason, PASS or GAP | `skills/spec-driven/references/implement.md:123` - the Task gate passes only `test` IDs to `--only` and never an `inspect` ID; `skills/spec-driven/references/validate.md:36-41,61-62` - one table, one row per Scenario, `inspect` evidence is `file:line` + reason, Result PASS or GAP | ✅ PASS |
| FLOW-01.S1 | none of the eight skill directories exist | `tests/test_install.py:60-62` - exit 0, `left = [... os.path.lexists(...)]`, `assertEqual(left, [])` | ✅ PASS |
| FLOW-01.S2 | triage/SKILL.md still exists with the same content; output "skipped triage: not installed by this repo" | `tests/test_install.py:75-78` - exit 0, byte-equal `SKILL.md`, folder holds only `SKILL.md`, `assertIn("skipped triage: not installed by this repo", out)` | ✅ PASS |
| FLOW-01.S3 | implement still a symlink, target unchanged; output "skipped implement: not installed by this repo" | `tests/test_install.py:94-99` - `assertTrue(os.path.islink(link))`, same `readlink`, target contents unchanged, `assertIn("skipped implement: ...", out)` | ✅ PASS |
| FLOW-02.S1 | skills/grilling/SKILL.md and skills/setup-spec-driven/SKILL.md exist | `tests/test_install.py:115-117` - exit 0, `assertTrue(os.path.isfile(... name, "SKILL.md"))` for both | ✅ PASS |
| FLOW-03.S1 | agent reports a failing run of the test before any production edit, and a passing run after | `skills/tdd/SKILL.md:61` - "write its test, run it, and see it fail before you edit any production file. Report that failing run ... then ... report the passing run" (also `implement.md:75-77`, report template `implement.md:401`) | ✅ PASS |
| FLOW-04.S1 | Small Specify starts with the repro as first Scenario; no production file changed | `skills/diagnosing-bugs/SKILL.md:118,136-145,148-156` - Phase 5 forbids applying the fix, reverts every production edit and checks `git status`, then starts a Small Specify whose first Scenario is the repro | ✅ PASS |
| FLOW-05.S1 | message says /code-review is available; no change-review file created | `skills/spec-driven/references/implement.md:368-370` - on PASS the closing message says `/code-review` is available, then stop; never run it or dispatch `change-reviewer` (also `review.md:8`) | ✅ PASS |
| FLOW-06.S1 | prototype committed to a throwaway branch; Specify starts with the verdict; no file outside the prototype changed on main | `skills/prototype/SKILL.md:26-34` - commit to a throwaway branch, leave main unchanged (checked with `git status`), start Specify with the verdict; line 34 overrides the "fold the winner in" wording of `UI.md:100` (see Code Quality) | ✅ PASS |
| EDGE-01.S1 | agent reads docs/adr/0002-integer-cents.md before writing the test | `skills/tdd/SKILL.md:22,31` - root ADRs are read with or without `.specs/decisions/`; the example is this Scenario | ✅ PASS |
| EDGE-01.S2 | agent reads src/billing/docs/adr/0002-integer-cents.md before writing the test | `skills/tdd/SKILL.md:23,32` - with a `CONTEXT-MAP.md`, read `<context>/docs/adr/` for every context the Task's paths fall under; example `src/billing/` | ✅ PASS |
| EDGE-01.S3 | agent runs the docs/adr probe and reads the deep ADR | `skills/tdd/SKILL.md:23,32` - without a map, run `fd -t d -p 'docs/adr$' ...` and read ADRs of every directory above the Task's paths "however deep it is" (`decisions.md:90-96`) | ✅ PASS |
| EDGE-02.S1 | Specify appends to billing-events.md; its summary row reads Specs "billing-events" | `skills/spec-driven/references/specify.md:62,136-140` - a `Specs: none` record the feature grows from is continued (no new record), and its header and `summary.md` Specs cell change from `none` to the feature name (also `grill-with-docs/SKILL.md:38`) | ✅ PASS |

`validate_scenarios.py integrate-skills --root . --since abd3b89` (run after this table is written): 0 errors, 0 warnings, 81 Scenarios proven - exit 0.

**Status**: ✅ All Scenarios proven

---

## Discrimination Sensor

Run in a temporary `git worktree` under the session scratchpad, removed with `git worktree remove --force` afterward. `git status --porcelain` of the real repo was empty before and after (identical). `graphify-out/` untouched. Installer tests ran against temp `CLAUDE_CONFIG_DIR`/`OPENCODE_CONFIG_DIR`/`HOME`.

| Mutation | File:line | Description | Killed? |
| -------- | --------- | ----------- | ------- |
| 1 | `skills/spec-driven/scripts/validate_scenarios.py:91` | Accept a `GAP` Result as PASS | ✅ Killed (PROOF-01.S3) |
| 2 | `skills/spec-driven/scripts/validate_scenarios.py:89` | Skip the duplicate-row check | ✅ Killed (PROOF-01.S5) |
| 3 | `skills/spec-driven/scripts/validate_spec.py:177` | Treat a legacy spec as native (`native = True`) | ✅ Killed (PLAN-01.S1) |
| 4 | `skills/spec-driven/scripts/validate_spec.py:218` | Stop checking the Decisions table's Choice cell | ✅ Killed (GRILL-09.S1) |
| 5 | `skills/spec-driven/scripts/validate_tasks.py:165` | Accept a forward `Blocked by` edge | ✅ Killed (TKT-05.S1) |
| 6 | `skills/spec-driven/scripts/validate_tasks.py:160` | Accept a task listed in two Tickets | ✅ Killed (TKT-04.S1) |
| 7 | `skills/spec-driven/scripts/validate_tasks.py:229` | Treat a legacy task plan as native (Ticket rules always errors) | ✅ Killed (PLAN-02.S1) |
| 8 | `skills/spec-driven/scripts/prep_review.py:187` | Protect only the root `CONTEXT.md`, not per-context ones | ✅ Killed (REV-01.S2) |
| 9 | `skills/spec-driven/scripts/prep_review.py:284` | Medium scope no longer needs `design.md` | ✅ Killed (TKT-02.S1) |
| 10 | `skills/spec-driven/scripts/prep_review.py:292` | List `context.md` only for legacy plans | ✅ Killed (REV-02.S3) |
| 11 | `skills/spec-driven/scripts/prep_review.py:323` | Run the structural validators on a foreign plan | ✅ Killed (PLAN-04.S1) |
| 12 | `skills/spec-driven/scripts/prep_review.py:314` | Foreign plan written to (never-write guard broken) | ✅ Killed (PLAN-04.S1-S3) |
| 13 | `skills/spec-driven/scripts/prep_review.py:314` | Drop the "foreign plan has uncommitted changes" refusal | ⚪ Survived - equivalent mutant: `snapshot()` (`prep_review.py:258-261`) still refuses the dirty foreign file as "outside the plan" and commits nothing (checked by hand in the scratch: exit 1, no commit). No behavior change, no fix needed |
| 14 | `skills/spec-driven/scripts/prep_review.py:318` | Report slug from the file's basename only | ✅ Killed (PLAN-04.S1-S3) |
| 15 | `install.sh:44` | Delete a retired folder without the phrase check | ✅ Killed (FLOW-01.S2) |
| 16 | `install.sh:44` | Follow a symlinked retired skill and delete it | ✅ Killed (FLOW-01.S3) |
| 17 | `install.sh:23` | Drop `wizard` from `RETIRED_SKILLS` | ✅ Killed (FLOW-01.S1) |
| 18 | `install.sh:45` | Skip the `rm -rf` of a matching retired folder | ✅ Killed (FLOW-01.S1) |

**Sensor depth**: expanded (18 manual mutations across all four scripts and the installer, covering every new branch)
**Result**: 17/17 non-equivalent mutants killed, 1 equivalent survivor - PASS ✅

---

## Interactive UAT Results

Skipped on the orchestrator's instruction. The feature is prompts, scripts and an installer with no interactive UI; the `inspect` rows above are the human-judgment proof.

---

## Code Quality

| Principle        | Status |
| ---------------- | ------ |
| Minimum code     | ✅ script changes are small additions (`find_tables`, `spec_is_native`, `parse_tickets`/`ticket_problems`, `foreign_target`) reused across the three validators and `prep_review.py` |
| Surgical changes | ✅ diff stays within the Tasks' `Where` files; retired skill folders deleted only in T30 |
| No scope creep   | ✅ no behavior beyond the Scenarios found |
| Matches patterns | ✅ same argparse/error-list style as the existing scripts; tests are stdlib `unittest` with `.md` fixtures |
| Spec-anchored outcome check (asserted values match spec) | ✅ every test asserts the exit code and the exact named token from the Then step; most also pin the error count |
| Per-layer Coverage Expectation met | ✅ every script and installer Scenario has one integration test; `inspect` covers prose and the `fd` warning by design |
| Every test proves exactly one Scenario - no Unclaimed Tests touched | ✅ `validate_scenarios.py --since abd3b89` reports 0 errors |
| Behavior Tests, not Implementation-Coupled | ✅ scripts run as subprocesses against fixture git repos; installer runs against temp config dirs |
| Repo Standards + Smell Baseline: `docs/adr/0001-0003` (legacy) and `D-grill-in-spec-driven.*` | ✅ |

Minor observations (not gaps; no Scenario requires them):

1. `skills/prototype/UI.md:100-105` still says "Fold the winner into the real code" and "promote the winning variant to a real route", and `skills/prototype/LOGIC.md:24` says the module "could be lifted out and dropped into the real codebase later". `skills/prototype/SKILL.md:34` explicitly overrides both ("This rule ... comes before anything LOGIC.md or UI.md says"), so FLOW-06.S1 holds, but the sub-files still read as a contradiction on their own. Rewording them would remove the reliance on the precedence clause.
2. `validate_scenarios.py` ignores Scenario-Anchored rows whose ID the spec does not define; `validate.md:54` lists "an unknown ID" among the errors. It is unclear whether that line means test claims only (which are checked) or table rows too.
3. `validate_tasks.py` `ticket_problems` does not flag a Ticket that lists a task ID with no matching `T<n>` heading.
4. `validate_tasks.py` treats a `tasks.md` with no `spec.md` beside it as legacy (Ticket rules only warn). Harmless today, because `prep_review.py` stops without `spec.md`.
5. `install.sh:16` now removes `tlc-spec-driven` only when its `SKILL.md` contains `name: tlc-spec-driven`. Before this change it was removed unconditionally. This matches the new provenance rule (D-grill-in-spec-driven.35).

---

## Edge Cases

- [x] EDGE-01 (legacy `docs/adr/` at the root and per context, with or without a map): stated in `skills/tdd/SKILL.md:22-23` and `skills/spec-driven/references/decisions.md:81-96`
- [x] EDGE-02 (a non-feature record becomes a feature): stated in `skills/spec-driven/references/specify.md:136-140` and `skills/grill-with-docs/SKILL.md:38`
- [x] Implicit-requirement sweep rows: broken `summary.md` (READ-05), empty cells (GRILL-09), slug taken (REC-01.S2), resumed draft (REC-10), tracker failure and retry (TKT-06.S2/S3), `fd` missing (READ-03/04) are all proven above

---

## Gate Check

- **Gate commands** (from `tasks.md` Gate Check Commands):
  - quick: `python3 -m unittest discover -s tests -v` → exit 0
  - build: `bash -n install.sh && node --check render-adapters.js && python3 -m py_compile skills/spec-driven/scripts/*.py` → exit 0
  - plan: `validate_spec.py integrate-skills --root .` → exit 0 (0 errors, 0 warnings); `validate_tasks.py integrate-skills --root .` → exit 0 (0 errors, 23 warnings: granularity smells on multi-file `Where` fields and `Tests: none` confirmations, all consistent with the Test Coverage Matrix)
  - scenarios: `validate_scenarios.py integrate-skills --root . --since abd3b89` → exit 1 before this report (50 errors, all "inspect Scenario has no proof" as expected), exit 0 after it
- **Tests**: 31 passed, 0 failed, 0 skipped (real `graphify` on PATH)
- **Test count before feature**: 0 (`tests/` did not exist at `abd3b89`)
- **Test count after feature**: 31
- **Delta**: +31 new tests, one per `test` Scenario
- **Skipped tests**: none
- **Failures**: none

---

## Fix Plans

None. No gaps found in this round, so no fix Ticket is needed.

---

## Requirement Traceability Update

The orchestrator should update `spec.md` (the Verifier edits only this report):

| Requirement | Previous Status | New Status |
| ----------- | --------------- | ---------- |
| GRILL-01 to GRILL-10 | Pending | ✅ Verified |
| REC-01 to REC-10 | Pending | ✅ Verified |
| READ-01 to READ-06 | Pending | ✅ Verified |
| REV-01 to REV-06 | Pending | ✅ Verified |
| TKT-01 to TKT-09 | Pending | ✅ Verified |
| PLAN-01 to PLAN-05 | Pending | ✅ Verified |
| PROOF-01, PROOF-02 | Pending | ✅ Verified |
| FLOW-01 to FLOW-06 | Pending | ✅ Verified |
| EDGE-01, EDGE-02 | Pending | ✅ Verified |

Success Criteria greps: `ready-for-agent|agent-grabbable` in skills/agents → none; `into the real code` in `skills/prototype/SKILL.md` → none; `superseded|Amendments` in skills/agents → none; `ls skills/wizard` fails, and `wizard` appears only at `install.sh:23` (the `RETIRED_SKILLS` entry); `docs/adr` in skills/agents appears only in legacy-read instructions.

---

## Summary

**Overall**: ✅ Ready

**Spec-anchored check**: 81/81 Scenarios matched their spec outcome (31 `test`, 50 `inspect`); 0 spec-precision gaps
**Sensor**: 17/17 non-equivalent mutations killed (1 equivalent survivor)
**Gate**: 31 passed, 0 failed

**What works**: inspect proofs in `validate_scenarios.py`; the Decisions & Assumptions and Ticket checks with legacy warnings; review snapshots of records and glossaries; the foreign-plan review path; the provenance-checked installer retirement; and the merged grill, record, read-rule, Ticket, publishing and single-path prose across spec-driven, grilling, domain-modeling, tdd, diagnosing-bugs, prototype, grill-with-docs and both reviewer agents.

**Issues found**: none blocking. Optional clean-ups are listed under Code Quality.

**Next steps**: orchestrator commits this report, updates spec traceability, and tells the human `/code-review` is available. Lessons distillation (validate.md section 10) was skipped on the orchestrator's instruction.

**Closing gates (run after writing this report)**: `validate_scenarios.py integrate-skills --root . --since abd3b89` → exit 0; `validate_state.py integrate-skills` → exit 0.
