---
name: tdd
description: The test-first loop that spec-driven Execute runs for each Task, one Scenario at a time (red, then green). Use when spec-driven Execute works a Task, or when the user mentions "red-green-refactor" or asks what makes a good test. It does not build a feature or fix a bug on its own; that work starts in spec-driven.
---

# Test-Driven Development

This skill is the test-first loop that spec-driven's Execute phase runs for each Task. Execute loads it by name, and for every Scenario of the Task whose proof type is `test` it runs one red → green cycle: write that Scenario's test, see it fail, then write the code that makes it pass.

It is not a way to build on its own. A feature, and a bug fix too, starts in spec-driven: Specify writes the Scenarios, the human runs `/spec-review` and gives Execution Approval, and only then does Execute run this loop. If you were asked to "build X test-first" and there is no approved Task for it, do not start a loop here. Say that the work goes through spec-driven (a bug fix is a Small Specify) and start there.

The rest of this file is the reference that makes the loop produce tests worth keeping: what to read first, what a good test is, where tests go, the anti-patterns, and the rules of the loop. Every section applies on every cycle: consult them before and during the loop, not after.

## Before the first test of a Task

Do these reads before you write the Task's first test. A test written without them can encode a choice the project already decided otherwise.

1. **The glossary.** Read `CONTEXT.md` (if it exists) so test names and interface vocabulary match the project's domain language.
2. **The Decisions that bind the code you touch.** Follow the read rule in spec-driven's `references/decisions.md` (`../spec-driven/references/decisions.md` from this skill's directory). That file is the one source of the rule; read it completely and run its steps in order. In short, for the paths the Task touches and the feature it belongs to:
   - **Discovery.** Run the two `fd` listings. If `fd` is not installed, stop and ask the user to install it.
   - **Active Grilling Records.** Read `.specs/decisions/summary.md` and open exactly the records whose Status is `active` and that either bind the project with Areas that overlap the Task's paths (or Areas `*`), or name the Task's feature in Specs. Do not open a record that binds only another feature, and do not open a `draft` record: a draft has no row and its Decisions are not settled.
   - **Root ADRs.** If `docs/adr/` exists at the repository root, read the ADRs that touch the area of the Task. This applies with or without `.specs/decisions/`: a repository that has only `docs/adr/` still has decisions to read.
   - **Per-context ADRs.** If `CONTEXT-MAP.md` exists, it lists the contexts: read `<context>/docs/adr/` for every context the Task's paths fall under. If there is no map, run the probe `fd -t d -p 'docs/adr$' -E .git -E node_modules -E .venv -E venv` and read the ADRs of every directory it finds that sits above the Task's paths, however deep it is.
   - **The feature's `context.md`.** If `.specs/features/<feature>/context.md` exists, read the whole file. It holds decisions the user locked under older rules, and it is read whatever kind of plan the feature has.
   - An old `## Decisions` section in `.specs/STATE.md` is read the same way, for the entries that touch the Task's area.
3. **What they mean for the test.** Every active Decision that binds the project, and every active legacy decision that sets a rule for the code, is a rule the test and the code follow. If the Task cannot be done without contradicting one, stop and surface the conflict by Decision ID or file name. Never work around it silently.

Four examples of step 2:

- `summary.md` lists `billing-rules.md` (project, Areas `src/billing/`, active), `money.md` (project, Areas `*`, active) and `dark-mode.md` (feature, Areas `src/ui/`, active, Specs `dark-mode`). The folder also holds `billing-ledger.md`, a draft with Areas `src/billing/` and no row. A Task that touches `src/billing/invoice.py` for feature `invoice-pdf` opens `billing-rules.md` and `money.md`. It does not open `dark-mode.md` or `billing-ledger.md`.
- A repository has `docs/adr/0002-integer-cents.md` and no `.specs/decisions/` at all. A Task that touches money formatting reads that ADR before writing its test.
- A Task touches `src/billing/total.py`, and the decision that governs it is `src/billing/docs/adr/0002-integer-cents.md`. With a `CONTEXT-MAP.md` that lists `src/billing/`, the map leads to it. Without a map, the `docs/adr$` probe finds `src/billing/docs/adr/`. Either way the ADR is read before the test is written.
- A legacy feature `09-validation-suite` has a `context.md` that locks "tolerance is 1e-6". A fix Task for that feature reads `09-validation-suite/context.md` before writing its test, and the test uses that tolerance.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification: "user can checkout with valid cart" tells you exactly what capability exists, and it survives refactors because it doesn't care about internal structure.

Inside Execute, each test proves exactly one Scenario and asserts the outcome that Scenario's Then steps name. The Scenario is the source of the expected values, never the code.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Seams: where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

**Test only at agreed seams.** The seams are agreed during planning, not in this loop. The Task's Scenarios say what is observed and through which interface, and `design.md` names the components and their interfaces. The human approved both, so that approval is the seam confirmation: do not ask the user to confirm those seams again.

Ask the user only about an interface that neither the Scenarios nor the Design names. Then ask one question about that interface ("the Scenario does not say where this is observed; I would test it through `X`. Is that the right interface?") and wait for the answer. No test is written at a seam that is neither named in the plan nor confirmed this way.

When the shape of that interface is itself in question (how deep the module is, where the seam belongs, what the interface should expose), call the Skill tool with "codebase-design" for the vocabulary. It is the shared source of the module, interface, depth, seam, adapter, leverage and locality terms, and it is a reference to consult, not a session to run.

## Anti-patterns

- **Implementation-coupled**: mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
- **Tautological**: the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth: a known-good literal, a worked example, the spec.
- **Horizontal slicing**: writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead: one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.

## Rules of the loop

- **Red before green.** For each `test` Scenario of the Task: write its test, run it, and see it fail before you edit any production file. Report that failing run (the command and the failure) before the production edit. Then write only enough code to pass it, run the test again, and report the passing run. A test that passes before the code exists has proved nothing: fix the test, or surface that the behavior already exists. Don't anticipate future tests or add speculative features.
- **One slice at a time.** One Scenario, one test, one minimal implementation per cycle.
- **Refactor small, inside the cycle.** With the test green, you may tidy the code this cycle just wrote. Wider restructuring is not part of the loop or of the Task: surface it to the user and leave it out.
- **`inspect` Scenarios have no cycle.** A Scenario whose proof type is `inspect` (a prompt, configuration, infrastructure code) gets no test. The Verifier checks it after the last Task.
- **The loop ends at the Task's gate.** Gate checks, the adequacy review and the commit are Execute's steps, described in spec-driven's `references/implement.md`.
