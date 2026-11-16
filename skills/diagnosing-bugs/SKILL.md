---
name: diagnosing-bugs
description: Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow.
---

# Diagnosing Bugs

A discipline for hard bugs. Skip phases only when explicitly justified.

This skill finds the cause of a bug. It does not fix it. When the root cause is confirmed, Phase 5 hands the repro, the root cause and the seam to spec-driven, which is the only path that builds code.

When exploring the codebase, read `CONTEXT.md` (if it exists) to get a clear mental model of the relevant modules, and read the Decisions that bind the area you're touching. To find them, follow the read rule in spec-driven's `references/decisions.md` (`../spec-driven/references/decisions.md` from this skill's directory). That file is the one source of the rule: read it completely and run its steps in order. A diagnosis has no feature, so open the `active` Grilling Records that bind the project where you work, and check the legacy decision sources it lists.

## Redact

This skill has you show commands, outputs and captured artifacts. **Redact every secret first**: write `<REDACTED>` in its place. Build loops against env vars, so the credential stays in the environment rather than in what you show. Captured artifacts carry auth headers: quote only the lines that carry the signal.

If the redacted output is not enough to diagnose the bug, say so and ask the user.

## Phase 1: Build a feedback loop

**This is the skill.** Everything else is mechanical. If you have a **tight** pass/fail signal for the bug (one that goes red on _this_ bug), you will find the cause; bisection, hypothesis-testing, and instrumentation all just consume it. If you don't have one, no amount of staring at code will save you.

Spend disproportionate effort here. **Be aggressive. Be creative. Refuse to give up.**

### Ways to construct one, in roughly this order

1. **Failing test** at whatever seam reaches the bug: unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) that drives the UI and asserts on DOM/console/network.
5. **Replay a captured trace.** Save a real network request / payload / event log to disk; replay it through the code path in isolation.
6. **Throwaway harness.** Spin up a minimal subset of the system (one service, mocked deps) that exercises the bug code path with a single function call.
7. **Property / fuzz loop.** If the bug is "sometimes wrong output", run 1000 random inputs and look for the failure mode.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through old-version vs new-version (or two configs) and diff outputs.
10. **HITL bash script.** Last resort. If a human must click, drive _them_ with `scripts/hitl-loop.template.sh` so the loop is still structured. Captured output feeds back to you.

Build the right feedback loop, and the bug is 90% fixed.

### Tighten the loop

Treat the loop as a product. Once you have _a_ loop, **tighten** it:

- Can I make it faster? (Cache setup, skip unrelated init, narrow the test scope.)
- Can I make the signal sharper? (Assert on the specific symptom, not "didn't crash".)
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem, freeze network.)

A 30-second flaky loop is barely better than no loop; a 2-second deterministic one is tight, a debugging superpower.

### Non-deterministic bugs

The goal is not a clean repro but a **higher reproduction rate**. Loop the trigger 100×, parallelise, add stress, narrow timing windows, inject sleeps. A 50%-flake bug is debuggable; 1% is not, so keep raising the rate until it's debuggable.

### When you genuinely cannot build a loop

Stop and say so explicitly. List what you tried. Ask the user for: (a) access to whatever environment reproduces it, (b) a redacted captured artifact (HAR file, log dump, core dump, screen recording with timestamps), or (c) permission to add temporary production instrumentation. Do **not** proceed to hypothesise without a loop.

### Completion criterion: a tight loop that goes red

Phase 1 is done when the loop is **tight** and **red-capable**: you can name **one command** (a script path, a test invocation, a curl) that you have **already run at least once** (show the invocation and its output, redacted), and that is:

- [ ] **Red-capable**: it drives the actual bug code path and asserts the **user's exact symptom**, so it can go red on this bug and green once fixed. Not "runs without erroring"; it must be able to _catch this specific bug_.
- [ ] **Deterministic**: same verdict every run (flaky bugs: a pinned, high reproduction rate, per above).
- [ ] **Fast**: seconds, not minutes.
- [ ] **Agent-runnable**: you can run it unattended; a human in the loop only via `scripts/hitl-loop.template.sh`.

If you catch yourself reading code to build a theory before this command exists, **stop: jumping straight to a hypothesis is the exact failure this skill prevents.** No red-capable command, no Phase 2.

## Phase 2: Reproduce + minimise

Run the loop. Watch it go red as the bug appears.

Confirm:

- [ ] The loop produces the failure mode the **user** described, not a different failure that happens to be nearby. Wrong bug = wrong fix.
- [ ] The failure is reproducible across multiple runs (or, for non-deterministic bugs, reproducible at a high enough rate to debug against).
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

### Minimise

Once it's red, shrink the repro to the **smallest scenario that still goes red**. Cut inputs, callers, config, data, and steps **one at a time**, re-running the loop after each cut, and keep only what's load-bearing for the failure.

Why bother: a minimal repro shrinks the hypothesis space in Phase 3 (fewer moving parts left to suspect) and becomes the clean regression test in Phase 5.

Done when **every remaining element is load-bearing**: removing any one of them makes the loop go green.

Do not proceed until you have reproduced **and** minimised.

## Phase 3: Hypothesise

Generate **3–5 ranked hypotheses** before testing any of them. Single-hypothesis generation anchors on the first plausible idea.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

If you cannot state the prediction, the hypothesis is a vibe: discard or sharpen it.

**Show the ranked list to the user before testing.** They often have domain knowledge that re-ranks instantly ("we just deployed a change to #3"), or know hypotheses they've already ruled out. Cheap checkpoint, big time saver. Don't block on it; proceed with your ranking if the user is AFK.

## Phase 4: Instrument

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:

1. **Debugger / REPL inspection** if the env supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup at the end becomes a single grep. Untagged logs survive; tagged logs die.

**Perf branch.** For performance regressions, logs are usually wrong. Instead: establish a baseline measurement (timing harness, `performance.now()`, profiler, query plan), then bisect. Measure first, fix second.

## Phase 5: Hand off to a Small Specify

The diagnosis ends here. When a probe from Phase 4 confirms one hypothesis from Phase 3, you have a root cause. **Do not apply the fix, and do not write the regression test.** A bug fix is a Change like any other, and every Change is built through spec-driven: a Small spec, `tasks.md`, a human-run `/spec-review`, Execution Approval, and only then Execute. This holds for a one-line fix, and it holds when the user says "just fix it": answer that the fix goes through spec-driven and that a Small Specify is the short way there.

Do the four steps below in order.

### 1. State the root cause

Write it in one or two sentences that name the file and line, the hypothesis that was confirmed, and the probe result that confirmed it. For example: "`format_date` in `src/export/dates.py:41` converts the timestamp to UTC before taking the date, so an order placed after 21:00 local time is exported with the next day's date. Confirmed: pinning the timezone to UTC makes the loop go green."

A hypothesis that only looks likely is not a root cause. If no probe has confirmed it, go back to Phase 4.

### 2. Name the seam

The seam is where the regression test for this bug belongs. A correct seam is one where a test exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow (a single-caller test when the bug needs multiple callers, a unit test that can't replicate the chain that triggered the bug), a regression test there gives false confidence.

Name the interface and the file it lives in. You are naming it, not writing a test at it: inside Execute, `tdd` writes the Scenario's test at that seam and sees it fail before any code changes.

**If no correct seam exists, that itself is the finding.** Say so in the hand-off: the codebase architecture is preventing the bug from being locked down, and the spec has to decide what to do about it.

### 3. Leave every production file unchanged

Before you hand off, bring the working tree back to where the diagnosis found it:

- [ ] All `[DEBUG-...]` instrumentation is removed (`grep` the prefix).
- [ ] Every other edit you made to a production file while probing is reverted, including any experimental change that made the loop go green. That change was a probe, not the fix.
- [ ] Throwaway harnesses and prototypes are deleted, or moved to a clearly-marked debug location.
- [ ] `git status` and `git diff` show no change to any production file. Check this; do not assume it.
- [ ] Nothing is committed.

Keep the Phase 1 loop: the one command, and the script or test file behind it if there is one. It is the repro, it is not production code, and it must still go red. Leave it uncommitted.

### 4. Start the Small Specify

Load `spec-driven` by name with your harness's skill tool (the Skill tool in Claude Code, the `skill` tool in opencode), or read `../spec-driven/SKILL.md` from this skill's directory when the harness cannot load a skill by name. Start its Specify phase at **Small** scope and give it these three things as input:

1. **The repro.** The one command from Phase 1, the minimised scenario from Phase 2, the user's exact symptom, and the redacted red output.
2. **The root cause**, as stated in step 1.
3. **The seam**, as named in step 2, or the finding that no correct seam exists.

**The repro is the spec's first Scenario.** Write the minimised scenario as Given and When, and the behavior the user expected, which is the opposite of the symptom, as Then. For the example above:

```gherkin
Scenario: an order placed late in the evening keeps its local date
  Given an order placed at 2026-03-14 22:30 in America/Sao_Paulo
  When the order is exported
  Then the exported date is 2026-03-14
```

Specify gives the Scenario its ID. The root cause goes into the spec's Problem Statement and into the Context of the Grilling Record, so the next debugger learns which hypothesis was correct. The seam tells Specify and `tdd` where the Scenario is observed.

Specify treats what the diagnosis established as given and does not ask it again. It still does its own reading and asks about what the diagnosis did not decide, such as how the fix should behave in neighbouring cases. If the fix turns out to be larger than a Small change, spec-driven's own sizing rules raise the scope; you still start from Small.

From here on, spec-driven's rules apply and this skill has nothing more to do. The fix is written in Execute, after Execution Approval, and the Phase 1 loop going green is how Execute knows the original symptom is gone.
