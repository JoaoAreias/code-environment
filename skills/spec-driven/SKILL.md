---
name: spec-driven
description: Feature planning and implementation in 4 phases (Specify, Design, Tasks, Execute), with human-triggered Spec and Change Reviews and explicit Execution Approval. Specify grills the user one question per turn and writes every Decision into a Grilling Record; Design is required at Medium scope and above; Tasks always runs and slices the work into day-sized Tickets of atomic tasks; Execute builds test-first with atomic Conventional Commits; an independent Verifier checks every Scenario (author != verifier, evidence-or-zero). Writes EARS acceptance criteria with Gherkin Scenarios as the test contract, searches the codebase with graphify before adding anything, applies Repo Standards plus a smell baseline, and ships deterministic Python gates and a self-improving lessons layer. Use when (1) planning features, (2) implementing or fixing code with verification, (3) validating an implementation against a spec. Triggers on "specify feature", "design", "tasks", "publish tickets", "implement", "validate", "verify work", "UAT", "pause work", "resume work". Do NOT use for pure architecture decomposition analysis or standalone technical design documents.
---

# Spec-Driven Development

Plan and implement features with precision. Granular tasks. Clear dependencies. Right tools. Zero ceremony.

```
SPECIFY → DESIGN → TASKS + TICKETS → /spec-review → Execution Approval → EXECUTE → Verifier → /code-review
the grill  Medium+   every scope       human-run      human go-ahead       required   automatic   human-run
```

- **Specify** is the grill: one question per turn, written into a Grilling Record as it goes.
- **Design** is required at Medium scope and above.
- **Tasks** runs at every scope and slices the work into day-sized Tickets made of atomic Tasks.
- After a Spec Review's Dispositions, the human may say **"publish tickets"** at any time; it is optional and separate from Execution Approval.
- The **Verifier** runs automatically after the last Task. `/spec-review` and `/code-review` are run by the human, never by you.

## Critical Rules (read before acting)

**Loading this skill's files.** Reference files live under `references/` in this skill's own directory (where this `SKILL.md` resides). Resolve them relative to the skill directory - never the workspace root - and load them through the active skill by name; never assume a fixed install path. When a step tells you to read a reference, **read it completely (to EOF)** before acting - never act on a partial/truncated read.

**Running this skill's scripts.** Every `scripts/*.py` shipped with this skill lives under that same skill directory. Resolve the skill directory first, then invoke `python3 <skill-dir>/scripts/<name>.py ...`. Never run `python3 scripts/...` from the consuming project root - that looks for a project-local `scripts/` tree that is not this skill. Project data under `.specs/` is still read/written relative to the project root (pass `--root` when the cwd is elsewhere). Below, `<skill-dir>` means the directory that contains this `SKILL.md`.

**Execution contract - every task, non-negotiable (holds even if you do not open the reference files):**

1. **Scenarios are the contract.** Every test proves exactly one Gherkin Scenario from the spec and carries its ID and Given/When/Then text; tests assert spec-defined outcomes and never mirror the implementation. See [standards.md](references/standards.md) section 3.
2. The gate must pass (tests pass) before a task is done - the test runner decides, not self-assessment.
3. One atomic commit per task. Mark the task complete in `tasks.md` (and update spec traceability when used) **before** that commit, and include those updates in the same commit. Never batch tasks; never weaken or skip a test that proves a Scenario. A pre-existing test without a Scenario that the task touches is claimed by a back-filled Scenario or dropped - never kept alive with a Legacy Path.
4. After the LAST task, a fresh **Verifier always runs automatically** (author ≠ verifier) - Scenario-anchored outcome check + discrimination sensor. It is never optional and never prompted. See Sub-Agent Delegation.
5. **Execution Approval:** nothing is built until the human explicitly says to execute, after a human-run `/spec-review` whose Findings all have Dispositions. Agreeing to a spec, design or task list is provisional and authorizes nothing; so is accepting a Finding. Never run `/spec-review` or `/code-review` yourself. See [review.md](references/review.md).
6. **Blast radius:** Execution Approval authorizes local implementation and local commits only. `git push`, force-push, deploy, production DB changes, and other remote / externally visible / destructive operations require an explicit go-ahead for that action.
7. **Search before you add.** Before any new capability, component or exported symbol, look for an existing equivalent with graphify and record what you searched ([standards.md](references/standards.md) section 4).
8. **Implementation happens only through spec-driven.** Every Change an agent builds, a one-line bug fix included, goes through this flow: a spec (Small scope for a small fix), `tasks.md`, a human-run `/spec-review`, Execution Approval, Execute, the Verifier. There is no shortcut and no exception. No other skill builds production code: a diagnosis, a prototype or a grill ends by handing its result to Specify. Never build straight from a tracker issue, a chat request or a teammate's document.
9. **Tickets are published only on a go-ahead.** Create or update tracker issues only when the user explicitly says "publish tickets", and only when a Spec Review exists and every Finding of the latest one has a Disposition. Write each Tracker ID into `tasks.md` right after its issue is created, never create a second issue for a Ticket that already has a Tracker ID, and stop at the first tracker failure. Publishing never starts Execute, and Execution Approval never publishes. See [tickets.md](references/tickets.md).
10. **Foreign plans are never edited.** A plan written outside spec-driven (a teammate's PRD, RFC or design document, another tool's spec folder) is read as input and may be reviewed, but you never edit it, reformat it or run the structural validators on it, and you never execute it directly: building from it starts with Specify, which writes a native spec that links it ([decisions.md](references/decisions.md) section 4).
11. **`graphify-out/` is never deleted.** `graphify-out/` is the graph cache: the code graph that the capability search, the reviewers and `graph_queries.py` read. It may be gitignored or listed in `.git/info/exclude`; ignored does not mean disposable. Never delete it, clean it up, move it or remove any file inside it, in any phase and for any reason: not as "untracked clutter", not to "start fresh", not with `git clean -x`, not because a tree should be clean. When you finish a phase, `graphify-out/graph.json` is still there. If you need a newer graph, refresh it with `graphify update .` and nothing else ([standards.md](references/standards.md) section 4).
12. **Decisions live in Grilling Records.** Every Decision is written into a Grilling Record under `.specs/decisions/` by the phase that made it, and a changed Decision is rewritten in place with a `Changed` line. Never write an ADR, an `AD-NNN` entry or a per-feature `context.md`; those exist only as legacy decision sources that are read. Before planning, building or judging, find the Decisions that apply with the read rule in [decisions.md](references/decisions.md).

**Deterministic gates run before human review - not from memory.** The structural gates for the spec and tasks are enforced by scripts in this skill's `scripts/` directory, so they cannot silently drift when the model forgets a step:

- Before presenting a spec: `python3 <skill-dir>/scripts/validate_spec.py <spec-path-or-feature>` (closure gate: required sections incl. `Existing Capabilities`, `Standards` and `Decisions & Assumptions`, EARS-shaped ACs with IDs, at least one Scenario per AC, filled Decisions and Assumptions rows, traceability).
- Before presenting tasks: `python3 <skill-dir>/scripts/validate_tasks.py <tasks-path-or-feature>` (a `## Tickets` section, every task in exactly one Ticket, `Blocked by` naming only earlier Tickets, granularity smell, diagram-vs-`Depends on` parity within a phase, no forward-phase dependency, every task carries `Tests` + `Gate`, every task with tests names its `Scenarios`, every Scenario is assigned).
- In each task's gate and in the Verifier: `python3 <skill-dir>/scripts/validate_scenarios.py <feature> [--only <ids>] [--since <base>]` (tests carry known Scenarios with undrifted text; touched tests are claimed; an `inspect` Scenario is proven by its PASS row in `validation.md`). A task's gate passes only its `test` Scenario IDs to `--only`; the Verifier checks every Scenario.
- On each commit: `python3 <skill-dir>/scripts/check_commit.py --message "<msg>"` (Conventional Commits). Optionally wire it as a git `commit-msg` guard (git only, no agent dependency) - see [implement.md](references/implement.md).
- Before declaring a feature done: `python3 <skill-dir>/scripts/validate_state.py <feature>` (completion gate: the Verifier's `validation.md` exists, its verdict is filled to PASS, and it cites `file:line` evidence - a missing, FAIL, placeholder, or evidence-free report fails). The closing step of Execute runs this automatically, the same way the lessons layer runs at distillation; it is not a manual step.

A non-zero exit means STOP and fix before proceeding. Skip a script only when no code-execution tool is available; then perform the same checks by reading the artifact.

**Before Execute:** confirm Execution Approval ([review.md](references/review.md)); read [implement.md](references/implement.md) completely and run `<skill-dir>/scripts/validate_tasks.py`; if `tasks.md` packs into more than one task-budgeted batch (> ~8 tasks), present the sub-agent offer first (see Sub-Agent Delegation).

## Auto-Sizing: The Core Principle

**The complexity determines the depth of each phase, not whether the plan exists.** Before starting any feature, assess its scope. Every scope gets a spec, a `tasks.md` with Tickets, a Spec Review and an Execution Approval; what changes is how deep each phase goes:

| Scope       | What                     | Specify                                                   | Design                                                              | Tasks                                                   | Execute                                               |
| ----------- | ------------------------ | --------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------- | ----------------------------------------------------- |
| **Small**   | ≤3 files, one sentence   | Short grill + minimal `spec.md` (`Scope: Small`)          | Skip, unless the change holds an architectural choice               | `tasks.md`: one Ticket listing every Task               | Implement + verify per task                           |
| **Medium**  | Clear feature, <10 tasks | Grill + spec (brief), sweep of the dimensions present     | **Required**: components, reuse table, links to its Decisions       | `tasks.md`: day-sized Tickets, each cut into Tasks      | Implement + verify per task                           |
| **Large**   | Multi-component feature  | Grill + full spec + requirement IDs, full sweep           | **Required**: architecture + components, approach question          | `tasks.md`: Tickets + full breakdown + dependencies     | Implement + verify per task                           |
| **Complex** | Ambiguity, new domain    | Full spec + [full grill and sweep](references/specify.md) | **Required**: [research](references/design.md) + architecture       | `tasks.md`: Tickets + breakdown + phase plan            | Implement + [interactive UAT](references/validate.md) |

**Rules:**

- **Specify, Tasks and Execute are required at every scope** - you always need to know WHAT, see the work laid out, and DO it
- **Specify is the grill** at every scope: one question per turn, written into a Grilling Record as it goes ([specify.md](references/specify.md)); there is no separate discuss step
- **Design is required at Medium scope and above** ([design.md](references/design.md)). Only a Small change with no architectural choice skips it. Design records its Decisions in the feature's Grilling Record
- **Tasks runs at every scope, Small included** ([tasks.md](references/tasks.md)). It slices the Spec into Tickets of about one day each, then cuts each Ticket into atomic Tasks. Tasks are never left implicit and never listed inline in place of `tasks.md`: the user reviews the work through that file
- **Every scope ends planning the same way:** the human runs `/spec-review`, records Dispositions, and gives Execution Approval - Small included. `/spec-review` stops when `tasks.md` is missing, or when `design.md` is missing at Medium scope and above
- **Interactive UAT is triggered within Execute** only for user-facing features with complex behavior

## .specs Structure

```
.specs/
├── STATE.md            # Project memory: the Handoff snapshot only (an old `## Decisions` log is a legacy decision source)
├── LESSONS.md          # Self-improving lessons playbook (rendered by scripts/lessons.py - do not hand-edit)
├── lessons.json        # Canonical lessons state (machine-owned)
├── decisions/          # Every Decision, in Grilling Records
│   ├── summary.md          # Index: one row per finished Grilling Record, plus the legacy decision sources
│   └── [slug].md           # One Grilling Record per grilling session; a feature's record also holds its Design and Review Decisions
├── reviews/            # Spec Reviews of foreign plans (plans written outside spec-driven)
│   └── [plan slug]/
│       └── spec-review-N.md
└── features/           # Feature specifications
    └── [feature]/
        ├── spec.md         # Requirements with traceable IDs; links its Grilling Record
        ├── design.md       # Architecture & components (Medium scope and above)
        ├── tasks.md        # Tickets and their atomic Tasks, with verification (every scope)
        ├── spec-review-N.md    # Spec Reviewer report, one per run, with Dispositions
        ├── validation.md   # Verifier report: PASS/FAIL, per-Scenario evidence, sensor result, diff range
        └── change-review-N.md  # Change Reviewer report, one per run, with Dispositions
```

**Create artifacts lazily.** Write each file only when its phase actually produces content - never scaffold an empty `design.md` or `tasks.md` up front. An empty file signals a phase happened when it did not. The only plan file that may be absent when planning ends is the `design.md` of a Small feature. The deterministic scripts (`validate_spec.py`, `validate_tasks.py`, `validate_scenarios.py`, `check_commit.py`, `validate_state.py`, `lessons.py`, `prep_review.py`, `graph_queries.py`) ship inside this skill's own `scripts/` directory.

**The graph cache.** `graphify-out/` (the code graph) sits at the repository root and usually stays out of git, through `.gitignore` or `.git/info/exclude`. It is a cache you keep: never delete it, refresh it with `graphify update .` (Critical Rule 11).

**Older files you may meet.** A feature folder written under older rules may hold a legacy decision file beside its spec, and a repository may hold `docs/adr/` or a `## Decisions` log in `STATE.md`. These are legacy decision sources: read them through [decisions.md](references/decisions.md), and never create or extend them.

## Workflow

**New feature:**

1. Specify (the grill, writes the Grilling Record, then `spec.md`) → Design (Medium scope and above) → Tasks (Tickets, then Tasks; every scope)
2. Human runs `/spec-review` → Dispositions → plan edits, with changed Decisions rewritten in place in the record → (another `/spec-review` if the human wants) → Execution Approval
3. Optional, at any time after the Dispositions and only when the human says "publish tickets": publish the Tickets to the tracker ([tickets.md](references/tickets.md))
4. Execute → Verifier (automatic). Verifier gaps become fix tasks in one fix Ticket for that round. When the Verifier passes, tell the human that `/code-review` is available; never run it yourself
5. Human runs `/code-review` → Dispositions → accepted Findings become fix tasks in one fix Ticket for that review → Execution Approval → Execute → Verifier

**Starting from someone else's plan:** a foreign plan is input to Specify, which asks only about its gaps and writes a native spec that links it. To review one without building, the human runs `/spec-review <path>`; the report goes under `.specs/reviews/`.

**Resume work:**

1. Read `.specs/STATE.md` (`## Handoff`).
2. Reconcile Handoff against git (`branch`, `status --porcelain`, recent commits) and `tasks.md` - evidence wins over a stale snapshot. Full procedure: [memory.md](references/memory.md).
3. Re-read the Decisions that apply with the read rule in [decisions.md](references/decisions.md).
4. Propose the reconciled next step before writing code.

## Context Loading Strategy

**On-demand load (only what the current task needs):**

- `.specs/STATE.md` - Handoff section (read on resume only)
- Decisions - at the start of every phase, through the read rule in [decisions.md](references/decisions.md): `.specs/decisions/summary.md`, then only the Grilling Records that apply, then the legacy decision sources that exist
- confirmed lessons - load at Specify and Design via `python3 <skill-dir>/scripts/lessons.py list --status confirmed` ([lessons.md](references/lessons.md)); confirmed only, never candidates
- [standards.md](references/standards.md) - at Specify (discover Repo Standards), Design, and before each task
- [review.md](references/review.md) - before Execute (Execution Approval) and after a reviewer returns
- spec.md (when working on a specific feature)
- the feature's Grilling Record (when designing, or when a spec row needs its full reasoning)
- design.md (when implementing from design)
- tasks.md (when executing tasks)
- [tickets.md](references/tickets.md) - at Tasks (slicing), when fix tasks are added, and on "publish tickets"

**Never load simultaneously:**

- Multiple feature specs
- Multiple architecture docs
- Grilling Records the read rule did not select

**Target:** <40k tokens total context
**Reserve:** 160k+ tokens for work, reasoning, outputs
**Monitoring:** Display status when >40k (see [context-limits.md](references/context-limits.md))

## Sub-Agent Delegation

**Trigger:** count total tasks. If the feature packs into more than one task-budgeted batch (> ~8 tasks) → offer sub-agents; if it fits a single batch (≤ ~8 tasks) → execute inline.

**Offer-then-confirm** - never auto-spawn. The user must accept before any sub-agent is dispatched.

**One worker per task-budgeted batch (~7 tasks, whole phases):** Phases stay the semantic/dependency unit; a **batch** is the execution unit - one or more *consecutive whole phases* packed to ~7 tasks. Walk phases in order, accumulate whole phases into the current batch until it reaches the budget, then start the next - **never split a phase** across workers. ~20 tasks → ~3 workers; scales linearly (40 → ~6). Each worker executes all its tasks in order (implement → gate → atomic commit), then reports a compact summary (tasks done, commit hashes, test counts, deviations). Batches run sequentially - a batch never starts until the previous one reports all tasks complete. Workers never spawn further sub-agents.

**Verifier (always-on, never prompted):** After the final task is committed, the orchestrator dispatches a fresh Verifier sub-agent automatically - regardless of phase count. Validation never requires a user prompt; it is the closing step of Execute. **Author ≠ verifier**: the Verifier re-derives coverage independently using evidence-or-zero; it does not inherit the author's mental model. The Verifier: (1) performs a **Scenario-anchored outcome check** - runs `validate_scenarios.py`, confirms each test's asserted value matches its Scenario's expected outcome, flags spec-precision gaps; (2) runs a **discrimination sensor** - injects behavior-level faults in an isolated scratch (temp worktree or file copies - never `git stash`), confirms tests kill them, discards the scratch and verifies real-tree porcelain matches the pre-sensor baseline; surviving mutants become fix tasks; (3) writes `.specs/features/[feature]/validation.md` (PASS/FAIL, per-AC evidence, sensor result, diff range); (4) returns a compact verdict + ranked gap list to the orchestrator in chat. Gaps become fix tasks, grouped in one fix Ticket per Verifier round ([tickets.md](references/tickets.md)); the fix→re-verify loop is bounded to 3 iterations before escalating. (5) **distills lessons** - turns each grounded failure (surviving mutant, spec-precision gap, failed AC, SPEC_DEVIATION) into a reusable project-local lesson via `<skill-dir>/scripts/lessons.py`; a clean PASS records nothing (see [lessons.md](references/lessons.md)).

**Model tier per role (only if the harness supports choosing a model per sub-agent).** Match the reasoning cost to the work instead of paying top-tier reasoning for boilerplate. A batch worker on a mechanical, low-ambiguity phase (entities, config, wiring, straightforward CRUD) runs on a faster/cheaper tier; a worker on a core-domain or high-ambiguity phase, and the Design phase itself, runs on a high-reasoning tier; the Verifier runs on a mid-to-high tier because it does adversarial reasoning and designs mutations. This is a portable recommendation: if the harness cannot set a per-sub-agent model, ignore it. Full rubric in [sub-agents.md](references/sub-agents.md).

**Standalone fallback:** Without sub-agents, run `validate.md` as an independent fresh-eyes pass after the final commit - including the spec-anchored check and discrimination sensor.

Full mechanics (worker payload, compact summary format, failure handling, context sizing, model tier, Verifier report format): [sub-agents.md](references/sub-agents.md).

## Commands

**Feature-level (auto-sized):**
| Trigger Pattern | Reference |
|----------------|-----------|
| Specify feature, define requirements, build from a teammate's plan | [specify.md](references/specify.md) |
| Design feature, architecture | [design.md](references/design.md) |
| Break into tasks, create tasks, slice into Tickets | [tasks.md](references/tasks.md) |
| Publish tickets, fix Tickets, Ticket size | [tickets.md](references/tickets.md) |
| Which Decisions apply here, legacy ADRs, native / legacy / foreign plans | [decisions.md](references/decisions.md) |
| Implement task, build, execute | [implement.md](references/implement.md) |
| Validate, verify, test, UAT, walk me through it | [validate.md](references/validate.md) |
| After `/spec-review` or `/code-review` returns; Dispositions; Execution Approval | [review.md](references/review.md) |
| Repo Standards, smell baseline, test quality, search before adding | [standards.md](references/standards.md) |

**Memory:**
| Trigger Pattern | Reference |
|----------------|-----------|
| Record decision, this is a project-level decision | Not a memory entry: the phase that makes a Decision writes it into the feature's Grilling Record ([specify.md](references/specify.md), [design.md](references/design.md), [review.md](references/review.md)) |
| Pause work, end session, I need to stop | [memory.md](references/memory.md) |
| Resume work, continue, pick up where we left off | [memory.md](references/memory.md) |
| Load lessons, what have we learned, apply past lessons | [lessons.md](references/lessons.md) |
| Record lesson, distill lessons (auto-runs after validation) | [lessons.md](references/lessons.md) |

## Knowledge Verification Chain

When researching, designing, or making any technical decision, follow this chain in strict order. Never skip steps.

```
Step 1: Codebase → graphify first (`graphify query`, `graph_queries.py symbols`), then rg; existing code, conventions, patterns
Step 2: Project docs → README, docs/, inline comments, Grilling Records under `.specs/decisions/` (found through references/decisions.md)
Step 3: Context7 MCP → resolve library ID, then query for current API/patterns
Step 4: Web search → official docs, reputable sources, community patterns
Step 5: Flag as uncertain → "I'm not certain about X - here's my reasoning, but verify"
```

**Rules:**

- Never skip to Step 5 if Steps 1-4 are available
- Step 5 is ALWAYS flagged as uncertain - never presented as fact
- **NEVER assume or fabricate.** If you cannot find an answer, say "I don't know" or "I couldn't find documentation for this". Inventing APIs, patterns, or behaviors causes cascading failures across design → tasks → implementation. Uncertainty is always preferable to fabrication.

## Output Behavior

**Do the work; do not narrate the machinery.** Produce the right artifact for the phase instead of announcing the phase ("I will now run the Specify phase"). The user judges the output, not a play-by-play of the process. This keeps the flow from reading as robotic.

**Match effort to the work.** Lightweight steps (feature-level checks, validation, mechanical tasks) do not need top-tier reasoning; heavy steps (complex design, ambiguous features) do. If the harness lets you pick a model per sub-agent, apply the tier rubric in [sub-agents.md](references/sub-agents.md); otherwise proceed and simply invest more care on the heavy steps. Mention this once per session at most, and only if it helps; skip it for an experienced user.

**Write generated artifacts in a plain, decided voice.** Specs, Grilling Records, validation reports, commit messages, and chat summaries follow the writing rules in [coding-principles.md](references/coding-principles.md): lead with the verdict, state decisions definitively, cut filler and mechanical hedging.

## Code Analysis

graphify for relationships and existing concepts, ast-grep and ripgrep for patterns and text. See [code-analysis.md](references/code-analysis.md).
