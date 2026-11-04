# Integrate Skills Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `spec-driven` skill: **activate it by name and follow its Execute flow and Critical Rules.** Do not search for skill files by filesystem path. The skill is the source of truth for the full flow (Execution Approval, per-task cycle, sub-agent delegation, adequacy review, Verifier, discrimination sensor).

**Do not start before Execution Approval:** a `/spec-review` ran, its Findings have Dispositions, and the human said to execute.

**If the skill cannot be activated, STOP and tell the user - do not proceed without it.**

**Note for this feature:** the installed spec-driven still follows the old rules (D-0001.27). Where the old skill and this plan disagree (Tickets, `Decisions & Assumptions`, no `context.md`), this plan wins; the tasks below implement the new rules.

---

**Spec**: `.specs/features/integrate-skills/spec.md`
**Design**: `.specs/features/integrate-skills/design.md`
**Grilling Record**: `.specs/decisions/0001-integrate-grill-into-spec-driven.md`
**Status**: Draft

---

## Test Coverage Matrix

Provenance: no testing guidelines in the repo (no `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING*`, test config) and no existing tests (`find . -name 'test_*.py'` → none). Strong default applied, shaped by D-0001.30.

| Layer | Example paths | Test type | Coverage Expectation | Proven by |
| --- | --- | --- | --- | --- |
| Deterministic scripts | `skills/spec-driven/scripts/validate_spec.py`, `validate_tasks.py`, `prep_review.py` | integration (`unittest`, fixture repo in a temp dir, script run as a subprocess) | every automated Scenario of the script, 1:1 | `tests/test_*.py` |
| Installer | `install.sh` | integration (`unittest`, temp `CLAUDE_CONFIG_DIR`/`OPENCODE_CONFIG_DIR`, stub `graphify`/`uv` on PATH) | every automated Scenario of the installer, 1:1 | `tests/test_install.py` |
| Skill and agent prose | `skills/**/SKILL.md`, `skills/**/references/*.md`, `agents/*.md` | uat | every agent-behavior Scenario walked once by the Verifier and recorded in `validation.md` | `validation.md` UAT table |

## Gate Check Commands

| Gate | Command | Used by |
| --- | --- | --- |
| quick | `python3 -m unittest discover -s tests -v` | script and installer tasks |
| scenarios | `python3 skills/spec-driven/scripts/validate_scenarios.py integrate-skills --root . --only <the task's Scenario IDs>` | script and installer tasks |
| build | `bash -n install.sh && node --check render-adapters.js && python3 -m py_compile skills/spec-driven/scripts/*.py` | every task |
| plan | `python3 skills/spec-driven/scripts/validate_spec.py integrate-skills --root . && python3 skills/spec-driven/scripts/validate_tasks.py integrate-skills --root .` | every task after T3 |
| full | quick + build + plan | prose tasks (regression only; behavior is proven by UAT) |

Before T2 lands, `validate_spec.py` reports one expected error on this spec (the renamed section). Before T3 lands, `validate_tasks.py` ignores the Tickets section.

---

## Tickets

### K1: Validators understand the new plan shape
**Delivers**: `validate_spec.py` accepts and requires "Decisions & Assumptions" at every scope; `validate_tasks.py` checks Tickets. This plan then passes both gates.
**Covers**: GRILL-05, GRILL-06, TKT-03, TKT-04, TKT-05 · GRILL-05.S1, GRILL-05.S2, GRILL-06.S1, TKT-03.S1, TKT-04.S1, TKT-05.S1
**Blocked by**: none
**Tasks**: T1, T2, T3

### K2: Review prep and installer follow the new rules
**Delivers**: `/spec-review` snapshots records and the glossary, lists the feature's Grilling Records, and stops on missing plan files; `install.sh` removes retired skills and warns about `fd`.
**Covers**: REV-01, REV-02, TKT-01, TKT-02, FLOW-01, READ-04 · REV-01.S1, REV-02.S1, TKT-01.S1, TKT-02.S1, TKT-02.S2, FLOW-01.S1, READ-04.S1
**Blocked by**: K1
**Tasks**: T4, T5, T6

### K3: Grill, record and read rule exist as skills
**Delivers**: vendored `grilling`, the Grilling Record and `summary.md` formats in domain-modeling, the shared read rule with `fd` discovery, and `setup-spec-driven`.
**Covers**: GRILL-01, GRILL-02, GRILL-03, REC-01, REC-02, REC-03, REC-04, REC-07, READ-01, READ-02, READ-03, EDGE-01, FLOW-02 · GRILL-01.S1, GRILL-02.S1, GRILL-03.S1, REC-01.S1, REC-02.S1, REC-03.S1, REC-04.S1, REC-07.S1, READ-01.S1, READ-02.S1, READ-03.S1, EDGE-01.S1, FLOW-02.S1
**Blocked by**: K2
**Tasks**: T7, T8, T9, T10

### K4: spec-driven plans the new way
**Delivers**: Specify grills, Design writes into the record at Medium+, Tasks always produces day-sized Tickets, and Tickets can be published on a go-ahead.
**Covers**: GRILL-04, GRILL-07, GRILL-08, EDGE-02, REC-06, REC-08, TKT-06, TKT-07, TKT-08 · GRILL-04.S1, GRILL-07.S1, GRILL-08.S1, EDGE-02.S1, REC-06.S1, REC-08.S1, TKT-06.S1, TKT-07.S1, TKT-08.S1
**Blocked by**: K3
**Tasks**: T11, T12, T13, T14, T15, T16

### K5: Execute and reviews use the records
**Delivers**: Execute runs the tdd loop and leaves `/code-review` to the human; Dispositions write Amendments; both reviewers check against the records.
**Covers**: FLOW-03, FLOW-05, REC-05, REV-03, REV-04, REV-05, REV-06 · FLOW-03.S1, FLOW-05.S1, REC-05.S1, REV-03.S1, REV-04.S1, REV-05.S1, REV-06.S1
**Blocked by**: K4
**Tasks**: T17, T18, T19, T20, T21

### K6: No side doors, no leftovers
**Delivers**: diagnosing-bugs hands off, grill-with-docs and improve-codebase-architecture write records, retired skills are gone, and the README describes the new flow.
**Covers**: FLOW-04, REC-09 · FLOW-04.S1, REC-09.S1
**Blocked by**: K5
**Tasks**: T22, T23, T24, T25

---

## Execution Plan

Each phase is one Ticket. Phases run in order; tasks within a phase run in order.

### Phase 1: K1 Validators

```
T1 → T2 → T3
```

### Phase 2: K2 Review prep and installer

```
T4 → T5 → T6
```

### Phase 3: K3 Grill, record and read rule

```
T7 → T8 → T9 → T10
```

### Phase 4: K4 Planning phases

```
T11 → T12 → T13 → T14 → T15 → T16
```

### Phase 5: K5 Execute and reviews

```
T17 → T18 → T19 → T20 → T21
```

### Phase 6: K6 Side doors and cleanup

```
T22 → T23 → T24 → T25
```

---

## Task Breakdown

### Phase 1: K1 Validators

#### T1: Add the fixture-repository test helper

**What**: `tests/fixtures.py` with a helper that builds a throwaway git repository in a temp dir (spec, tasks, design, records, summary) and runs a script as a subprocess, returning exit code and output.
**Where**: `tests/fixtures.py`
**Depends on**: None
**Reuses**: fixture layout used to smoke-test the scripts in the previous feature (scratch repo with `.specs/features/<f>/`)
**Requirement**: GRILL-05, TKT-01 (infrastructure for their tests)

**Done when**:
- [ ] `python3 -c "import sys; sys.path.insert(0, 'tests'); import fixtures"` succeeds
- [ ] Gate check passes: build

**Tests**: none (test infrastructure; proves no Scenario)
**Scenarios**: none - this task writes no tests
**Gate**: build

**Commit**: `test: add fixture repository helper for script tests`

---

#### T2: Rename and require "Decisions & Assumptions" in validate_spec.py

**What**: replace "Assumptions & Open Questions" with "Decisions & Assumptions" in both required-section lists, read the new table (Choice and Rationale cells filled), accept a section whose body is `none`.
**Where**: `skills/spec-driven/scripts/validate_spec.py` (tests in `tests/test_validate_spec.py`)
**Depends on**: T1
**Reuses**: `section_bounds`, `split_row`, `REQUIRED_SECTIONS` in the same file
**Requirement**: GRILL-05, GRILL-06

**Done when**:
- [ ] the three Scenario tests pass and carry their Scenario text verbatim
- [ ] `validate_spec.py integrate-skills` exits 0 on this feature
- [ ] Gate check passes: quick, scenarios, build

**Tests**: integration
**Scenarios**: GRILL-05.S1, GRILL-05.S2, GRILL-06.S1
**Gate**: quick

**Commit**: `feat(spec-driven): require Decisions & Assumptions in every spec`

---

#### T3: Check Tickets in validate_tasks.py

**What**: add `Tickets` to the required sections and a Ticket pass: parse `### K<n>:` blocks and their `**Tasks**` and `**Blocked by**` fields; error when a task is in no Ticket, in more than one, or when Blocked by names a later Ticket.
**Where**: `skills/spec-driven/scripts/validate_tasks.py` (tests in `tests/test_validate_tasks.py`)
**Depends on**: T2
**Reuses**: `parse_tasks`, `TASK_RE`, the error/warning reporting in `check`
**Requirement**: TKT-03, TKT-04, TKT-05

**Done when**:
- [ ] the three Scenario tests pass
- [ ] `validate_tasks.py integrate-skills` exits 0 on this file
- [ ] Gate check passes: quick, scenarios, build, plan

**Tests**: integration
**Scenarios**: TKT-03.S1, TKT-04.S1, TKT-05.S1
**Gate**: quick

**Commit**: `feat(spec-driven): check Ticket membership and blocking order in tasks.md`

---

### Phase 2: K2 Review prep and installer

#### T4: Snapshot records and glossary; list the feature's records in prep_review.py

**What**: add `.specs/decisions/` and `CONTEXT.md` to the plan paths the pre-review commit protects; read `summary.md` and list records whose Specs names the feature; drop `context.md` and the `STATE.md` decisions line from the Review context.
**Where**: `skills/spec-driven/scripts/prep_review.py` (tests in `tests/test_prep_review.py`)
**Depends on**: T3
**Reuses**: `prep_spec`, `dirty_paths`, `must_git`
**Requirement**: REV-01, REV-02

**Done when**:
- [ ] both Scenario tests pass
- [ ] Gate check passes: quick, scenarios, build, plan

**Tests**: integration
**Scenarios**: REV-01.S1, REV-02.S1
**Gate**: quick

**Commit**: `feat(spec-driven): snapshot Grilling Records and glossary before spec review`

---

#### T5: Stop review prep on missing plan files

**What**: in `prep_spec`, raise `Stop` when `tasks.md` is missing at any scope, or `design.md` is missing at Medium, Large or Complex.
**Where**: `skills/spec-driven/scripts/prep_review.py` (tests in `tests/test_prep_review.py`)
**Depends on**: T4
**Reuses**: `spec_scope` from `scenarios_lib.py`; the existing `Stop` exception
**Requirement**: TKT-01, TKT-02

**Done when**:
- [ ] the three Scenario tests pass
- [ ] Gate check passes: quick, scenarios, build, plan

**Tests**: integration
**Scenarios**: TKT-01.S1, TKT-02.S1, TKT-02.S2
**Gate**: quick

**Commit**: `feat(spec-driven): require tasks.md always and design.md at Medium+ before review`

---

#### T6: Retire skills and warn about fd in install.sh

**What**: extend `RETIRED_SKILLS` with `ask-matt implement to-spec to-tickets triage wayfinder setup-matt-pocock-skills`; print a warning when `fd` is not on PATH and continue.
**Where**: `install.sh` (tests in `tests/test_install.py`)
**Depends on**: T5
**Reuses**: the `RETIRED_SKILLS` removal loop at `install.sh:24-28`; the graphify presence check style at `install.sh:50`
**Requirement**: FLOW-01, READ-04

**Done when**:
- [ ] both Scenario tests pass, with stub `graphify` and `uv` on PATH and temp config dirs
- [ ] Gate check passes: quick, scenarios, build, plan

**Tests**: integration
**Scenarios**: FLOW-01.S1, READ-04.S1
**Gate**: quick

**Commit**: `feat(install): remove retired skills and warn when fd is missing`

---

### Phase 3: K3 Grill, record and read rule

#### T7: Vendor and extend the grilling skill

**What**: copy the synced `grilling` text into the repo and add the "you decide" and "decide the rest" escapes and the Binds-in-recommendation rule; add `agents/openai.yaml`.
**Where**: `skills/grilling/SKILL.md`
**Depends on**: T6
**Reuses**: `~/.claude/skills/synced/*/grilling/SKILL.md`; `skills/grill-with-docs/agents/openai.yaml` as the yaml pattern
**Requirement**: GRILL-01, GRILL-02, GRILL-03

**Done when**:
- [ ] the skill states one question per turn with options and a recommendation, both escapes, and Binds in the recommendation
- [ ] Gate check passes: full

**Tests**: uat
**Scenarios**: GRILL-01.S1, GRILL-02.S1, GRILL-03.S1
**Gate**: full

**Commit**: `feat(grilling): vendor the grilling skill with decision escapes`

---

#### T8: Grilling Record and summary formats in domain-modeling

**What**: replace `ADR-FORMAT.md` with `GRILLING-RECORD-FORMAT.md` (record and `summary.md` templates, completeness rules in prose, numbering, incremental writing, legacy lines, Amendments and Design sections); rewrite `SKILL.md` to write records instead of offering ADRs.
**Where**: `skills/domain-modeling/GRILLING-RECORD-FORMAT.md`, `skills/domain-modeling/SKILL.md`, `skills/domain-modeling/ADR-FORMAT.md` (deleted)
**Depends on**: T7
**Reuses**: `.specs/decisions/0001-integrate-grill-into-spec-driven.md` and `summary.md` as the worked example
**Requirement**: REC-01, REC-02, REC-03, REC-04, REC-07

**Done when**:
- [ ] no file in `skills/domain-modeling/` tells the agent to write an ADR
- [ ] the template marks every section required and says a record covers the whole session
- [ ] Gate check passes: full

**Tests**: uat
**Scenarios**: REC-01.S1, REC-02.S1, REC-03.S1, REC-04.S1, REC-07.S1
**Gate**: full

**Commit**: `feat(domain-modeling): replace ADRs with complete Grilling Records`

---

#### T9: Write the shared read rule and discovery reference

**What**: `references/decisions.md` with discovery (two `fd` commands, stop-and-ask when `fd` is missing), the `summary.md` row filter, the legacy check, the Binds test, and "cite outside sources used".
**Where**: `skills/spec-driven/references/decisions.md`
**Depends on**: T8
**Reuses**: D-0001.17, D-0001.18, D-0001.19 text from the Grilling Record
**Requirement**: READ-01, READ-02, READ-03, EDGE-01

**Done when**:
- [ ] the file holds the exact fd commands from D-0001.18 and the filter from D-0001.17
- [ ] Gate check passes: full

**Tests**: uat
**Scenarios**: READ-01.S1, READ-02.S1, READ-03.S1, EDGE-01.S1
**Gate**: full

**Commit**: `feat(spec-driven): add the shared Decision read rule and repo discovery`

---

#### T10: Rename setup-matt-pocock-skills to setup-spec-driven

**What**: `git mv` the directory; drop Section B and `triage-labels.md`; point the domain docs section and `domain.md` at `.specs/decisions/`; rewrite names and descriptions; add an `install.sh` test for the new skills.
**Where**: `skills/setup-spec-driven/` (tests in `tests/test_install.py`)
**Depends on**: T9
**Reuses**: `skills/setup-matt-pocock-skills/` contents
**Requirement**: FLOW-02

**Done when**:
- [ ] no file under `skills/setup-spec-driven/` mentions triage labels, ADRs or matt-pocock
- [ ] the FLOW-02 test passes
- [ ] Gate check passes: quick, scenarios, build, plan

**Tests**: integration
**Scenarios**: FLOW-02.S1
**Gate**: quick

**Commit**: `refactor(setup): rename setup-matt-pocock-skills to setup-spec-driven`

---

### Phase 4: K4 Planning phases

#### T11: Specify runs the grill

**What**: rewrite `specify.md` steps 1-2: pre-question steps (lessons, `decisions.md`, capability search, Standards), call `grilling` and `domain-modeling` by name with the sibling-path fallback, dimensions sweep as closing branches, incremental record, spec written after shared understanding; update both templates (Decisions & Assumptions table, Deferred Ideas in Out of Scope, optional References); continue an existing non-feature record when one exists; delete `discuss.md`.
**Where**: `skills/spec-driven/references/specify.md`, `skills/spec-driven/references/discuss.md` (deleted)
**Depends on**: T10
**Reuses**: current `specify.md` steps 3-4 (EARS, Scenarios, closure gate) unchanged
**Requirement**: GRILL-04, GRILL-07, GRILL-08, EDGE-02

**Done when**:
- [ ] no reference in `skills/spec-driven/` points at `discuss.md` or `context.md`
- [ ] Gate check passes: full

**Tests**: uat
**Scenarios**: GRILL-04.S1, GRILL-07.S1, GRILL-08.S1, EDGE-02.S1
**Gate**: full

**Commit**: `feat(spec-driven): Specify grills and writes a Grilling Record`

---

#### T12: Design writes into the Grilling Record

**What**: Design is required at Medium+; it reads via `decisions.md`; asks grill-style questions; appends a `## Design` section; Tech Decisions become links; the supersede flow goes through records instead of `AD-NNN`.
**Where**: `skills/spec-driven/references/design.md`
**Depends on**: T11
**Reuses**: current template sections (reuse table, components, risks)
**Requirement**: REC-06, REC-08

**Done when**:
- [ ] no instruction in `design.md` writes to `STATE.md` or `docs/adr/`
- [ ] Gate check passes: full

**Tests**: uat
**Scenarios**: REC-06.S1, REC-08.S1
**Gate**: full

**Commit**: `feat(spec-driven): Design records its Decisions in the Grilling Record`

---

#### T13: Tasks always runs and slices Tickets first

**What**: remove the skip rule; slice the Spec into Tickets (D-0001.23, markup D-0001.31) before cutting Tasks; document the `## Tickets` section in the template and the Ticket checks in step 5.
**Where**: `skills/spec-driven/references/tasks.md`
**Depends on**: T12
**Reuses**: current Tasks process and template
**Requirement**: TKT-08

**Done when**:
- [ ] the template's Tickets section matches what `validate_tasks.py` checks
- [ ] Gate check passes: full

**Tests**: uat
**Scenarios**: TKT-08.S1
**Gate**: full

**Commit**: `feat(spec-driven): Tasks runs at every scope and slices day-sized Tickets`

---

#### T14: Ticket slicing and publishing reference

**What**: `references/tickets.md`: one-day vertical slices, expand–contract for wide refactors, publishing per tracker (from `docs/agents/issue-tracker.md` written by `setup-spec-driven`), the Dispositions gate, ID write-back, drift listing.
**Where**: `skills/spec-driven/references/tickets.md`
**Depends on**: T13
**Reuses**: `skills/to-tickets/SKILL.md` sections 3 and 5; `skills/setup-spec-driven/issue-tracker-*.md`
**Requirement**: TKT-06, TKT-07

**Done when**:
- [ ] it states that publishing needs an explicit "publish tickets" after all Dispositions of the latest Spec Review
- [ ] Gate check passes: full

**Tests**: uat
**Scenarios**: TKT-06.S1, TKT-07.S1
**Gate**: full

**Commit**: `feat(spec-driven): add Ticket slicing and publishing`

---

#### T15: Update the spec-driven SKILL.md

**What**: flow line, auto-sizing table (Tasks at every scope, Design at Medium+), `.specs` tree (`decisions/`, no `context.md`), commands table (publish tickets; Discuss removed; decisions.md), Critical Rules (implementation only through spec-driven; Tickets published only on go-ahead), Knowledge Verification Chain step 2 (records instead of `STATE.md`).
**Where**: `skills/spec-driven/SKILL.md`
**Depends on**: T14
**Reuses**: current SKILL.md structure
**Requirement**: GRILL-07, TKT-08 (entry-point wording)

**Done when**:
- [ ] SKILL.md mentions neither `context.md` nor the safety valve
- [ ] Gate check passes: full

**Tests**: none (entry-point wording; its Scenarios are proven by T11 and T13)
**Scenarios**: none - this task writes no tests
**Gate**: full

**Commit**: `docs(spec-driven): describe the merged flow in SKILL.md`

---

#### T16: Memory, standards and writing references follow the records

**What**: `memory.md` keeps only `## Handoff` and points Decisions at `decisions.md`; `standards.md` §1 lists active project Decisions as Repo Standards and uses discovery; `coding-principles.md` drops ADR wording.
**Where**: `skills/spec-driven/references/memory.md`, `skills/spec-driven/references/standards.md`, `skills/spec-driven/references/coding-principles.md`
**Depends on**: T15
**Reuses**: current files
**Requirement**: READ-01 (Repo Standard wording)

**Done when**:
- [ ] no instruction in these files writes `AD-NNN` or ADRs
- [ ] Gate check passes: full

**Tests**: none (wording; READ-01 is proven by T9)
**Scenarios**: none - this task writes no tests
**Gate**: full

**Commit**: `docs(spec-driven): point memory and standards at Grilling Records`

---

### Phase 5: K5 Execute and reviews

#### T17: Execute ends at the Verifier and leaves /code-review to the human

**What**: in `implement.md`: drop the safety valve; call `tdd` per Task; deferred ideas are surfaced and become Out of Scope rows only on a go-ahead; after the Verifier passes, say `/code-review` is available and never run it.
**Where**: `skills/spec-driven/references/implement.md`
**Depends on**: T16
**Reuses**: current per-task cycle and Verifier section
**Requirement**: FLOW-05

**Done when**:
- [ ] no instruction in `implement.md` runs `/code-review` or edits `context.md`
- [ ] Gate check passes: full

**Tests**: uat
**Scenarios**: FLOW-05.S1
**Gate**: full

**Commit**: `feat(spec-driven): Execute runs tdd per Task and leaves /code-review to the human`

---

#### T18: tdd becomes Execute's per-Task loop

**What**: description and intro say it is the test-first loop spec-driven Execute runs; seams come from Scenarios and Design, asking only for unnamed interfaces; the ADR line becomes a link to `decisions.md`.
**Where**: `skills/tdd/SKILL.md`
**Depends on**: T17
**Reuses**: current tdd content (tests.md, mocking.md unchanged)
**Requirement**: FLOW-03

**Done when**:
- [ ] the description no longer offers to build features on its own
- [ ] Gate check passes: full

**Tests**: uat
**Scenarios**: FLOW-03.S1
**Gate**: full

**Commit**: `feat(tdd): run as the per-Task loop inside spec-driven Execute`

---

#### T19: Dispositions write Amendments

**What**: in `review.md`, after recording Dispositions, append Amendments for Findings that change Decisions and update `summary.md`; add the publish-tickets gate; in `finding-format.md`, replace `AD-NNN` inputs with Grilling Records.
**Where**: `skills/spec-driven/references/review.md`, `skills/spec-driven/references/finding-format.md`
**Depends on**: T18
**Reuses**: current "After a reviewer returns" steps
**Requirement**: REC-05

**Done when**:
- [ ] step order: record Dispositions, write Amendments, commit, distill Lessons
- [ ] Gate check passes: full

**Tests**: uat
**Scenarios**: REC-05.S1
**Gate**: full

**Commit**: `feat(spec-driven): record Amendments when a Disposition changes a Decision`

---

#### T20: spec-reviewer checks the plan against the Grilling Record

**What**: read via `decisions.md` (records, discovery, legacy); add the Thought Partnership, Truthful Reporting, Practical Judgment and Communication checks from D-0001.20.
**Where**: `agents/spec-reviewer.md`
**Depends on**: T19
**Reuses**: current "Read first" and "What to check" sections
**Requirement**: REV-03, REV-04, REV-05

**Done when**:
- [ ] the agent no longer reads `context.md` or `AD-NNN` as primary sources
- [ ] Gate check passes: full

**Tests**: uat
**Scenarios**: REV-03.S1, REV-04.S1, REV-05.S1
**Gate**: full

**Commit**: `feat(agents): spec-reviewer checks plans against Grilling Records`

---

#### T21: change-reviewer checks the Change against active Decisions

**What**: read via `decisions.md`; flag a Change contradicting an active Decision without an Amendment, and a silent departure from a `Decided by: user` choice as a false Claim.
**Where**: `agents/change-reviewer.md`
**Depends on**: T20
**Reuses**: current "Read first" and "What to check" sections
**Requirement**: REV-06

**Done when**:
- [ ] the agent no longer reads `AD-NNN` as a primary source
- [ ] Gate check passes: full

**Tests**: uat
**Scenarios**: REV-06.S1
**Gate**: full

**Commit**: `feat(agents): change-reviewer checks Changes against active Decisions`

---

### Phase 6: K6 Side doors and cleanup

#### T22: diagnosing-bugs hands off to Specify

**What**: Phase 5 becomes a hand-off of the repro, root cause and seam to a Small Specify; the ADR line becomes a link to `decisions.md`.
**Where**: `skills/diagnosing-bugs/SKILL.md`
**Depends on**: T21
**Reuses**: Phases 1-4 unchanged
**Requirement**: FLOW-04

**Done when**:
- [ ] no instruction in the skill applies a fix
- [ ] Gate check passes: full

**Tests**: uat
**Scenarios**: FLOW-04.S1
**Gate**: full

**Commit**: `feat(diagnosing-bugs): hand confirmed root causes to spec-driven`

---

#### T23: grill-with-docs and improve-codebase-architecture write Grilling Records

**What**: `grill-with-docs` (+ openai.yaml) describes writing a Grilling Record and `CONTEXT.md` and points features at spec-driven; `improve-codebase-architecture` (+ `HTML-REPORT.md`, openai.yaml) treats active Decisions as it treated ADRs and records rejections in its record.
**Where**: `skills/grill-with-docs/SKILL.md`, `skills/improve-codebase-architecture/SKILL.md`, `skills/improve-codebase-architecture/HTML-REPORT.md`
**Depends on**: T22
**Reuses**: current texts
**Requirement**: REC-09

**Done when**:
- [ ] neither skill mentions writing or offering an ADR
- [ ] Gate check passes: full

**Tests**: uat
**Scenarios**: REC-09.S1
**Gate**: full

**Commit**: `feat(skills): grill-with-docs and architecture reviews write Grilling Records`

---

#### T24: Delete the retired skills

**What**: `git rm -r` `skills/ask-matt`, `skills/implement`, `skills/to-spec`, `skills/to-tickets`, `skills/triage`, `skills/wayfinder` and `skills/engineering-README.md`.
**Where**: `skills/` (seven paths)
**Depends on**: T23
**Reuses**: none
**Requirement**: FLOW-01 (source side; installed copies handled by T6)

**Done when**:
- [ ] `grep -rn "ask-matt\|to-tickets\|to-spec\|triage\|wayfinder\|/implement" skills agents` finds nothing outside historical records
- [ ] Gate check passes: full

**Tests**: none (deletion; FLOW-01 is proven by T6)
**Scenarios**: none - this task writes no tests
**Gate**: full

**Commit**: `refactor(skills): remove retired skills`

---

#### T25: Rewrite the README for the merged flow

**What**: skill table, flow description (Specify grill, Design at Medium+, Tasks and Tickets, reviews, Execute with tdd, Verifier, `/code-review`), `.specs/decisions/`, `fd` requirement, attribution as "based on mattpocock/skills", no `engineering-README.md`.
**Where**: `README.md`
**Depends on**: T24
**Reuses**: current README sections
**Requirement**: none (documentation)

**Done when**:
- [ ] the README lists no retired skill as installed
- [ ] Gate check passes: full

**Tests**: none (documentation)
**Scenarios**: none - this task writes no tests
**Gate**: full

**Commit**: `docs: describe the merged spec-driven flow in the README`

---

## Task Granularity Check

| Task | Scope | Status |
| --- | --- | --- |
| T1 | 1 helper module | ✅ Granular |
| T2, T3, T4, T5 | 1 script change each | ✅ Granular |
| T6 | 1 installer change | ✅ Granular |
| T7, T9, T11-T15, T17-T22, T25 | 1 file each (T11 also deletes `discuss.md`, T19 touches the format file it depends on) | ✅ Granular |
| T8 | 1 skill's format (new file + SKILL.md + one deletion) | ⚠️ Multi-file, one concept |
| T10 | 1 directory rename | ⚠️ Multi-file, one concept |
| T16 | 3 small wording updates | ⚠️ Multi-file, one concept |
| T23 | 2 skills, same change | ⚠️ Multi-file, one concept |
| T24 | 7 deletions | ⚠️ Multi-file, one concept |

## Diagram-Definition Cross-Check

| Task | Depends on (definition) | Diagram arrow | Match |
| --- | --- | --- | --- |
| T1 | None | start of Phase 1 | ✅ |
| T2 | T1 | T1 → T2 | ✅ |
| T3 | T2 | T2 → T3 | ✅ |
| T4 | T3 | start of Phase 2 (cross-phase) | ✅ |
| T5 | T4 | T4 → T5 | ✅ |
| T6 | T5 | T5 → T6 | ✅ |
| T7 | T6 | start of Phase 3 (cross-phase) | ✅ |
| T8-T10 | previous task | chain | ✅ |
| T11 | T10 | start of Phase 4 (cross-phase) | ✅ |
| T12-T16 | previous task | chain | ✅ |
| T17 | T16 | start of Phase 5 (cross-phase) | ✅ |
| T18-T21 | previous task | chain | ✅ |
| T22 | T21 | start of Phase 6 (cross-phase) | ✅ |
| T23-T25 | previous task | chain | ✅ |

## Test Co-location Validation

| Task | Layer | Matrix requires | Task Tests | Status |
| --- | --- | --- | --- | --- |
| T1 | test infrastructure | none | none | ✅ |
| T2-T5 | deterministic scripts | integration | integration | ✅ |
| T6, T10 | installer | integration | integration | ✅ |
| T7-T9, T11-T14, T17-T23 | skill and agent prose | uat | uat | ✅ |
| T15, T16, T24, T25 | prose with no own Scenario | none | none | ✅ |
