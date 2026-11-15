# Integrate Skills Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `spec-driven` skill: **activate it by name and follow its Execute flow and Critical Rules.** Do not search for skill files by filesystem path. The skill is the source of truth for the full flow (Execution Approval, per-task cycle, sub-agent delegation, adequacy review, Verifier, discrimination sensor).

**Do not start before Execution Approval:** a `/spec-review` ran, its Findings have Dispositions, and the human said to execute.

**If the skill cannot be activated, STOP and tell the user - do not proceed without it.**

**Note for this feature:** the installed spec-driven still follows the old rules (D-grill-in-spec-driven.27). Where the old skill and this plan disagree (Tickets, `Decisions & Assumptions`, no `context.md`, `inspect` proofs, plan kinds), this plan wins; the tasks below implement the new rules. In particular, until T2 lands the per-Task Scenario gate passes only the Task's `test` Scenario IDs, and `inspect` Scenarios are left to the Verifier.

---

**Spec**: `.specs/features/integrate-skills/spec.md`
**Design**: `.specs/features/integrate-skills/design.md`
**Grilling Record**: `.specs/decisions/grill-in-spec-driven.md`
**Spec Reviews**: `.specs/features/integrate-skills/spec-review-1.md`, `.specs/features/integrate-skills/spec-review-2.md` (Dispositions applied)
**Status**: Draft

---

## Test Coverage Matrix

Provenance: no testing guidelines in the repo (no `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING*`, test config) and no existing tests (`find . -name 'test_*.py'` → none). Strong default applied, shaped by D-grill-in-spec-driven.38 and D-grill-in-spec-driven.42.

| Layer | Example paths | Test type | Proof type | Coverage Expectation | Proven by |
| --- | --- | --- | --- | --- | --- |
| Deterministic scripts | `skills/spec-driven/scripts/validate_spec.py`, `validate_tasks.py`, `validate_scenarios.py`, `prep_review.py` | integration (`unittest`, fixture repo in a temp dir, script run as a subprocess, real `graphify` on PATH) | test | every `test` Scenario of the script, 1:1 | `tests/test_*.py` |
| Installer | `install.sh` | integration (`unittest`, temp `CLAUDE_CONFIG_DIR`/`OPENCODE_CONFIG_DIR`, real `graphify` on PATH) | test, except the missing-`fd` warning (inspect) | every `test` Scenario of the installer, 1:1 | `tests/test_install.py` |
| Skill and agent prose | `skills/**/SKILL.md`, `skills/**/references/*.md`, `agents/*.md` | inspect | inspect | every `inspect` Scenario checked once by the Verifier against the final files | one row per Scenario in `validation.md`'s Scenario-Anchored table (`file:line` and reason in the evidence cell, Result `PASS`) |

**Fixture rule** (D-grill-in-spec-driven.38): sample specs, tasks, validation files, foreign plans and `SKILL.md` copies are `.md` files under `tests/fixtures/<case>/`, copied into the temp repo by `tests/fixtures.py`. No test function contains sample Scenario text, because `scenarios_lib.parse_test_file` reads every line of a test function as a possible Scenario claim. Each test Task adds the fixture files its tests need.

## Gate Check Commands

| Gate | Command | Used by |
| --- | --- | --- |
| quick | `python3 -m unittest discover -s tests -v` | script and installer tasks |
| scenarios | `python3 skills/spec-driven/scripts/validate_scenarios.py integrate-skills --root . --only <the task's test Scenario IDs> --since HEAD` | tasks that claim `test` Scenarios; never pass `inspect` IDs |
| build | `bash -n install.sh && node --check render-adapters.js && python3 -m py_compile skills/spec-driven/scripts/*.py` | every task |
| plan | `python3 skills/spec-driven/scripts/validate_spec.py integrate-skills --root . && python3 skills/spec-driven/scripts/validate_tasks.py integrate-skills --root .` | every task after T6 |
| full | quick + build + plan (plan only after T6) | prose tasks (regression only; behavior is proven by inspection) |

Before T4 lands, `validate_spec.py` reports one expected error on this spec (the renamed section). Before T6 lands, `validate_tasks.py` ignores the Tickets section. Before T2 lands, `validate_scenarios.py` without `--only` fails every `inspect` Scenario.

---

## Tickets

### K1: Gates accept inspect proofs
**Delivers**: a Scenario marked `**Proof**: inspect` passes `validate_scenarios.py` when the Scenario-Anchored table in `validation.md` has exactly one PASS row for it; Execute and the Verifier know which Scenarios each one checks.
**Covers**: PROOF-01, PROOF-02 · PROOF-01.S1, PROOF-01.S2, PROOF-01.S3, PROOF-01.S4, PROOF-01.S5, PROOF-02.S1
**Blocked by**: none
**Tasks**: T1, T2, T3

### K2: Validators understand the new plan shape
**Delivers**: `validate_spec.py` requires "Decisions & Assumptions" in native specs and checks its two tables by header; `validate_tasks.py` checks Tickets; legacy plans only get warnings. This plan then passes both gates.
**Covers**: GRILL-05, GRILL-06, GRILL-09, PLAN-01, TKT-03, TKT-04, TKT-05, PLAN-02 · GRILL-05.S1, GRILL-05.S2, GRILL-06.S1, GRILL-09.S1, GRILL-09.S2, PLAN-01.S1, TKT-03.S1, TKT-03.S2, TKT-04.S1, TKT-05.S1, PLAN-02.S1
**Blocked by**: K1
**Tasks**: T4, T5, T6, T7

### K3: Review prep and installer follow the new rules
**Delivers**: `/spec-review` snapshots records and every glossary, lists the feature's records and any `context.md`, stops on missing plan files, and reviews a teammate's foreign plan (a file or a folder, each with its own report folder) without touching it; `install.sh` removes this repository's retired skills, leaves same-named skills from other sources alone, and warns about `fd`.
**Covers**: REV-01, REV-02, TKT-01, TKT-02, PLAN-04, FLOW-01, READ-04 · REV-01.S1, REV-01.S2, REV-02.S1, REV-02.S2, REV-02.S3, TKT-01.S1, TKT-02.S1, TKT-02.S2, PLAN-04.S1, PLAN-04.S2, PLAN-04.S3, FLOW-01.S1, FLOW-01.S2, FLOW-01.S3, READ-04.S1
**Blocked by**: K2
**Tasks**: T8, T9, T10, T11

### K4: Specify grills and writes a Grilling Record
**Delivers**: a user can run Specify and be grilled one question at a time; the agent writes a draft record as it goes, resumes it after an interruption, reads Decisions through the shared read rule, and writes a native spec, including from a teammate's foreign plan. `setup-spec-driven` and `grilling` install.
**Covers**: GRILL-01, GRILL-02, GRILL-03, GRILL-04, GRILL-07, GRILL-08, GRILL-10, REC-01, REC-02, REC-03, REC-04, REC-07, REC-10, READ-02, READ-03, READ-05, EDGE-02, PLAN-05, FLOW-02 · GRILL-01.S1, GRILL-02.S1, GRILL-03.S1, GRILL-04.S1, GRILL-07.S1, GRILL-08.S1, GRILL-10.S1, REC-01.S1, REC-01.S2, REC-02.S1, REC-03.S1, REC-04.S1, REC-07.S1, REC-10.S1, READ-02.S1, READ-03.S1, READ-05.S1, EDGE-02.S1, PLAN-05.S1, FLOW-02.S1
**Blocked by**: K3
**Tasks**: T12, T13, T14, T15, T16

### K5: Design, Tasks and Tickets follow the records
**Delivers**: Design writes into the record at Medium+, Tasks always produces day-sized Tickets, Tickets publish safely on a go-ahead, and the skill entry point keeps `graphify-out/`.
**Covers**: REC-06, REC-08, TKT-08, TKT-06, TKT-07, READ-06 · REC-06.S1, REC-08.S1, TKT-08.S1, TKT-06.S1, TKT-06.S2, TKT-06.S3, TKT-07.S1, TKT-07.S2, READ-06.S1
**Blocked by**: K4
**Tasks**: T17, T18, T19, T20, T21

### K6: Execute and reviews use the records
**Delivers**: Execute runs the tdd loop, reads legacy and per-context decisions, puts fixes in fix Tickets, and leaves `/code-review` to the human; Dispositions rewrite Decisions in place; both reviewers check against the records.
**Covers**: FLOW-05, TKT-09, FLOW-03, READ-01, EDGE-01, PLAN-03, REC-05, REV-03, REV-04, REV-05, REV-06 · FLOW-05.S1, TKT-09.S1, TKT-09.S2, FLOW-03.S1, READ-01.S1, EDGE-01.S1, EDGE-01.S2, EDGE-01.S3, PLAN-03.S1, REC-05.S1, REC-05.S2, REC-05.S3, REV-03.S1, REV-04.S1, REV-05.S1, REV-05.S2, REV-06.S1
**Blocked by**: K5
**Tasks**: T22, T23, T24, T25, T26

### K7: No side doors, no leftovers
**Delivers**: diagnosing-bugs and prototype hand off to Specify, grill-with-docs and improve-codebase-architecture write records, the eight retired skills, `wizard` included, are gone, and the README describes the new flow.
**Covers**: FLOW-04, FLOW-06, REC-09 · FLOW-04.S1, FLOW-06.S1, REC-09.S1
**Blocked by**: K6
**Tasks**: T27, T28, T29, T30, T31

---

## Execution Plan

Each phase is one Ticket. Phases run in order; tasks within a phase run in order.

### Phase 1: K1 Inspect proofs

```
T1 → T2 → T3
```

### Phase 2: K2 Validators

```
T4 → T5 → T6 → T7
```

### Phase 3: K3 Review prep and installer

```
T8 → T9 → T10 → T11
```

### Phase 4: K4 Specify

```
T12 → T13 → T14 → T15 → T16
```

### Phase 5: K5 Design, Tasks and Tickets

```
T17 → T18 → T19 → T20 → T21
```

### Phase 6: K6 Execute and reviews

```
T22 → T23 → T24 → T25 → T26
```

### Phase 7: K7 Side doors and cleanup

```
T27 → T28 → T29 → T30 → T31
```

---

## Task Breakdown

### Phase 1: K1 Inspect proofs

#### T1: Add the fixture-repository test helper

**What**: `tests/fixtures.py` with a helper that builds a throwaway git repository in a temp dir by copying a named case from `tests/fixtures/<case>/` (spec, tasks, design, records, summary, validation.md, glossaries, all as `.md` files) and runs a script as a subprocess, returning exit code and output. It requires the real `graphify` on PATH and fails with a clear message when it is missing. A first case, `tests/fixtures/base/`, holds a minimal native feature. Fixture text never lives inside a test function (see the fixture rule above).
**Where**: `tests/fixtures.py` (with `tests/fixtures/base/`)
**Depends on**: None
**Reuses**: fixture layout used to smoke-test the scripts in the previous feature (scratch repo with `.specs/features/<f>/`)
**Requirement**: PROOF-01, GRILL-05, TKT-01 (infrastructure for their tests)

**Done when**:
- [x] `python3 -c "import sys; sys.path.insert(0, 'tests'); import fixtures"` succeeds
- [x] the helper builds a repo from `tests/fixtures/base/` and `validate_scenarios.py` reports no claim coming from a fixture file
- [x] Gate check passes: build

**Tests**: none (test infrastructure; proves no Scenario)
**Scenarios**: none - this task writes no tests
**Gate**: build

**Commit**: `test: add fixture repository helper for script tests`

---

#### T2: Accept inspect proofs in validate_scenarios.py

**What**: `scenarios_lib.parse_spec` reads an optional `**Proof**: test|inspect` line after each Scenario's closing fence (default `test`). For an `inspect` Scenario, `validate_scenarios.py` finds the Scenario-Anchored table in `.specs/features/<f>/validation.md` by its `Scenario` and `Result` headers (never by position) and accepts the Scenario only when exactly one row carries its ID and that row's Result is `PASS`, with or without the `✅` mark. A missing table or row, a `❌ GAP` Result, or two rows with the same ID is an error naming the Scenario.
**Where**: `skills/spec-driven/scripts/validate_scenarios.py`, `skills/spec-driven/scripts/scenarios_lib.py` (tests in `tests/test_validate_scenarios.py`)
**Depends on**: T1
**Reuses**: `parse_spec`, the missing-test check and error reporting in `validate_scenarios.py`
**Requirement**: PROOF-01

**Done when**:
- [x] the five Scenario tests pass and carry their Scenario text verbatim; their fixtures are `.md` files under `tests/fixtures/`
- [x] a spec with no `**Proof**:` lines behaves exactly as before (every Scenario needs a test)
- [x] Gate check passes: quick, scenarios, build

**Tests**: integration
**Scenarios**: PROOF-01.S1, PROOF-01.S2, PROOF-01.S3, PROOF-01.S4, PROOF-01.S5
**Gate**: quick

**Commit**: `feat(spec-driven): accept the Verifier's Scenario table as proof for inspect Scenarios`

---

#### T3: Execute and the Verifier handle inspect Scenarios

**What**: `implement.md` step 5.3 passes only the Task's `test` Scenario IDs to `validate_scenarios.py --only`; `validate.md` §2 tells the Verifier to check every `inspect` Scenario against the final files and record it in the existing Scenario-Anchored table, exactly one row per Scenario of either proof type, before running `validate_scenarios.py` on all Scenarios. For an `inspect` Scenario the evidence cell holds the `file:line` read and a one-sentence reason (IaC may cite command output) in place of a test assertion. The §2 text and the report template at the end of `validate.md` both gain that wording; no second table is added. The existing interactive UAT step for user-facing features stays; it is not a proof type.
**Where**: `skills/spec-driven/references/implement.md`, `skills/spec-driven/references/validate.md`
**Depends on**: T2
**Reuses**: current step 5 and §2 text
**Requirement**: PROOF-02

**Done when**:
- [x] neither file tells an agent to fail a Scenario only because it has no test when its proof type is `inspect`
- [x] `validate.md` describes one results table and its template shows an `inspect` row in it
- [x] Gate check passes: full (plan excluded until T6)

**Tests**: inspect
**Scenarios**: PROOF-02.S1
**Gate**: full

**Commit**: `feat(spec-driven): check inspect Scenarios once in the Verifier`

---

### Phase 2: K2 Validators

#### T4: Rename and require "Decisions & Assumptions" in validate_spec.py

**What**: replace "Assumptions & Open Questions" with "Decisions & Assumptions" in both required-section lists; accept a section whose body is `none`; find the Decisions table by its `ID` and `Choice` headers and the Assumptions table by its `Assumption` and `Chosen default` headers; error on an empty Choice or Rationale, or an empty Chosen default or Rationale, naming the row's first cell.
**Where**: `skills/spec-driven/scripts/validate_spec.py` (tests in `tests/test_validate_spec.py`)
**Depends on**: T3
**Reuses**: `section_bounds`, `split_row`, `REQUIRED_SECTIONS` and the assumptions check at `validate_spec.py:197-217`
**Requirement**: GRILL-05, GRILL-06, GRILL-09

**Done when**:
- [x] the five Scenario tests pass and carry their Scenario text verbatim
- [x] `validate_spec.py integrate-skills` exits 0 on this feature
- [x] Gate check passes: quick, scenarios, build

**Tests**: integration
**Scenarios**: GRILL-05.S1, GRILL-05.S2, GRILL-06.S1, GRILL-09.S1, GRILL-09.S2
**Gate**: quick

**Commit**: `feat(spec-driven): require Decisions & Assumptions and check its tables by header`

---

#### T5: Legacy specs only warn in validate_spec.py

**What**: a spec with no `**Grilling Record**:` line is legacy; for it, a missing "Decisions & Assumptions" section is a warning, and the old "Assumptions & Open Questions" table is still checked as before.
**Where**: `skills/spec-driven/scripts/validate_spec.py` (tests in `tests/test_validate_spec.py`)
**Depends on**: T4
**Reuses**: the warning reporting in `validate_spec.py`
**Requirement**: PLAN-01

**Done when**:
- [x] the Scenario test passes
- [x] Gate check passes: quick, scenarios, build

**Tests**: integration
**Scenarios**: PLAN-01.S1
**Gate**: quick

**Commit**: `feat(spec-driven): accept legacy specs with warnings`

---

#### T6: Check Tickets in validate_tasks.py

**What**: add `Tickets` to the required sections and a Ticket pass: parse `### K<n>:` blocks and their `**Tasks**` and `**Blocked by**` fields; error when a task is in no Ticket, in more than one, or when Blocked by names a later Ticket. Fix Tickets and fix tasks with a `**Fixes**` field are ordinary Tickets and tasks.
**Where**: `skills/spec-driven/scripts/validate_tasks.py` (tests in `tests/test_validate_tasks.py`)
**Depends on**: T5
**Reuses**: `parse_tasks`, `TASK_RE`, the error/warning reporting in `check`
**Requirement**: TKT-03, TKT-04, TKT-05

**Done when**:
- [x] the four Scenario tests pass
- [x] `validate_tasks.py integrate-skills` exits 0 on this file
- [x] Gate check passes: quick, scenarios, build, plan

**Tests**: integration
**Scenarios**: TKT-03.S1, TKT-03.S2, TKT-04.S1, TKT-05.S1
**Gate**: quick

**Commit**: `feat(spec-driven): check Ticket membership and blocking order in tasks.md`

---

#### T7: Legacy task plans only warn in validate_tasks.py

**What**: when the `spec.md` beside `tasks.md` has no `**Grilling Record**:` line, a missing `## Tickets` section and tasks outside Tickets are warnings.
**Where**: `skills/spec-driven/scripts/validate_tasks.py` (tests in `tests/test_validate_tasks.py`)
**Depends on**: T6
**Reuses**: the Ticket pass from T6
**Requirement**: PLAN-02

**Done when**:
- [x] the Scenario test passes
- [x] Gate check passes: quick, scenarios, build, plan

**Tests**: integration
**Scenarios**: PLAN-02.S1
**Gate**: quick

**Commit**: `feat(spec-driven): accept legacy task plans with warnings`

---

### Phase 3: K3 Review prep and installer

#### T8: Snapshot records and every glossary; list the feature's records in prep_review.py

**What**: add `.specs/decisions/`, `CONTEXT-MAP.md` and every path whose basename is `CONTEXT.md` to the plan paths the pre-review commit protects; read `summary.md` and list records whose Specs names the feature; list the feature's `context.md` as a legacy decision source whenever the file exists, whatever the plan kind; for a native feature drop the `STATE.md` decisions line from the Review context.
**Where**: `skills/spec-driven/scripts/prep_review.py` (tests in `tests/test_prep_review.py`)
**Depends on**: T7
**Reuses**: `prep_spec`, `dirty_paths`, `must_git`
**Requirement**: REV-01, REV-02

**Done when**:
- [x] the five Scenario tests pass with the real `graphify`
- [x] Gate check passes: quick, scenarios, build, plan

**Tests**: integration
**Scenarios**: REV-01.S1, REV-01.S2, REV-02.S1, REV-02.S2, REV-02.S3
**Gate**: quick

**Commit**: `feat(spec-driven): snapshot Grilling Records and glossaries before spec review`

---

#### T9: Stop review prep on missing plan files

**What**: in `prep_spec`, raise `Stop` when `tasks.md` is missing at any scope, or `design.md` is missing at Medium, Large or Complex.
**Where**: `skills/spec-driven/scripts/prep_review.py` (tests in `tests/test_prep_review.py`)
**Depends on**: T8
**Reuses**: `spec_scope` from `scenarios_lib.py`; the existing `Stop` exception
**Requirement**: TKT-01, TKT-02

**Done when**:
- [x] the three Scenario tests pass
- [x] Gate check passes: quick, scenarios, build, plan

**Tests**: integration
**Scenarios**: TKT-01.S1, TKT-02.S1, TKT-02.S2
**Gate**: quick

**Commit**: `feat(spec-driven): require tasks.md always and design.md at Medium+ before review`

---

#### T10: Review a foreign plan in prep_review.py

**What**: when the target is a file or folder path outside `.specs/features/`, treat it as a foreign plan: skip the structural validators with a note saying why, and never write to the plan. The report path is `.specs/reviews/<slug>/spec-review-<n>.md`, where `<slug>` is the repo-relative path with its extension and leading dots removed and other characters turned into hyphens; `next_run` runs inside that folder, so each plan has its own run numbers and previous run. A folder target is one plan: every `*.md` file in it is listed as a plan file. A target that does not exist raises `Stop`.
**Where**: `skills/spec-driven/scripts/prep_review.py` (tests in `tests/test_prep_review.py`)
**Depends on**: T9
**Reuses**: `prep_spec` argument handling, `next_run` and the Review context printer
**Requirement**: PLAN-04

**Done when**:
- [x] the three Scenario tests pass
- [x] Gate check passes: quick, scenarios, build, plan

**Tests**: integration
**Scenarios**: PLAN-04.S1, PLAN-04.S2, PLAN-04.S3
**Gate**: quick

**Commit**: `feat(spec-driven): review foreign plans without validating or editing them`

---

### Phase 4: K4 Specify

```
T12 → T13 → T14 → T15 → T16
```

### Phase 5: K5 Design, Tasks and Tickets

```
T17 → T18 → T19 → T20 → T21
```

### Phase 6: K6 Execute and reviews

```
T22 → T23 → T24 → T25 → T26
```

### Phase 7: K7 Side doors and cleanup

```
T27 → T28 → T29 → T30 → T31
```

---

## Task Breakdown

### Phase 1: K1 Inspect proofs

#### T1: Add the fixture-repository test helper

**What**: `tests/fixtures.py` with a helper that builds a throwaway git repository in a temp dir by copying a named case from `tests/fixtures/<case>/` (spec, tasks, design, records, summary, validation.md, glossaries, all as `.md` files) and runs a script as a subprocess, returning exit code and output. It requires the real `graphify` on PATH and fails with a clear message when it is missing. A first case, `tests/fixtures/base/`, holds a minimal native feature. Fixture text never lives inside a test function (see the fixture rule above).
**Where**: `tests/fixtures.py` (with `tests/fixtures/base/`)
**Depends on**: None
**Reuses**: fixture layout used to smoke-test the scripts in the previous feature (scratch repo with `.specs/features/<f>/`)
**Requirement**: PROOF-01, GRILL-05, TKT-01 (infrastructure for their tests)

**Done when**:
- [x] `python3 -c "import sys; sys.path.insert(0, 'tests'); import fixtures"` succeeds
- [x] the helper builds a repo from `tests/fixtures/base/` and `validate_scenarios.py` reports no claim coming from a fixture file
- [x] Gate check passes: build

**Tests**: none (test infrastructure; proves no Scenario)
**Scenarios**: none - this task writes no tests
**Gate**: build

**Commit**: `test: add fixture repository helper for script tests`

---

#### T2: Accept inspect proofs in validate_scenarios.py

**What**: `scenarios_lib.parse_spec` reads an optional `**Proof**: test|inspect` line after each Scenario's closing fence (default `test`). For an `inspect` Scenario, `validate_scenarios.py` finds the Scenario-Anchored table in `.specs/features/<f>/validation.md` by its `Scenario` and `Result` headers (never by position) and accepts the Scenario only when exactly one row carries its ID and that row's Result is `PASS`, with or without the `✅` mark. A missing table or row, a `❌ GAP` Result, or two rows with the same ID is an error naming the Scenario.
**Where**: `skills/spec-driven/scripts/validate_scenarios.py`, `skills/spec-driven/scripts/scenarios_lib.py` (tests in `tests/test_validate_scenarios.py`)
**Depends on**: T1
**Reuses**: `parse_spec`, the missing-test check and error reporting in `validate_scenarios.py`
**Requirement**: PROOF-01

**Done when**:
- [x] the five Scenario tests pass and carry their Scenario text verbatim; their fixtures are `.md` files under `tests/fixtures/`
- [x] a spec with no `**Proof**:` lines behaves exactly as before (every Scenario needs a test)
- [x] Gate check passes: quick, scenarios, build

**Tests**: integration
**Scenarios**: PROOF-01.S1, PROOF-01.S2, PROOF-01.S3, PROOF-01.S4, PROOF-01.S5
**Gate**: quick

**Commit**: `feat(spec-driven): accept the Verifier's Scenario table as proof for inspect Scenarios`

---

#### T3: Execute and the Verifier handle inspect Scenarios

**What**: `implement.md` step 5.3 passes only the Task's `test` Scenario IDs to `validate_scenarios.py --only`; `validate.md` §2 tells the Verifier to check every `inspect` Scenario against the final files and record it in the existing Scenario-Anchored table, exactly one row per Scenario of either proof type, before running `validate_scenarios.py` on all Scenarios. For an `inspect` Scenario the evidence cell holds the `file:line` read and a one-sentence reason (IaC may cite command output) in place of a test assertion. The §2 text and the report template at the end of `validate.md` both gain that wording; no second table is added. The existing interactive UAT step for user-facing features stays; it is not a proof type.
**Where**: `skills/spec-driven/references/implement.md`, `skills/spec-driven/references/validate.md`
**Depends on**: T2
**Reuses**: current step 5 and §2 text
**Requirement**: PROOF-02

**Done when**:
- [x] neither file tells an agent to fail a Scenario only because it has no test when its proof type is `inspect`
- [x] `validate.md` describes one results table and its template shows an `inspect` row in it
- [x] Gate check passes: full (plan excluded until T6)

**Tests**: inspect
**Scenarios**: PROOF-02.S1
**Gate**: full

**Commit**: `feat(spec-driven): check inspect Scenarios once in the Verifier`

---

### Phase 2: K2 Validators

#### T4: Rename and require "Decisions & Assumptions" in validate_spec.py

**What**: replace "Assumptions & Open Questions" with "Decisions & Assumptions" in both required-section lists; accept a section whose body is `none`; find the Decisions table by its `ID` and `Choice` headers and the Assumptions table by its `Assumption` and `Chosen default` headers; error on an empty Choice or Rationale, or an empty Chosen default or Rationale, naming the row's first cell.
**Where**: `skills/spec-driven/scripts/validate_spec.py` (tests in `tests/test_validate_spec.py`)
**Depends on**: T3
**Reuses**: `section_bounds`, `split_row`, `REQUIRED_SECTIONS` and the assumptions check at `validate_spec.py:197-217`
**Requirement**: GRILL-05, GRILL-06, GRILL-09

**Done when**:
- [x] the five Scenario tests pass and carry their Scenario text verbatim
- [x] `validate_spec.py integrate-skills` exits 0 on this feature
- [x] Gate check passes: quick, scenarios, build

**Tests**: integration
**Scenarios**: GRILL-05.S1, GRILL-05.S2, GRILL-06.S1, GRILL-09.S1, GRILL-09.S2
**Gate**: quick

**Commit**: `feat(spec-driven): require Decisions & Assumptions and check its tables by header`

---

#### T5: Legacy specs only warn in validate_spec.py

**What**: a spec with no `**Grilling Record**:` line is legacy; for it, a missing "Decisions & Assumptions" section is a warning, and the old "Assumptions & Open Questions" table is still checked as before.
**Where**: `skills/spec-driven/scripts/validate_spec.py` (tests in `tests/test_validate_spec.py`)
**Depends on**: T4
**Reuses**: the warning reporting in `validate_spec.py`
**Requirement**: PLAN-01

**Done when**:
- [x] the Scenario test passes
- [x] Gate check passes: quick, scenarios, build

**Tests**: integration
**Scenarios**: PLAN-01.S1
**Gate**: quick

**Commit**: `feat(spec-driven): accept legacy specs with warnings`

---

#### T6: Check Tickets in validate_tasks.py

**What**: add `Tickets` to the required sections and a Ticket pass: parse `### K<n>:` blocks and their `**Tasks**` and `**Blocked by**` fields; error when a task is in no Ticket, in more than one, or when Blocked by names a later Ticket. Fix Tickets and fix tasks with a `**Fixes**` field are ordinary Tickets and tasks.
**Where**: `skills/spec-driven/scripts/validate_tasks.py` (tests in `tests/test_validate_tasks.py`)
**Depends on**: T5
**Reuses**: `parse_tasks`, `TASK_RE`, the error/warning reporting in `check`
**Requirement**: TKT-03, TKT-04, TKT-05

**Done when**:
- [x] the four Scenario tests pass
- [x] `validate_tasks.py integrate-skills` exits 0 on this file
- [x] Gate check passes: quick, scenarios, build, plan

**Tests**: integration
**Scenarios**: TKT-03.S1, TKT-03.S2, TKT-04.S1, TKT-05.S1
**Gate**: quick

**Commit**: `feat(spec-driven): check Ticket membership and blocking order in tasks.md`

---

#### T7: Legacy task plans only warn in validate_tasks.py

**What**: when the `spec.md` beside `tasks.md` has no `**Grilling Record**:` line, a missing `## Tickets` section and tasks outside Tickets are warnings.
**Where**: `skills/spec-driven/scripts/validate_tasks.py` (tests in `tests/test_validate_tasks.py`)
**Depends on**: T6
**Reuses**: the Ticket pass from T6
**Requirement**: PLAN-02

**Done when**:
- [x] the Scenario test passes
- [x] Gate check passes: quick, scenarios, build, plan

**Tests**: integration
**Scenarios**: PLAN-02.S1
**Gate**: quick

**Commit**: `feat(spec-driven): accept legacy task plans with warnings`

---

### Phase 3: K3 Review prep and installer

#### T8: Snapshot records and every glossary; list the feature's records in prep_review.py

**What**: add `.specs/decisions/`, `CONTEXT-MAP.md` and every path whose basename is `CONTEXT.md` to the plan paths the pre-review commit protects; read `summary.md` and list records whose Specs names the feature; list the feature's `context.md` as a legacy decision source whenever the file exists, whatever the plan kind; for a native feature drop the `STATE.md` decisions line from the Review context.
**Where**: `skills/spec-driven/scripts/prep_review.py` (tests in `tests/test_prep_review.py`)
**Depends on**: T7
**Reuses**: `prep_spec`, `dirty_paths`, `must_git`
**Requirement**: REV-01, REV-02

**Done when**:
- [x] the five Scenario tests pass with the real `graphify`
- [x] Gate check passes: quick, scenarios, build, plan

**Tests**: integration
**Scenarios**: REV-01.S1, REV-01.S2, REV-02.S1, REV-02.S2, REV-02.S3
**Gate**: quick

**Commit**: `feat(spec-driven): snapshot Grilling Records and glossaries before spec review`

---

#### T9: Stop review prep on missing plan files

**What**: in `prep_spec`, raise `Stop` when `tasks.md` is missing at any scope, or `design.md` is missing at Medium, Large or Complex.
**Where**: `skills/spec-driven/scripts/prep_review.py` (tests in `tests/test_prep_review.py`)
**Depends on**: T8
**Reuses**: `spec_scope` from `scenarios_lib.py`; the existing `Stop` exception
**Requirement**: TKT-01, TKT-02

**Done when**:
- [x] the three Scenario tests pass
- [x] Gate check passes: quick, scenarios, build, plan

**Tests**: integration
**Scenarios**: TKT-01.S1, TKT-02.S1, TKT-02.S2
**Gate**: quick

**Commit**: `feat(spec-driven): require tasks.md always and design.md at Medium+ before review`

---

#### T10: Review a foreign plan in prep_review.py

**What**: when the target is a file or folder path outside `.specs/features/`, treat it as a foreign plan: skip the structural validators with a note saying why, and never write to the plan. The report path is `.specs/reviews/<slug>/spec-review-<n>.md`, where `<slug>` is the repo-relative path with its extension and leading dots removed and other characters turned into hyphens; `next_run` runs inside that folder, so each plan has its own run numbers and previous run. A folder target is one plan: every `*.md` file in it is listed as a plan file. A target that does not exist raises `Stop`.
**Where**: `skills/spec-driven/scripts/prep_review.py` (tests in `tests/test_prep_review.py`)
**Depends on**: T9
**Reuses**: `prep_spec` argument handling, `next_run` and the Review context printer
**Requirement**: PLAN-04

**Done when**:
- [x] the three Scenario tests pass
- [x] Gate check passes: quick, scenarios, build, plan

**Tests**: integration
**Scenarios**: PLAN-04.S1, PLAN-04.S2, PLAN-04.S3
**Gate**: quick

**Commit**: `feat(spec-driven): review foreign plans without validating or editing them`

---

#### T11: Retire skills and warn about fd in install.sh

**What**: extend `RETIRED_SKILLS` with `ask-matt implement to-spec to-tickets triage wayfinder wizard setup-matt-pocock-skills`, each paired with a short phrase from the `SKILL.md` this repository shipped. The removal loop deletes an installed folder only when it is not a symlink and its `SKILL.md` contains that phrase; otherwise it prints `skipped <name>: not installed by this repo` and leaves the folder. Print a warning when `fd` is not on PATH and continue. The test fixtures hold their own small `SKILL.md` copies with those phrases under `tests/fixtures/`, because T30 deletes the source skills.
**Where**: `install.sh` (tests in `tests/test_install.py`)
**Depends on**: T10
**Reuses**: the `RETIRED_SKILLS` removal loop at `install.sh:24-28`; the graphify presence check style at `install.sh:50`
**Requirement**: FLOW-01, READ-04

**Done when**:
- [ ] the three FLOW-01 tests pass with temp config dirs and the real `graphify`
- [ ] every phrase in `RETIRED_SKILLS` occurs in the matching `skills/<name>/SKILL.md` at this commit
- [ ] the fd check prints a warning naming `fd` and does not exit
- [ ] Gate check passes: quick, scenarios, build, plan

**Tests**: integration
**Scenarios**: FLOW-01.S1, FLOW-01.S2, FLOW-01.S3, READ-04.S1
**Gate**: quick

**Commit**: `feat(install): remove only this repo's retired skills and warn when fd is missing`

---

### Phase 4: K4 Specify

#### T12: Vendor and extend the grilling skill

**What**: copy the synced `grilling` text into the repo and add the "you decide" and "decide the rest" escapes and the Binds-in-recommendation rule; add `agents/openai.yaml`.
**Where**: `skills/grilling/SKILL.md`
**Depends on**: T11
**Reuses**: `~/.claude/skills/synced/*/grilling/SKILL.md`; `skills/grill-with-docs/agents/openai.yaml` as the yaml pattern
**Requirement**: GRILL-01, GRILL-02, GRILL-03 (support file; proven through Specify in T16)

**Done when**:
- [x] the skill states one question per turn with options and a recommendation, both escapes, and Binds in the recommendation
- [x] Gate check passes: full

**Tests**: none (support file; its Scenarios are claimed by T16, which wires it into Specify)
**Scenarios**: none - this task writes no tests
**Gate**: full

**Commit**: `feat(grilling): vendor the grilling skill with decision escapes`

---

#### T13: Grilling Record and summary formats in domain-modeling

**What**: replace `ADR-FORMAT.md` with `GRILLING-RECORD-FORMAT.md` (record and `summary.md` templates; completeness rules in prose; one choice per Decision; slug names unique in the folder; `draft` status and resume; incremental writing; rewrite in place with a `Changed` line; `## Design` and `## Review` sections; the Date column and sorting; legacy lines); rewrite `SKILL.md` to write records instead of offering ADRs.
**Where**: `skills/domain-modeling/GRILLING-RECORD-FORMAT.md`, `skills/domain-modeling/SKILL.md`, `skills/domain-modeling/ADR-FORMAT.md` (deleted)
**Depends on**: T12
**Reuses**: `.specs/decisions/grill-in-spec-driven.md` and `summary.md` as the worked example
**Requirement**: REC-01, REC-03, REC-04, REC-05 (support file; proven through Specify in T16 and review.md in T24)

**Done when**:
- [ ] no file in `skills/domain-modeling/` tells the agent to write an ADR or mark a Decision superseded
- [ ] the template marks every section required and says a record covers the whole session
- [ ] Gate check passes: full

**Tests**: none (support file; its Scenarios are claimed by T16 and T24)
**Scenarios**: none - this task writes no tests
**Gate**: full

**Commit**: `feat(domain-modeling): replace ADRs with complete Grilling Records`

---

#### T14: Write the shared read rule and discovery reference

**What**: `references/decisions.md` with discovery (two `fd` commands, stop-and-ask when `fd` is missing), the `summary.md` row filter (`active` only; `draft` records skipped; no other status exists), the header fallback for a broken index, the legacy sources (root and per-context `docs/adr/`, `STATE.md`, and a feature's `context.md` whenever it exists), the three plan kinds (the `**Grilling Record**:` line alone separates native from legacy), the Binds test, and "cite outside sources used".
**Where**: `skills/spec-driven/references/decisions.md`
**Depends on**: T13
**Reuses**: D-grill-in-spec-driven.17, .18, .19 and .43 text from the Grilling Record; `skills/setup-matt-pocock-skills/domain.md:9`
**Requirement**: READ-01, READ-02, READ-03, READ-05, EDGE-01 (support file; proven through its consumers in T16 and T23)

**Done when**:
- [ ] the file holds the exact fd commands from D-grill-in-spec-driven.18, the `docs/adr` probe, and the filter from D-grill-in-spec-driven.17
- [ ] Gate check passes: full

**Tests**: none (support file; its Scenarios are claimed by T16 and T23)
**Scenarios**: none - this task writes no tests
**Gate**: full

**Commit**: `feat(spec-driven): add the shared Decision read rule and repo discovery`

---

#### T15: Rename setup-matt-pocock-skills to setup-spec-driven

**What**: `git mv` the directory; drop Section B and `triage-labels.md`; point the domain docs section and `domain.md` at `.specs/decisions/`; rewrite names and descriptions; add an `install.sh` test for the new skills.
**Where**: `skills/setup-spec-driven/` (tests in `tests/test_install.py`)
**Depends on**: T14
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

#### T16: Specify runs the grill

**What**: rewrite `specify.md` steps 1-2: pre-question steps (lessons, `decisions.md`, capability search, Standards); call `grilling` and `domain-modeling` by name with the sibling-path fallback; create the draft record at the first answer and resume a draft found for the feature; dimensions sweep as closing branches; spec written after shared understanding; update both templates (`**Grilling Record**:` line, `**Proof**:` line per Scenario, Decisions & Assumptions table, Deferred Ideas in Out of Scope, optional References); continue an existing non-feature record when one exists; take a foreign plan as input and link it; delete `discuss.md`.
**Where**: `skills/spec-driven/references/specify.md`, `skills/spec-driven/references/discuss.md` (deleted)
**Depends on**: T15
**Reuses**: current `specify.md` steps 3-4 (EARS, Scenarios, closure gate) unchanged
**Requirement**: GRILL-01, GRILL-02, GRILL-03, GRILL-04, GRILL-07, GRILL-08, GRILL-10, REC-01, REC-02, REC-03, REC-04, REC-07, REC-10, READ-02, READ-03, READ-05, EDGE-02, PLAN-05

**Done when**:
- [ ] no reference in `skills/spec-driven/` points at `discuss.md` or tells an agent to write `context.md`
- [ ] Gate check passes: full

**Tests**: inspect
**Scenarios**: GRILL-01.S1, GRILL-02.S1, GRILL-03.S1, GRILL-04.S1, GRILL-07.S1, GRILL-08.S1, GRILL-10.S1, REC-01.S1, REC-01.S2, REC-02.S1, REC-03.S1, REC-04.S1, REC-07.S1, REC-10.S1, READ-02.S1, READ-03.S1, READ-05.S1, EDGE-02.S1, PLAN-05.S1
**Gate**: full

**Commit**: `feat(spec-driven): Specify grills and writes a Grilling Record`

---

### Phase 5: K5 Design, Tasks and Tickets

#### T17: Design writes into the Grilling Record

**What**: Design is required at Medium+; it reads via `decisions.md`; asks grill-style questions; appends a `## Design` section; Tech Decisions become links; changing another record's Decision rewrites it there instead of writing `AD-NNN`.
**Where**: `skills/spec-driven/references/design.md`
**Depends on**: T16
**Reuses**: current template sections (reuse table, components, risks)
**Requirement**: REC-06, REC-08

**Done when**:
- [ ] no instruction in `design.md` writes to `STATE.md` or `docs/adr/`
- [ ] Gate check passes: full

**Tests**: inspect
**Scenarios**: REC-06.S1, REC-08.S1
**Gate**: full

**Commit**: `feat(spec-driven): Design records its Decisions in the Grilling Record`

---

#### T18: Tasks always runs and slices Tickets first

**What**: remove the skip rule; slice the Spec into Tickets (D-grill-in-spec-driven.23, markup D-grill-in-spec-driven.39) before cutting Tasks; add the Proof type column to the Test Coverage Matrix template; document the `## Tickets` section in the template and the Ticket checks in step 5.
**Where**: `skills/spec-driven/references/tasks.md`
**Depends on**: T17
**Reuses**: current Tasks process and template
**Requirement**: TKT-08

**Done when**:
- [ ] the template's Tickets section matches what `validate_tasks.py` checks
- [ ] Gate check passes: full

**Tests**: inspect
**Scenarios**: TKT-08.S1
**Gate**: full

**Commit**: `feat(spec-driven): Tasks runs at every scope and slices day-sized Tickets`

---

#### T19: Ticket slicing, fix Tickets and publishing reference

**What**: `references/tickets.md`: one-day vertical slices, expand–contract for wide refactors, fix Tickets per round, and publishing per tracker (from `docs/agents/issue-tracker.md` written by `setup-spec-driven`) with the four rules: a Spec Review with all Dispositions first, ID write-back right after each issue, never re-create a published Ticket (drift listed and updated on a go-ahead), stop and resume on failure. Issues link to the Spec, say the work is built through it, and carry no `ready-for-agent` label or "agent-grabbable" wording.
**Where**: `skills/spec-driven/references/tickets.md`
**Depends on**: T18
**Reuses**: `skills/to-tickets/SKILL.md` sections 3 and 5 (without the label); `skills/setup-spec-driven/issue-tracker-*.md`
**Requirement**: TKT-06, TKT-07

**Done when**:
- [ ] it states that publishing needs an explicit "publish tickets" after a Spec Review whose Findings all have Dispositions
- [ ] `grep -n "ready-for-agent\|agent-grabbable" skills/spec-driven/references/tickets.md` finds nothing
- [ ] Gate check passes: full

**Tests**: inspect
**Scenarios**: TKT-06.S1, TKT-06.S2, TKT-06.S3, TKT-07.S1, TKT-07.S2
**Gate**: full

**Commit**: `feat(spec-driven): add Ticket slicing and safe publishing`

---

#### T20: Update the spec-driven SKILL.md

**What**: flow line, auto-sizing table (Tasks at every scope, Design at Medium+), `.specs` tree (`decisions/`, `reviews/`, no `context.md`), commands table (publish tickets; Discuss removed; decisions.md), Critical Rules (implementation only through spec-driven; Tickets published only on go-ahead; foreign plans never edited; `graphify-out/` is a cache that may be gitignored and is never deleted, only refreshed with `graphify update .`), Knowledge Verification Chain step 2 (records instead of `STATE.md`).
**Where**: `skills/spec-driven/SKILL.md`
**Depends on**: T19
**Reuses**: current SKILL.md structure
**Requirement**: READ-06, GRILL-07, TKT-08 (entry-point wording)

**Done when**:
- [ ] SKILL.md mentions neither `context.md` as something to write nor the safety valve
- [ ] Gate check passes: full

**Tests**: inspect
**Scenarios**: READ-06.S1
**Gate**: full

**Commit**: `docs(spec-driven): describe the merged flow in SKILL.md`

---

#### T21: Memory, standards and writing references follow the records

**What**: `memory.md` keeps only `## Handoff` and points Decisions at `decisions.md`; `standards.md` §1 lists active project Decisions as Repo Standards and uses discovery, and §4 states that `graphify-out/` is never deleted; `coding-principles.md` drops ADR wording.
**Where**: `skills/spec-driven/references/memory.md`, `skills/spec-driven/references/standards.md`, `skills/spec-driven/references/coding-principles.md`
**Depends on**: T20
**Reuses**: current files
**Requirement**: READ-01, READ-06 (Repo Standard and graph wording)

**Done when**:
- [ ] no instruction in these files writes `AD-NNN` or ADRs, or deletes `graphify-out/`
- [ ] Gate check passes: full

**Tests**: none (wording; READ-01 is claimed by T23 and READ-06 by T20)
**Scenarios**: none - this task writes no tests
**Gate**: full

**Commit**: `docs(spec-driven): point memory and standards at Grilling Records`

---

### Phase 6: K6 Execute and reviews

#### T22: Execute ends at the Verifier, with fix Tickets, and leaves /code-review to the human

**What**: in `implement.md`: drop the safety valve; call `tdd` per Task; deferred ideas are surfaced and become Out of Scope rows only on a go-ahead; after the Verifier passes, say `/code-review` is available and never run it. In `implement.md` and `validate.md`: Verifier gaps become fix tasks in one fix Ticket per round.
**Where**: `skills/spec-driven/references/implement.md`, `skills/spec-driven/references/validate.md`
**Depends on**: T21
**Reuses**: current per-task cycle and Verifier section
**Requirement**: FLOW-05, TKT-09

**Done when**:
- [ ] no instruction in `implement.md` runs `/code-review` or edits `context.md`
- [ ] Gate check passes: full

**Tests**: inspect
**Scenarios**: FLOW-05.S1, TKT-09.S1
**Gate**: full

**Commit**: `feat(spec-driven): Execute runs tdd per Task and leaves /code-review to the human`

---

#### T23: tdd becomes Execute's per-Task loop

**What**: description and intro say it is the test-first loop spec-driven Execute runs; seams come from Scenarios and Design, asking only for unnamed interfaces; the ADR line becomes a link to `decisions.md`, so a Task reads active Decisions, root and per-context ADRs, and the feature's `context.md` when one exists, before its test.
**Where**: `skills/tdd/SKILL.md`
**Depends on**: T22
**Reuses**: current tdd content (tests.md, mocking.md unchanged)
**Requirement**: FLOW-03, READ-01, EDGE-01, PLAN-03

**Done when**:
- [ ] the description no longer offers to build features on its own
- [ ] Gate check passes: full

**Tests**: inspect
**Scenarios**: FLOW-03.S1, READ-01.S1, EDGE-01.S1, EDGE-01.S2, EDGE-01.S3, PLAN-03.S1
**Gate**: full

**Commit**: `feat(tdd): run as the per-Task loop inside spec-driven Execute`

---

#### T24: Dispositions rewrite Decisions in place

**What**: in `review.md`, after recording Dispositions, rewrite each changed Decision in its original record with a `Changed` line, add review-made Decisions under `## Review`, update `summary.md` when the record's summary or Areas change, turn accepted Change Review Findings into fix tasks in one fix Ticket, and keep the publish-tickets gate; in `finding-format.md`, replace `AD-NNN` inputs with Grilling Records.
**Where**: `skills/spec-driven/references/review.md`, `skills/spec-driven/references/finding-format.md`
**Depends on**: T23
**Reuses**: current "After a reviewer returns" steps
**Requirement**: REC-05, TKT-09

**Done when**:
- [ ] step order: record Dispositions, rewrite Decisions, commit, distill Lessons
- [ ] neither file mentions Amendments or superseded Decisions
- [ ] Gate check passes: full

**Tests**: inspect
**Scenarios**: REC-05.S1, REC-05.S2, REC-05.S3, TKT-09.S2
**Gate**: full

**Commit**: `feat(spec-driven): rewrite Decisions in place when a Disposition changes them`

---

#### T25: spec-reviewer checks the plan against the Grilling Record

**What**: read via `decisions.md` (records, discovery, legacy sources); add the Thought Partnership, Truthful Reporting, Practical Judgment and Communication checks from D-grill-in-spec-driven.20, including bundled choices; for a foreign plan, judge content only and write the report under `.specs/reviews/`.
**Where**: `agents/spec-reviewer.md`
**Depends on**: T24
**Reuses**: current "Read first" and "What to check" sections
**Requirement**: REV-03, REV-04, REV-05

**Done when**:
- [ ] the agent no longer reads `context.md` or `AD-NNN` as primary sources
- [ ] Gate check passes: full

**Tests**: inspect
**Scenarios**: REV-03.S1, REV-04.S1, REV-05.S1, REV-05.S2
**Gate**: full

**Commit**: `feat(agents): spec-reviewer checks plans against Grilling Records`

---

#### T26: change-reviewer checks the Change against active Decisions

**What**: read via `decisions.md`; flag a Change contradicting an active Decision that was not rewritten, and a silent departure from a `Decided by: user` choice as a false Claim.
**Where**: `agents/change-reviewer.md`
**Depends on**: T25
**Reuses**: current "Read first" and "What to check" sections
**Requirement**: REV-06

**Done when**:
- [ ] the agent no longer reads `AD-NNN` as a primary source
- [ ] Gate check passes: full

**Tests**: inspect
**Scenarios**: REV-06.S1
**Gate**: full

**Commit**: `feat(agents): change-reviewer checks Changes against active Decisions`

---

### Phase 7: K7 Side doors and cleanup

#### T27: diagnosing-bugs hands off to Specify

**What**: Phase 5 becomes a hand-off of the repro, root cause and seam to a Small Specify; the ADR line becomes a link to `decisions.md`.
**Where**: `skills/diagnosing-bugs/SKILL.md`
**Depends on**: T26
**Reuses**: Phases 1-4 unchanged
**Requirement**: FLOW-04

**Done when**:
- [ ] no instruction in the skill applies a fix
- [ ] Gate check passes: full

**Tests**: inspect
**Scenarios**: FLOW-04.S1
**Gate**: full

**Commit**: `feat(diagnosing-bugs): hand confirmed root causes to spec-driven`

---

#### T28: prototype hands its verdict to Specify

**What**: rule 6 keeps the prototype on a throwaway branch and records the verdict and the question it settled, then hands the verdict to Specify instead of folding it into the real code.
**Where**: `skills/prototype/SKILL.md`
**Depends on**: T27
**Reuses**: rules 1-5 unchanged; T27's hand-off wording
**Requirement**: FLOW-06

**Done when**:
- [ ] `grep -n "into the real code" skills/prototype/SKILL.md` finds nothing
- [ ] Gate check passes: full

**Tests**: inspect
**Scenarios**: FLOW-06.S1
**Gate**: full

**Commit**: `feat(prototype): hand validated verdicts to spec-driven`

---

#### T29: grill-with-docs and improve-codebase-architecture write Grilling Records

**What**: `grill-with-docs` (+ openai.yaml) describes writing a Grilling Record and `CONTEXT.md` and points features at spec-driven; `improve-codebase-architecture` (+ `HTML-REPORT.md`, openai.yaml) treats active Decisions as it treated ADRs and records rejections in its record.
**Where**: `skills/grill-with-docs/SKILL.md`, `skills/improve-codebase-architecture/SKILL.md`, `skills/improve-codebase-architecture/HTML-REPORT.md`
**Depends on**: T28
**Reuses**: current texts
**Requirement**: REC-09

**Done when**:
- [ ] neither skill mentions writing or offering an ADR
- [ ] Gate check passes: full

**Tests**: inspect
**Scenarios**: REC-09.S1
**Gate**: full

**Commit**: `feat(skills): grill-with-docs and architecture reviews write Grilling Records`

---

#### T30: Delete the retired skills

**What**: `git rm -r` `skills/ask-matt`, `skills/implement`, `skills/to-spec`, `skills/to-tickets`, `skills/triage`, `skills/wayfinder`, `skills/wizard` and `skills/engineering-README.md`.
**Where**: `skills/` (eight paths)
**Depends on**: T29
**Reuses**: none
**Requirement**: FLOW-01 (source side; installed copies handled by T11)

**Done when**:
- [ ] `grep -rn "ask-matt\|to-tickets\|to-spec\|triage\|wayfinder\|wizard\|/implement" skills agents` finds nothing outside historical records
- [ ] `grep -rn "ready-for-agent\|agent-grabbable" skills agents` finds nothing
- [ ] Gate check passes: full

**Tests**: none (deletion; FLOW-01 is proven by T11)
**Scenarios**: none - this task writes no tests
**Gate**: full

**Commit**: `refactor(skills): remove retired skills`

---

#### T31: Rewrite the README for the merged flow

**What**: skill table, flow description (Specify grill, Design at Medium+, Tasks and Tickets, reviews, Execute with tdd, Verifier with `inspect` proofs, `/code-review`), `.specs/decisions/`, legacy and foreign plans, `fd` and graphify requirements (and that `graphify-out/` is kept), attribution as "based on mattpocock/skills", no `engineering-README.md`.
**Where**: `README.md`
**Depends on**: T30
**Reuses**: current README sections
**Requirement**: none (documentation)

**Done when**:
- [ ] the README lists no retired skill as installed, `wizard` included
- [ ] Gate check passes: full

**Tests**: none (documentation)
**Scenarios**: none - this task writes no tests
**Gate**: full

**Commit**: `docs: describe the merged spec-driven flow in the README`

---

## Task Granularity Check

| Task | Scope | Status |
| --- | --- | --- |
| T1 | 1 helper module with its base fixture folder | ✅ Granular |
| T2 | 1 check across `validate_scenarios.py` and the parser it uses | ⚠️ Multi-file, one concept |
| T3 | 1 rule in the Execute and Verifier references | ⚠️ Multi-file, one concept |
| T4-T10 | 1 script change each | ✅ Granular |
| T11 | 1 installer change | ✅ Granular |
| T12, T14, T16-T20, T23, T25-T28, T31 | 1 file each (T16 also deletes `discuss.md`) | ✅ Granular |
| T13 | 1 skill's format (new file + SKILL.md + one deletion) | ⚠️ Multi-file, one concept |
| T15 | 1 directory rename | ⚠️ Multi-file, one concept |
| T21 | 3 small wording updates | ⚠️ Multi-file, one concept |
| T22 | 1 rule in the Execute and Verifier references | ⚠️ Multi-file, one concept |
| T24 | review.md plus the format file it depends on | ⚠️ Multi-file, one concept |
| T29 | 2 skills, same change | ⚠️ Multi-file, one concept |
| T30 | 8 deletions | ⚠️ Multi-file, one concept |

## Diagram-Definition Cross-Check

| Task | Depends on (definition) | Diagram arrow | Match |
| --- | --- | --- | --- |
| T1 | None | start of Phase 1 | ✅ |
| T2-T3 | previous task | chain | ✅ |
| T4 | T3 | start of Phase 2 (cross-phase) | ✅ |
| T5-T7 | previous task | chain | ✅ |
| T8 | T7 | start of Phase 3 (cross-phase) | ✅ |
| T9-T11 | previous task | chain | ✅ |
| T12 | T11 | start of Phase 4 (cross-phase) | ✅ |
| T13-T16 | previous task | chain | ✅ |
| T17 | T16 | start of Phase 5 (cross-phase) | ✅ |
| T18-T21 | previous task | chain | ✅ |
| T22 | T21 | start of Phase 6 (cross-phase) | ✅ |
| T23-T26 | previous task | chain | ✅ |
| T27 | T26 | start of Phase 7 (cross-phase) | ✅ |
| T28-T31 | previous task | chain | ✅ |

## Test Co-location Validation

| Task | Layer | Matrix requires | Task Tests | Status |
| --- | --- | --- | --- | --- |
| T1 | test infrastructure | none | none | ✅ |
| T2, T4-T10 | deterministic scripts | integration | integration | ✅ |
| T11, T15 | installer | integration (inspect for the fd warning) | integration | ✅ |
| T3, T16-T20, T22-T29 | skill and agent prose | inspect | inspect | ✅ |
| T12-T14, T21, T30, T31 | prose with no own Scenario | none | none | ✅ |
