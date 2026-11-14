# Spec Review SR2 · integrate-skills

- **Reviewed**: commit `42bd695`
- **Inputs read**: spec.md, design.md, tasks.md, `.specs/decisions/grill-in-spec-driven.md`, `.specs/decisions/summary.md`, spec-review-1.md (no `.specs/STATE.md`, no `context.md`)
- **Evidence**: graph refreshed 2026-11-14 11:34 (1071 nodes, 1447 edges) · Sonar: not used (nothing built) · Structural checks: `validate_spec.py` 1 error (the renamed section, expected per the spec's Assumptions row 3), `validate_tasks.py` 0 errors / 23 warnings · Scenario coverage re-counted: 74 Scenarios (24 `test`, 50 `inspect`), each claimed by exactly one Task and covered by exactly one Ticket
- **Reviewer Lessons applied**: none (no confirmed reviewer lessons)

## Dimensions

| Dimension | Status | Findings |
| --- | --- | --- |
| Functional Correctness | not assessable (nothing built yet) | 0 |
| Practical Judgment | assessed | 0 |
| Thought Partnership | assessed | 1 |
| Verification | assessed | 2 |
| Engineering Craft | assessed | 2 |
| Truthful Reporting | assessed | 1 |
| Communication | assessed | 0 |
| Production Risk | assessed | 1 |

## Previous run

| Finding | Disposition | Now |
| --- | --- | --- |
| SR1-F1 | accept | resolved: `**Proof**:` line on every Scenario; K1 (T1-T3) builds the mechanism; GRILL-01..03, REC-01..04, READ-02/03 now claimed by T16 and READ-01, EDGE-01 by T23. New gap in the row format: see SR2-F2 |
| SR1-F2 | accept | resolved: PLAN-01..05, REV-02.S2, D-grill-in-spec-driven.43/.44. New gaps: see SR2-F1 and SR2-F5 |
| SR1-F3 | accept | resolved: slug names (D-grill-in-spec-driven.7), REC-01.S2, Date column (D-grill-in-spec-driven.8) |
| SR1-F4 | accept | resolved: TKT-06.S2, TKT-06.S3, TKT-07.S2 and the four rules in D-grill-in-spec-driven.25 |
| SR1-F5 | accept | resolved: sweep table at `spec.md:140-152`; the two `N/A` lines re-checked and hold |
| SR1-F6 | accept | resolved: TKT-03.S2, TKT-09.S1/S2, D-grill-in-spec-driven.45 |
| SR1-F7 | accept | resolved: EDGE-01.S2/S3, REV-01.S2, D-grill-in-spec-driven.33 |
| SR1-F8 | accept | resolved: GRILL-09.S1/S2 (header-name lookup) in T4 |
| SR1-F9 | reject: tests require the real graphify; fd-missing becomes inspect | not re-raised; READ-06 and READ-04.S1 (`inspect`) added as agreed |
| SR1-F10 | accept | resolved for `prototype` (FLOW-06) and `ready-for-agent` (TKT-06); one more route remains, see SR2-F6 |
| SR1-F11 | accept | mostly resolved: in-place rewriting and the nine split Decisions are in place. A new `retired` status was added that the grill notes did not choose, see SR2-F4 |

## Findings

### SR2-F1 · Foreign-plan review reports are keyed by file basename, so two plans that share a name share one run history
- **Dimension**: Engineering Craft · **Severity**: Major · **Confidence**: high
- **Where**: `design.md:120` and `design.md:257` (agent-decided detail); Spec `PLAN-04`, Scenario `PLAN-04.S1`; Task T10; `skills/spec-driven/scripts/prep_review.py:95-99` (`next_run`)
- **Problem**: A foreign plan's report goes to `.specs/reviews/<basename>-review-<n>.md`, and `<n>` and "Previous run" come from `next_run`, which scans one directory for one prefix. Other flows use fixed file names per feature folder: the spec's own example, `.kiro/specs/payments/` (`spec.md:506`), holds `requirements.md`/`design.md`/`tasks.md`, as every Kiro feature does. Reviewing `.kiro/specs/payments/design.md` and later `.kiro/specs/orders/design.md` gives both the prefix `design-review`. The second review is numbered SR2, and its "Previous run" is the first plan's report. The plan also does not say what happens when the target is a folder (a Kiro or openspec feature is a folder, not one file). PLAN-04 only defines "a file path".
- **Evidence**:
  - `design.md:120`: "a report path `.specs/reviews/<basename>-review-<n>.md`"
  - `prep_review.py:96-98`: `nums = [... re.match(prefix + r"-(\d+)\.md$", f) ...]`, `prev = ... f"{prefix}-{n - 1}.md"`. The counter and the previous run depend only on the prefix
  - The spec-reviewer prompt tells the reviewer to reconcile every earlier Finding from "Previous run", so it would check plan B against plan A's Dispositions
  - `PLAN-04.S1` uses one uniquely named file (`docs/rfcs/042-billing.md`), so the collision is never exercised
- **Failure scenario**: The user reviews a teammate's `.kiro/specs/payments/design.md`, then `.kiro/specs/orders/design.md`. The second run is labelled SR2. The reviewer reports the payments Findings as "resolved" or "still open" against the orders plan, and the human records Dispositions in a history that mixes two plans.
- **Recommendation**: Derive the report name from the plan's repo-relative path (for example, slugify `.kiro/specs/payments/design.md` to `kiro-specs-payments-design`), or give each foreign plan its own folder under `.specs/reviews/`. Define folder targets (review every markdown file in the folder as one plan). Add a Scenario with two same-named foreign plans that checks each gets its own run 1.
- **Would change my mind**: a rule elsewhere in the plan that makes foreign report names unique per source path.
- **Disposition**: accept
- **Grill notes**: foreign-plan reports go to `.specs/reviews/<repo-relative path as a slug>/spec-review-<n>.md` (e.g. `.kiro/specs/payments/design.md` gives `kiro-specs-payments-design/`), so each plan has its own run counter and previous run; a folder target is one plan (every markdown file in it reviewed together, slug from the folder path); one new automated Scenario: two same-named foreign plans each get run 1. Rejected flat files with the slug in the name.

### SR2-F2 · The new `inspect` row has a different shape from the Verifier's existing per-Scenario table, and the plan does not say which row the validator reads
- **Dimension**: Verification · **Severity**: Major · **Confidence**: high
- **Where**: `design.md:117`, `design.md:179-184`; Spec `PROOF-01`, `PROOF-02`; Tasks T2, T3; `skills/spec-driven/references/validate.md:35-47`, `:236-246`
- **Problem**: `validate_scenarios.py` will accept an `inspect` Scenario when `validation.md` has "a row whose first cell is the Scenario ID and second cell is `PASS`". But the Verifier already writes a per-Scenario table into the same file, "for each Scenario in `spec.md`", with columns `Scenario | Spec-defined outcome | file:line | Result` and results written as `✅ PASS` / `❌ GAP`. After T3 the file holds two rows keyed by the same Scenario ID: one with the outcome text in cell 2, one with `PASS`/`FAIL` in cell 2. The plan does not say whether the validator takes the first matching row or any row, whether `✅ PASS` counts as `PASS`, or whether `❌ GAP` counts as a failure. T3 does not change the existing table, and no Scenario covers a duplicate ID or the template's emoji vocabulary.
- **Evidence**:
  - `validate.md:37`: "for each Scenario in `spec.md`, the Verifier re-derives the spec-defined expected outcome..."
  - `validate.md:242`: `| PAY-01.S1 | [precise value/state from spec] | ... | ✅ PASS |`, with the ID in cell 1 and the result in cell 4
  - `design.md:182-183`: `| Scenario | Result | Evidence | Reason |` / `| DEMO-01.S1 | PASS | ...`, with the result in cell 2
  - `PROOF-01.S1` to `.S3` each have exactly one row per ID, with no emoji
- **Failure scenario**: The Verifier follows the existing template and records `FLOW-05.S1` only in the Scenario-Anchored table as `✅ PASS`. `validate_scenarios.py` finds no row with `PASS` in cell 2 and fails the feature even though the inspection passed. The opposite also happens: an anchored row reads `❌ GAP` while a separate inspect row reads `PASS`, and the validator accepts the Scenario.
- **Recommendation**: Pick one table. Either the inspect result lives in the existing Scenario-Anchored table (the validator finds the table by its `Scenario` and `Result` headers and reads the `Result` cell, normalising `✅`/`❌`), or inspect rows sit in their own `## Inspect proofs` section, which the validator alone reads. Say in T3 that `validate.md`'s template changes to match. Add a Scenario where the same ID appears in both tables with conflicting results.
- **Would change my mind**: text in T3 or the design that removes `inspect` Scenarios from the Scenario-Anchored table, or that makes the validator read only a named section.
- **Disposition**: accept
- **Grill notes**: one table. No separate inspect table; every Scenario (test or inspect) has exactly one row in the Verifier's existing Scenario-Anchored table, and for an inspect Scenario the evidence column holds the `file:line` read plus one sentence of reason. `validate_scenarios.py` finds the table by its `Scenario` and `Result` headers and reads the `Result` cell, treating `✅ PASS` and `PASS` alike; `❌ GAP`, a missing row or a duplicate ID fails. New automated Scenarios: emoji PASS, GAP row, duplicate ID. Rejected a separate `## Inspect proofs` section.

### SR2-F3 · Fixture specs written inside test functions will register as extra Scenario claims and fail the scenarios gate
- **Dimension**: Verification · **Severity**: Minor · **Confidence**: high
- **Where**: Tasks T1, T2, T4-T10 (Gate `scenarios`, `tasks.md:38`); `skills/spec-driven/scripts/scenarios_lib.py:184-226` (`parse_test_file`), `:36-40` (`TEST_PATH_RE`)
- **Problem**: Nearly every `test` Scenario needs a fixture spec that contains `Scenario: DEMO-01.S1 ...` lines (PROOF-01, GRILL-05/06/09, PLAN-01/02, TKT-01/02, REV-01/02). `parse_test_file` runs `SCEN_LINE_RE.search` on every line from a test's `def` to the next one, including triple-quoted strings. So a fixture built inline in a test makes that test claim both its own Scenario and `DEMO-01.S1`. That gives two errors on every run, whatever `--only` says: "claims 2 Scenarios" and "DEMO-01.S1 is not defined in any spec". The plan's T1 helper does not say where fixture text lives.
- **Evidence**:
  - `scenarios_lib.py:217-220`: `m = SCEN_LINE_RE.search(body)` → `d["claims"].setdefault(current, [])` for any line in the test's span
  - `validate_scenarios.py:80-86`: the claims>1 and undefined-ID errors are raised for every test file, before `--only` filters anything
  - `TEST_PATH_RE` matches anything under `tests/` with a code extension, so a `.md` fixture file under `tests/` is not scanned
- **Failure scenario**: T2's tests build the PROOF-01.S1 fixture spec inline. The T2 gate `validate_scenarios.py ... --only PROOF-01.S1,...` exits 1 on the test's own fixture. The Verifier's final full run fails the same way.
- **Recommendation**: In T1, put fixture specs, tasks and validation files as `.md` files under `tests/fixtures/` (not scanned), or require the helper to assemble them from data outside any `def test_*` span. State this in the Test Coverage Matrix.
- **Would change my mind**: a T1 rule that already keeps fixture text out of test function bodies.
- **Disposition**: accept
- **Grill notes**: fixture specs, tasks and validation files live as `.md` files under `tests/fixtures/` (not scanned by the Scenario checker); the T1 helper copies them into each test's temporary repo; no test function contains sample Scenario text; the Test Coverage Matrix states the rule. Rejected changing the checker to ignore Scenario lines outside docstrings.

### SR2-F4 · A `retired` record status was added that the SR1-F11 answer did not choose, and nothing in the plan ever sets it
- **Dimension**: Thought Partnership · **Severity**: Minor · **Confidence**: high
- **Where**: `spec.md:92` (D-grill-in-spec-driven.8 row, Decided by `user`), `spec.md:149`, `READ-01.S1`; `grill-in-spec-driven.md:268`, `:272`; `design.md:150`, `:165`; `spec-review-1.md:179`
- **Problem**: The SR1-F11 grill notes say "summary.md Status is draft/active only". The record's D-8 now says "Status is `active` or `retired` (a whole record no longer applies; its Decisions were rewritten elsewhere)" and is marked Decided by `user`. The SR1-F11 Session path entry (`grill-in-spec-driven.md`, "Spec Review SR1 grill") never mentions `retired`. The reason given also conflicts with D-15: a changed Decision is rewritten in its original record, so a record's Decisions are never "rewritten elsewhere". No criterion, task or template says who sets `retired` or when, yet READ-01 makes consumers skip such records.
- **Evidence**:
  - `spec-review-1.md:179`: "no superseded status (summary.md Status is draft/active only)"
  - `grill-in-spec-driven.md:268`: "Status is `active` or `retired` ... its Decisions were rewritten elsewhere"
  - `grill-in-spec-driven.md:311-312` (D-15): "the Decision's text is rewritten in its original record"
  - `rg -n retired .specs/features/integrate-skills/` finds only readers (READ-01, the sweep, the data models), never a writer
- **Failure scenario**: An agent later marks a whole record `retired` to "clean up" after one Decision changes, and the read rule then hides its other, still-binding Decisions from every consumer.
- **Recommendation**: Ask the user. Either drop `retired` (statuses `draft`/`active`, as the grill notes say), or define who retires a record, when, and that every Decision in it must first be rewritten or explicitly dropped. Then record the answer in the Session path.
- **Would change my mind**: a Session path entry where the user chose a `retired` status.
- **Disposition**: accept
- **Grill notes**: drop `retired`. Record Status is `draft` or `active` only; a Decision that stops applying is rewritten to say so with a `Changed` line, and its record stays `active`. `retired` removed from the record (D-.8, D-.17, D-.47), spec, design and the read rule; the exchange is added to the Session path. Rejected keeping `retired` with a user-only rule.

### SR2-F5 · Plan kind depends on one self-declared line, and the two definitions of "legacy" disagree
- **Dimension**: Engineering Craft · **Severity**: Minor · **Confidence**: medium
- **Where**: `grill-in-spec-driven.md` D-grill-in-spec-driven.43; `design.md:118-120`; Spec `PLAN-01`, `PLAN-02`, `REV-02`; Tasks T5, T7, T8
- **Problem**: D-43 defines a legacy plan as "spec.md without that line, **or with a `context.md`**". The validators and `prep_review.py` (design.md:118-120, REV-02) look only at the `**Grilling Record**:` line, and REV-02 says a native feature's `context.md` is *not* listed. Take a feature that has the line and also a `context.md`, for example a legacy feature someone re-specified. D-43 calls it legacy and its `context.md` a decision source. The scripts call it native and drop `context.md` from the Review context. In the other direction, a new spec that leaves out the one line turns every new error (missing Decisions & Assumptions, orphan tasks, Ticket order) into a warning, though `summary.md` already records which features are native.
- **Evidence**:
  - D-43: "A **legacy** spec-driven plan (`.specs/features/<f>/spec.md` without that line, or with a `context.md`)"
  - `design.md:120`: "native features drop `context.md` ... legacy features list `context.md`"
  - `spec.md:599`: "for a native feature it SHALL NOT list `context.md`"
- **Failure scenario**: The user adds a Grilling Record line to a work-repo legacy feature whose `context.md` locks "tolerance is 1e-6". `/spec-review` no longer gives the reviewer that file, and the reviewer cannot flag a plan that breaks the lock.
- **Recommendation**: Use one definition everywhere. Simplest: list `context.md` whenever it exists, whatever the plan kind. Optionally treat a feature named in a `summary.md` Specs cell as native even without the line, so a dropped line cannot silently turn errors into warnings.
- **Would change my mind**: the user confirming that D-43's "or with a `context.md`" clause is obsolete.
- **Disposition**: accept
- **Grill notes**: one definition. Plan kind depends only on the `**Grilling Record**:` line; the "or with a `context.md`" clause is removed from D-.43. `context.md` is read and listed whenever it exists, whatever the plan kind (read rule, `prep_review.py`, REV-02), with one new automated Scenario. The user declined the optional second signal (a feature named in a `summary.md` Specs cell counting as native); a forgotten line still downgrades errors to warnings, accepted.

### SR2-F6 · `wizard` still writes and commits scripts outside spec-driven, against the Goal of zero side doors
- **Dimension**: Truthful Reporting · **Severity**: Minor · **Confidence**: medium
- **Where**: `spec.md:61` (Goal); `skills/wizard/SKILL.md:12`, `:35`, `:44`; no Task touches `skills/wizard/`
- **Problem**: The Goal states "0 installed skills offer an implementation path outside spec-driven". `wizard` writes a bash script into the repo (`scripts/` path), and for a repeatable setup it tells the agent to commit it and link it from the README. That code reaches the repository with no Spec, review or Verifier. Neither the grill nor the tasks mention `wizard`.
- **Evidence**:
  - `wizard/SKILL.md:12`: "saved to a scratch or `scripts/` path ... Commit it only when the user wants a repeatable setup path"
  - `wizard/SKILL.md:44`: "If it's a repeatable setup path, commit it and link it from the README"
  - `rg -n wizard .specs/features/integrate-skills/ .specs/decisions/` finds nothing
- **Failure scenario**: After this change ships, the Goal checkbox is ticked while an installed skill still commits code to the repository with no Spec, review or Verifier.
- **Recommendation**: Either narrow the Goal to "feature and bug-fix code", naming `wizard` as an accepted exception for operator scripts, or route a committed wizard through a Small Specify, as `diagnosing-bugs` does.
- **Would change my mind**: the user stating that operator wizards are outside "implementation".
- **Disposition**: accept
- **Grill notes**: the user had never used `wizard` (vendored from mattpocock/skills in 5544263; nothing depends on it once `ask-matt` and `engineering-README.md` are deleted) and chose to retire it: it joins the retired skills (folder deleted, `install.sh` removes installed copies, README updated), eight in total; the Goal stays "0 installed skills" with no exception. Rejected a named exception and routing committed wizards through a Small Specify.

### SR2-F7 · `install.sh` will `rm -rf` any skill named `implement`, `triage` or `to-spec` in the shared skills directory, not only this repo's copies
- **Dimension**: Production Risk · **Severity**: Minor · **Confidence**: medium
- **Where**: Spec `FLOW-01`, Scenario `FLOW-01.S1`; Task T11; `install.sh:9`, `:24-28`
- **Problem**: The removal loop deletes `$CLAUDE_DIR/skills/<name>` by name alone. The old list held one repo-specific name (`tlc-spec-driven`). The new one adds generic names (`implement`, `triage`, `to-spec`, `wayfinder`) in a directory other sources also install into. On this machine `~/.claude/skills` already holds third-party entries (`omarchy` and `diagnose-crash` symlinks, `synced/`), and at work opencode reads the same directory. A skill named `implement` from another source would be deleted with no prompt. FLOW-01.S1 only checks that the seven names are gone, never that an unrelated skill survives.
- **Evidence**:
  - `install.sh:24-28`: `if [ -d "$CLAUDE_DIR/skills/$name" ]; then rm -rf "$CLAUDE_DIR/skills/$name"`
  - `ls -la ~/.claude/skills`: `omarchy -> /usr/share/omarchy/...`, `diagnose-crash -> ...`, `synced/` are not from this repo
- **Failure scenario**: A work machine has a team-provided `triage` skill. Running this repo's `install.sh` removes it and prints "removed retired skill triage".
- **Recommendation**: Remove a retired directory only when its `SKILL.md` shows it came from this repo (for example, its frontmatter `name` matches and a known phrase from the vendored text is present), otherwise warn and skip. Add a Scenario: a foreign `skills/triage/` survives the install.
- **Would change my mind**: confirmation that nothing but this repo's installer ever writes to `~/.claude/skills` on any machine the user installs to.
- **Disposition**: accept
- **Grill notes**: the retirement loop deletes a folder only when its installed `SKILL.md` contains a known phrase from the version this repo shipped (one phrase per retired skill, held in `install.sh`) and the folder is not a symlink; otherwise it warns ("skipped <name>: not installed by this repo") and leaves it. One new automated Scenario: a different skill named `triage` survives the install. Rejected an interactive confirmation and leaving the loop name-only.
