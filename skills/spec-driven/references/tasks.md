# Tasks

**Goal**: Slice the Spec into day-sized **Tickets**, then break each Ticket into GRANULAR, ATOMIC **Tasks**. Clear dependencies. Right tools. Sequential phase execution plan.

**Tasks runs at every scope.** Every Spec gets a `tasks.md`: Small, Medium, Large and Complex alike. The phase is never skipped and Tasks are never left implicit, because the user reviews the work through `tasks.md` and the product team follows it through Tickets. `/spec-review` stops when `tasks.md` is missing. At Small scope the spec's `## Steps` list is only a first sketch; `tasks.md` is still written from it, with one Ticket that lists every Task.

Two levels, cut top-down:

- A **Ticket** is a slice of the Spec's work sized to about one day, demoable on its own, that the product team can follow on the issue tracker. It is made of Tasks and names the Tickets that block it.
- A **Task** is an atomic unit of work inside exactly one Ticket, finished by exactly one commit.

Tickets come first. You slice the Spec into Tickets, and only then cut each Ticket into Tasks; you never write a flat task list and group it into Tickets afterwards.

`<skill-dir>` below is the `spec-driven` skill directory.

## Why Granular Tasks?

| Vague Task (BAD) | Granular Tasks (GOOD)             |
| ---------------- | --------------------------------- |
| "Create form"    | T1: Create email input component  |
|                  | T2: Add email validation function |
|                  | T3: Create submit button          |
|                  | T4: Add form state management     |
|                  | T5: Connect form to API           |
| "Implement auth" | T1: Create login form             |
|                  | T2: Create register form          |
|                  | T3: Add token storage utility     |
|                  | T4: Create auth API service       |
|                  | T5: Add route protection          |

**Benefits of granular:**

- **Agents don't err** - Single focus, no ambiguity
- **Easy to test** - Each task = one verifiable outcome
- **Clean commits** - Each task = one atomic, revertable commit
- **Errors isolated** - One failure doesn't block everything

**Rule**: One task = ONE of these:

- One component
- One function
- One API endpoint
- One file change

---

## Process

### 1. Load the plan so far

Read `.specs/features/[feature]/spec.md` and the Grilling Record its `**Grilling Record**:` line links. Read `.specs/features/[feature]/design.md` when the feature has one (Medium scope and above always does; a Small feature usually does not). Then follow the read rule in [decisions.md](decisions.md) for the paths the Tasks will touch: active project-binding Decisions and legacy decision sources are Repo Standards every Task has to respect.

### 1.5. Generate the Test Coverage Matrix (ALWAYS)

This step ALWAYS runs - there is no precondition. Decide which of two paths to take, then generate the three sections below.

**Step 0 - Read project quality/testing guidelines (ALWAYS, before anything else).**

Start from the Repo Standards already listed in the spec's `## Standards` section ([standards.md](standards.md) section 1). Then scan the project for documented testing standards. Stack-agnostic sources to check (illustrative, not exhaustive):

- Agent/AI convention files, if the repo has any: `AGENTS.md` (the vendor-neutral standard) and any tool-specific rules file or rules directory the project happens to use
- Contributor guides: `CONTRIBUTING.md`, `docs/` (testing, quality, or standards subdocs), README testing section
- Tool configuration: coverage thresholds in the test runner config (e.g., `jest.config.*`, `vitest.config.*`, `pytest.ini`, `.nycrc`, `Makefile` coverage targets, CI coverage gates)

**If guidelines are found:** the Coverage Expectation (see matrix below) conforms to them. Existing test samples fill gaps in style/location/framework only. Cite the specific files found in the matrix provenance note.

**If no guidelines are found:** apply the strong default - cover every spec AC and every listed edge case; domain/business logic maps 1:1 to spec ACs; routes/e2e cover happy + edge + error paths. This default may exceed the current repo's depth, which is intentional.

**Decision:**

- **Existing tests in the repo** → infer the matrix and gate commands by sampling the codebase.
- **No tests at all** → ask the user: "What test types will this project use (unit / integration / e2e / none)? What commands run them?"

**How to infer (path 1 - existing tests):**

1. **Sample test files.** Locate 5-10 existing test files. Map each file's location relative to its source file to identify which code layers are exercised and at what level (unit, integration, e2e). Use these samples for style, location patterns, framework, and test type - and as a **floor** (never produce tests less thorough than existing ones for the same layer). Existing tests are NOT a ceiling on thoroughness; the thoroughness target comes from the spec ACs, listed edge cases, and guidelines (or strong default). The Coverage Expectation column captures the target per layer.
2. **Discover commands from the repo.** Do NOT invent commands and do NOT assume an ecosystem. Read the project's own build/task manifests, test config, and CI workflows to extract the actual commands - for example: `package.json` / `project.json` (JS/TS), `Makefile`, `pyproject.toml` / `tox.ini` / `pytest` (Python), `Cargo.toml` (Rust), `go test` invocations (Go), `pom.xml` / `build.gradle` (Java/Kotlin), `Gemfile` / `Rakefile` (Ruby), `composer.json` (PHP), `.github/workflows` / `.gitlab-ci.yml`. The list is illustrative; detect what this repo actually uses. Capture the **linter/formatter** command too (e.g. the configured `lint`/`format`/`typecheck` script, or a `.pre-commit-config`, `.golangci.yml`, `ruff`/`eslint`/`biome` config) - the Build gate runs it alongside the tests.

**Output contract - render these two sections verbatim into `tasks.md`** (the exact headings downstream phases reference):

---

## Test Coverage Matrix

> Generated from codebase, project guidelines, and spec - confirm before Execute. Guidelines found: [list files, e.g. `AGENTS.md`, `jest.config.ts` - or "none - strong defaults applied"].

| Code Layer | Required Test Type | Proof type | Coverage Expectation | Location Pattern | Run Command |
| ---------- | ------------------ | ---------- | -------------------- | ---------------- | ----------- |
| [layer] | [unit/integration/e2e/inspect/none] | [test/inspect/none] | [depth target for this layer] | [glob or path pattern, or where the Verifier records the proof] | [command] |

**Proof type** says how the Scenarios of a layer are proven. It repeats the `**Proof**:` line each Scenario carries in the spec ([specify.md](specify.md) step 3.5):

- `test`: a Behavior Test proves each Scenario. This is the default, and the Required Test Type says which kind of test.
- `inspect`: the layer is something no test can exercise (a prompt or other skill prose, infrastructure code, configuration). The Required Test Type is also `inspect`. No test is written; after the last Task the Verifier reads the final files and records one row per Scenario in the Scenario-Anchored table of `validation.md`. Never choose `inspect` for a layer a test could exercise.
- `none`: the layer has no Scenario of its own (the Required Test Type is `none`).

**Coverage Expectation values** - set from guidelines first; use strong defaults when no guideline applies:

| Layer type | Strong default (no guideline) |
| ---------- | ----------------------------- |
| Domain / business-logic (service, use-case, domain model) | All branches; 1:1 to spec ACs; every listed edge case has a test |
| Route / controller / e2e / integration | All routes in scope: happy path + every listed edge case + error/failure paths |
| Repository / data-access | Key query paths + error handling; infer from existing repo tests |
| Entity / config / schema | none - build gate only |
| Prompt / skill prose / IaC / configuration with `inspect` Scenarios | Every `inspect` Scenario checked once by the Verifier against the final files |

These defaults may exceed the current repo's depth. That is intentional - they are a **target**, not a reflection of what already exists.

*Example (filled in):*

| Code Layer | Required Test Type | Proof type | Coverage Expectation | Location Pattern | Run Command |
| ---------- | ------------------ | ---------- | -------------------- | ---------------- | ----------- |
| Service | unit | test | All branches; 1:1 to spec ACs; all listed edge cases | `src/**/__test__/*.spec.ts` | `yarn test:unit` |
| Repository | integration | test | Key query paths + error paths | `src/**/__test__/*.e2e-spec.ts` | `yarn test:e2e` |
| Controller/Resolver | e2e | test | All routes: happy + edge + error | `src/**/__test__/*.e2e-spec.ts` | `yarn test:e2e` |
| Entity / Config | none | none | - (build gate only) | - | build gate only |
| Agent prompts (`prompts/*.md`) | inspect | inspect | Every `inspect` Scenario, one row each in `validation.md` | `validation.md` Scenario-Anchored table | build gate only |

## Gate Check Commands

> Generated from codebase - confirm before Execute.

| Gate Level | When to Use | Command |
| ---------- | ----------- | ------- |
| Quick | After tasks with unit tests only | [unit test command] |
| Full | After tasks with e2e/integration tests | [unit + e2e commands] |
| Build | After phase completion or config/entity-only tasks | [build + lint + all tests] |

---

**Co-located tests:** Every task that creates or modifies a code layer with a required test type MUST include writing/updating those tests in the same task. Tests are NOT separate tasks. The tests must satisfy the layer's **Coverage Expectation** from the matrix - not merely exist.

| Task creates...                           | Done When must include...                                                                                          |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Code layer with "unit" requirement        | Unit tests written satisfying the layer's Coverage Expectation (e.g., 1:1 AC mapping for domain logic; all listed edge cases covered) + quick gate passes |
| Code layer with "e2e" requirement         | E2E tests written satisfying the layer's Coverage Expectation (e.g., every route the task adds: happy path + edge + error paths) + full gate passes |
| Code layer with "integration" requirement | Integration tests written satisfying the layer's Coverage Expectation + full gate passes                           |
| Code layer with "inspect" requirement     | The `inspect` Scenarios the task's change delivers are named in its `Scenarios` field + gate check at the appropriate level. No test is written; the Verifier proves them after the last task |
| Code layer with "none" requirement        | Gate check at appropriate level                                                                                    |

### 2. Slice the Spec into Tickets, then cut each Ticket into Tasks

**2.1 Slice the Spec into Tickets first.** Before you write a single Task, divide the Spec's acceptance criteria and Scenarios into Tickets. The slicing rules live in [tickets.md](tickets.md); in short:

- **About one day each.** A Ticket is roughly one day of work for the person or agent building it. Much more than a day: split it. A few minutes: merge it into a neighbour.
- **A vertical slice.** Each Ticket cuts a narrow but complete path through every layer it needs, and is demoable or verifiable on its own. A Ticket is never "the backend" or "the tests". A wide mechanical refactor is the one exception and is sequenced as expand-contract Tickets ([tickets.md](tickets.md)).
- **Blocked-by edges.** Each Ticket names the Tickets that must be finished before it can start, or `none`. Edges point only to Tickets listed earlier.
- **Complete cover.** Every acceptance criterion and every Scenario of the Spec is covered by a Ticket.
- **Every scope gets Tickets.** A Small feature is less than a day of work, so it gets exactly one Ticket, `K1`, and every Task in `tasks.md` is listed in that Ticket. Medium, Large and Complex features get as many Tickets as they have day-sized slices.

Write each Ticket into the `## Tickets` section of `tasks.md` in the markup shown in the template: a `### K<n>: <title>` heading with `**Delivers**`, `**Covers**`, `**Blocked by**` and `**Tasks**` fields. The `K` keeps Ticket IDs apart from Task IDs (`T<n>`).

**2.2 Then cut each Ticket into atomic Tasks.** Take the Tickets in order and break each one into the Tasks that deliver it. Number Tasks `T1`, `T2`, ... across the whole file, Ticket by Ticket. Every Task belongs to exactly one Ticket: add its ID to that Ticket's `**Tasks**` field as soon as you write it. A Task that seems to belong to two Tickets is either two Tasks or a sign the Tickets are sliced wrong.

**Task = ONE deliverable**. Examples:

- ✅ "Create UserService interface" (one file, one concept)
- ❌ "Implement user management" (too vague, multiple files)

**Each Task claims only the Scenarios its own change delivers**, and they are Scenarios its Ticket covers. A Task whose Scenarios have proof type `test` writes their tests and names their IDs in `**Scenarios**`. A Task whose Scenarios have proof type `inspect` (prose, infrastructure code, configuration) says `**Tests**: inspect` and names those IDs in `**Scenarios**` the same way; it writes no test for them.

### 3. Define Dependencies

What MUST be done before this task can start?

### 4. Create Execution Plan

**One phase per Ticket.** Each Ticket is one Execution Plan phase, in the order the Tickets are listed: `### Phase 1: K1 [title]`, `### Phase 2: K2 [title]`, and so on. Each phase depends on the ones before it; tasks execute sequentially within a phase. Because a Ticket's `Blocked by` only names earlier Tickets, finishing the phases in order always respects the blocking edges.

**Size phases near the worker budget.** During Execute, phases are packed into task-budgeted batches (~7 tasks per sub-agent, whole phases - see [sub-agents.md](sub-agents.md)). Because a batch cut may only land on a phase boundary, a phase that is much larger than the budget forces an over-sized worker. Keep each phase from greatly exceeding the budget:

- If a phase would hold **more than ~10 tasks (≈1.5× the budget)**, its Ticket is almost certainly more than a day of work: split the Ticket into two Tickets at a genuine dependency/cohesion seam - not at an arbitrary task index - so each stays demoable on its own.
- Only leave a phase over-sized when its tasks are one tight dependency chain that genuinely cannot be split. That is a legitimate (if fat) single-worker phase, not a smell.

This keeps phase boundaries meaningful while letting the packing hit its target worker count.

### 5. Validate Before Presenting (MANDATORY)

Before showing tasks to the user, run ALL four pre-approval checks. These are NOT optional - they are gates. If any check fails, restructure the Tickets and tasks and re-run until all pass.

**Deterministic backing (run it, do not eyeball it).** `python3 <skill-dir>/scripts/validate_tasks.py <tasks-path-or-feature>` enforces the structural half of these checks so they cannot drift: it flags a `Where` that names multiple files (granularity smell, Check 1), a diagram edge with no matching `Depends on` within a phase and vice-versa (Check 2), a task missing its `Tests` or `Gate` field, a `Tests: none` to confirm against the matrix (Check 3), any dependency pointing to a later phase, and the Ticket rules (Check 4). A non-zero exit means restructure before presenting. The script checks structure; you still build the two tables below (the layer-to-test co-location judgment is yours). If no code-execution tool is available, run the checks by reading `tasks.md`.

**Check 1: Task Granularity** - verify each task is atomic (see Granularity Check section).

**Check 2: Diagram-Definition Cross-Check** - verify the execution diagram matches every task's `Depends on` field (see Diagram-Definition Cross-Check section). Build the cross-check table and include it in the output.

**Check 3: Test Co-location Validation** - verify every task's `Tests` field matches the **Test Coverage Matrix** generated above (see Test Co-location Validation section). Build the validation table and include it in the output.

**Check 4: Tickets** - `validate_tasks.py` reads the `## Tickets` section and fails when any of these is true:

- **The `## Tickets` section is missing.** It is a required section at every scope, next to `Test Coverage Matrix`, `Gate Check Commands`, `Execution Plan` and `Task Breakdown`.
- **A task is listed in no Ticket.** Every `T<n>` in the Task Breakdown must appear in the `**Tasks**` field of some Ticket. This includes fix tasks appended later: a fix task passes when it is listed in a fix Ticket.
- **A task is listed in more than one Ticket.** The error names the task and both Tickets.
- **A Ticket's `**Blocked by**` names a Ticket that is not listed before it.** Blocking edges point backward only; `none` means the Ticket can start immediately.

The script finds Tickets by their `### K<n>:` headings under the `## Tickets` heading and reads only the `**Tasks**` and `**Blocked by**` fields, so keep that markup exact. What it cannot check is yours to check by reading: each Ticket is about one day and demoable alone, `**Delivers**` states a user-visible outcome, and the `**Covers**` fields together name every acceptance criterion and Scenario of the Spec.

For a **legacy plan** (the `spec.md` beside `tasks.md` has no `**Grilling Record**:` line, see [decisions.md](decisions.md) section 4) a missing `## Tickets` section and the Ticket rules are reported as warnings, not errors. A legacy plan is not rewritten to add Tickets; a native plan always has them.

**Output both tables with the tasks** so the user can see the validation results. Any ❌ means you MUST restructure before presenting - do not show failing tasks to the user and ask them to approve.

**Note on the generated matrix:** The two sections (`Test Coverage Matrix`, `Gate Check Commands`) are provisional - generated from codebase sampling or user input and included in this file for user review. They become authoritative at Execution Approval, after `/spec-review`. Agreeing to the task list itself is provisional and never starts Execute ([review.md](review.md)).

**Scenario assignment:** every task whose `Tests` field is not `none` names the Scenario IDs it proves or delivers in a `**Scenarios**` field (`test` and `inspect` Scenarios alike), and every Scenario in the spec is assigned to some task. `validate_tasks.py` enforces both.

**Tickets are not published here.** The Tasks phase only writes Tickets into `tasks.md`. Creating issues on the tracker happens later and only when the user explicitly says "publish tickets", after a Spec Review whose Findings all have Dispositions ([tickets.md](tickets.md)). Never offer to publish as part of presenting the tasks, and never add a `**Tracker**` line yourself: publishing writes it.

**Fix Tickets come later.** When a Verifier round or a Change Review produces fix tasks, they are appended to this file together with one new fix Ticket for that round ([tickets.md](tickets.md)). Every fix task belongs to a Ticket like any other Task.

### 6. ASK About MCPs and Skills

**CRITICAL**: Before execution, ask the user:

> "For each task, which tools should I use?"
>
> **Available MCPs**: [list from project or user]
> **Available Skills**: [list from project or user]

---

## Template: `.specs/features/[feature]/tasks.md`

```markdown
# [Feature] Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `spec-driven` skill: **activate it by name and follow its Execute flow and Critical Rules.** Do not search for skill files by filesystem path. The skill is the source of truth for the full flow (Execution Approval, per-task cycle, sub-agent delegation, adequacy review, Verifier, discrimination sensor).

**Do not start before Execution Approval:** a `/spec-review` ran, its Findings have Dispositions, and the human said to execute.

**If the skill cannot be activated, STOP and tell the user - do not proceed without it.**

---

**Spec**: `.specs/features/[feature]/spec.md`
**Design**: `.specs/features/[feature]/design.md` (Medium scope and above; leave the line out when a Small feature has no design)
**Grilling Record**: `.specs/decisions/[slug].md`
**Status**: Draft | Approved | In Progress | Done

---

<!-- The two sections below are generated by step 1.5 of the Tasks process and filled in during task creation. Do not manually populate them - they are produced by the agent from codebase sampling. -->

## Test Coverage Matrix

[Generated in step 1.5 - see process above]

## Gate Check Commands

[Generated in step 1.5 - see process above]

---

## Tickets

<!-- Written in step 2.1, BEFORE any Task is cut. One block per Ticket, in dependency order. Each Ticket is about one day of work and demoable on its own. A Small feature has exactly one Ticket, K1, listing every Task. -->

### K1: [Ticket title - the deliverable, in the user's terms]
**Delivers**: [what works for the user once this Ticket is done - one or two sentences, no file paths]
**Covers**: [FEAT]-01, [FEAT]-02 · [FEAT]-01.S1, [FEAT]-02.S1
**Blocked by**: none
**Tasks**: T1, T2, T3

### K2: [Ticket title]
**Delivers**: [user-visible outcome]
**Covers**: [FEAT]-03, [FEAT]-04 · [FEAT]-03.S1, [FEAT]-04.S1
**Blocked by**: K1
**Tasks**: T4

<!--
Field rules:
- Heading: `### K<n>: <title>`, numbered K1, K2, ... in listing order. `K` never collides with task IDs (`T<n>`).
- **Delivers**: the outcome from the user's or product team's view.
- **Covers**: the acceptance criterion IDs, then `·`, then the Scenario IDs this Ticket delivers. Together the Tickets cover every criterion and Scenario of the Spec.
- **Blocked by**: `none`, or the IDs of Tickets listed EARLIER in this section. Never a later Ticket.
- **Tasks**: the IDs of the Tasks that make up this Ticket. Every Task in the Task Breakdown is listed in exactly one Ticket.
- **Tracker**: do not write this line. It is added by "publish tickets", right after the Ticket's issue is created, and holds the issue ID (see the tickets reference).
- Fix Tickets are appended here later, one per Verifier round or Change Review, for example `### K3: Fix Verifier round 1` or `### K4: Fix CR1`, with the same four fields.
-->

---

## Execution Plan

Each phase is one Ticket. Phases are ordered and run sequentially - each phase completes before the next begins, and tasks within a phase execute in order.

### Phase 1: K1 [Ticket title]

```
T1 → T2 → T3
```

### Phase 2: K2 [Ticket title]

```
T4
```

---

## Task Breakdown

### Phase 1: K1 [Ticket title]

#### T1: [Create X Interface]

**What**: [One sentence: exact deliverable]
**Where**: `src/path/to/file.ts`
**Depends on**: None
**Reuses**: `src/existing/BaseInterface.ts`
**Requirement**: [FEAT]-01

**Tools**:

- MCP: `filesystem` (or NONE)
- Skill: NONE

**Done when**:

- [ ] Interface defined with all methods from design
- [ ] Types exported correctly
- [ ] No TypeScript errors

**Tests**: [unit/e2e/integration/inspect/none - from coverage matrix]
**Scenarios**: [none - this task proves no Scenario]
**Gate**: [quick/full/build - from gate check commands]

---

#### T2: [Implement Y Service]

**What**: [Exact deliverable]
**Where**: `src/services/YService.ts`
**Depends on**: T1
**Reuses**: `src/services/BaseService.ts` patterns
**Requirement**: [FEAT]-01, [FEAT]-02

**Tools**:

- MCP: `filesystem`, `context7`
- Skill: NONE

**Done when**:

- [ ] Implements interface from T1
- [ ] Handles error cases from design
- [ ] Gate check passes: `[quick gate command from the Gate Check Commands above]`
- [ ] `validate_scenarios.py [feature] --only [FEAT]-01.S1,[FEAT]-02.S1` passes (only `test` Scenario IDs are passed to `--only`; never an `inspect` ID)
- [ ] Test count: [N] tests pass (no silent deletions)

**Tests**: unit
**Scenarios**: [FEAT]-01.S1, [FEAT]-02.S1
**Gate**: quick

---

#### T3: [Write the Z agent prompt]

**What**: [Exact deliverable - a change no test can exercise]
**Where**: `prompts/z-agent.md`
**Depends on**: T2
**Reuses**: `prompts/base-agent.md` structure
**Requirement**: [FEAT]-03

**Tools**:

- MCP: `filesystem`
- Skill: NONE

**Done when**:

- [ ] The prompt states every Then step of [FEAT]-03.S1 explicitly
- [ ] Follows the structure of the existing prompts
- [ ] Gate check passes: `[build gate command from the Gate Check Commands above]`

**Tests**: inspect
**Scenarios**: [FEAT]-03.S1
**Gate**: build

---

### Phase 2: K2 [Ticket title]

#### T4: [Add A Feature to Y]

**What**: [Exact deliverable]
**Where**: `src/services/YService.ts` (modify)
**Depends on**: T3
**Reuses**: Existing service patterns
**Requirement**: [FEAT]-04

**Tools**:

- MCP: `filesystem`, `github`
- Skill: `api-design`

**Done when**:

- [ ] Feature works per acceptance criteria
- [ ] Gate check passes: `[full gate command from the Gate Check Commands above]`
- [ ] Test count: [N] tests pass (no silent deletions)

**Tests**: integration
**Scenarios**: [FEAT]-04.S1
**Gate**: full

**Commit**: `feat([scope]): [description]`

---

## Phase Execution Map

Visual representation of task ordering. Phases run in sequence, and tasks within a phase run in order:

```
Phase 1 (K1) → Phase 2 (K2)

Phase 1:  T1 ------→ T2 ------→ T3
Phase 2:  T4
```

Execution is strictly sequential - there is no intra-phase parallelism. A single agent (or batch worker) works one task at a time, in order.

**How phase-based execution works:**

At Execute, the agent counts total tasks and packs phases into **task-budgeted batches** (~7 tasks
per worker, whole phases - the benchmarked sweet spot is ~20 tasks → ~3 workers). A **phase** is the
semantic/dependency unit; a **batch** is one or more *consecutive whole phases* assigned to one
worker. The cut only ever lands on a phase boundary - a phase is never split across workers. When
packing yields more than one batch (> ~8 tasks), the agent offers to dispatch batch sub-agents.
Batches run sequentially: each worker executes ALL its tasks in order, then reports a compact summary
before the next batch starts. This right-sizes the worker count by workload instead of by phase
count (one-per-phase is too fragmented; expensive and slow). See [sub-agents.md](sub-agents.md) for
the full model - packing algorithm, offer-then-confirm, worker payload, compact summary contract,
failure handling, and context sizing guidance.

When the whole feature fits a single batch (≤ ~8 tasks), execution happens inline in the main window
with no sub-agents spawned.

**The orchestrating agent's role during Execute:**
1. Count total tasks and pack phases into ~7-task batches - offer batch sub-agents if that yields more than one batch and the user accepts
2. Dispatch the next batch (to a worker, or execute inline)
3. Receive the compact batch summary
4. Update tasks.md with results
5. If the batch summary shows all tasks complete: proceed to the next batch
6. If a task failed: decide fix/escalate before dispatching the next batch

---

## Task Granularity Check

Before approving tasks, verify they are granular enough:

| Task                            | Scope         | Status       |
| ------------------------------- | ------------- | ------------ |
| T1: Create email input          | 1 component   | ✅ Granular  |
| T2: Add validation function     | 1 function    | ✅ Granular  |
| T3: Create form with all fields | 5+ components | ❌ Split it! |
| T4: Connect to API              | 1 function    | ✅ Granular  |

**Granularity check**:

- ✅ 1 component / 1 function / 1 endpoint = Good
- ⚠️ 2-3 related things in same file = OK if cohesive
- ❌ Multiple components or files = MUST split

---

## Diagram-Definition Cross-Check

Before approving tasks, verify the execution diagram is consistent with the task definitions. These are independent artifacts that can drift - the diagram is drawn for visual clarity while task bodies are written for precision. Both must agree.

For each task, check:

| Task | Depends On (task body) | Diagram Shows | Status |
| ---- | ---------------------- | ------------- | ------ |
| T[N] | [deps from body] | [deps from diagram arrows] | ✅ Match or ❌ Mismatch |

**Rules:**

- Every `Depends on` in a task body must have a corresponding arrow in the diagram.
- Every arrow in the diagram must correspond to a `Depends on` in the target task's body.
- A task must never depend on a task in a later phase - dependencies point backward or within the same phase only.

---

## Test Co-location Validation

Before approving tasks, verify EVERY task's `Tests` field is consistent with the **Test Coverage Matrix** generated above. This is a hard gate - tasks that fail this check MUST be fixed.

For each task, check: does the task create or modify a code layer that has a required test type in the coverage matrix? If yes, the task's `Tests` field MUST match.

| Task | Code Layer Created/Modified | Matrix Requires | Task Says | Status |
| ---- | --------------------------- | --------------- | --------- | ------ |
| T[N]: [name] | [layer from coverage matrix] | [test type] | [task's Tests field] | ✅ OK or ❌ VIOLATION |

**Rules:**

- "Tested in another task" is NOT a valid justification for `Tests: none`. That is test deferral - the exact anti-pattern this validation prevents.
- `Tests: none` is only valid when the coverage matrix says "none" for that code layer.
- `Tests: inspect` is only valid when the coverage matrix gives that layer proof type `inspect`. The task still names its Scenarios; the Verifier proves them.
- If a task creates MULTIPLE code layers (e.g., service + controller), use the HIGHEST test type required by any of them.
- Any ❌ VIOLATION → restructure the task to include its required tests before proceeding.

**Resolving compilation dependencies:**

When a task creates code that can't be tested until a later task completes (e.g., a controller that needs module wiring before its e2e tests can run), do NOT defer the tests to a separate task. Instead, restructure:

1. **Merge forward:** Move the untestable task's tests into the earliest task where they become runnable (e.g., the wiring task includes wiring + e2e tests for the controller it enables).
2. **Merge backward:** Absorb the blocking dependency into the current task so it becomes self-testable (e.g., controller task includes its own module registration).

Pick whichever option keeps tasks atomic and cohesive. The goal: no task produces unverified code. If code can't be tested in the task that creates it, the task boundaries are wrong.

---

## Tips

- **Tickets first** - slice the Spec into day-sized, demoable Tickets, then cut each Ticket into Tasks; never group a flat task list afterwards
- **Every scope has Tasks and Tickets** - a Small feature gets one Ticket that lists every Task
- **One Task, one Ticket** - every Task is listed in exactly one Ticket's `Tasks` field
- **Phases are ordered** - One phase per Ticket; each phase completes before the next; tasks run in order within a phase
- **Reuses = Token saver** - Always reference existing code
- **Tools per task** - MCPs and Skills prevent wrong approaches
- **Dependencies are gates** - Clear what blocks what
- **Done when = Testable** - If you can't verify it, rewrite it
- **Requirement ID = Traceable** - Every task traces back to a spec requirement
- **Scenarios = proposed proofs** - Each task names the Scenarios it proves (`test`) or delivers (`inspect`); the Spec Reviewer judges them before anything is built
- **Publishing is separate** - Tickets reach the tracker only on an explicit "publish tickets" ([tickets.md](tickets.md))
- **One commit per task** - Plan the commit message format in advance

---

## Task Verification Standards

Every task MUST follow the `Done when` + `Tests` + `Gate` fields defined in the **Task Breakdown** template above. Each `Done when` entry must be specific, testable (binary pass/fail), and reference the gate check command from the `Gate Check Commands` section. Include the expected test count to prevent silent deletions.
