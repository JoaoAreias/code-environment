# Change Review CR1 · integrate-skills

- **Reviewed**: `8a965132060a...8b8776e23776` (36 commits, 132 files)
- **Inputs read**: spec.md (Decisions & Assumptions, Requirement Traceability), design.md (`prep_review.py` and installer sections, Error Handling, Tech Decisions), tasks.md, validation.md, spec-review-1.md, spec-review-2.md, `.specs/decisions/summary.md`, `.specs/decisions/grill-in-spec-driven.md` (header; D-.17, D-.18, D-.33, D-.34, D-.35, D-.42, D-.43, D-.44), legacy `docs/adr/0001-0003` (listed, not re-read: nothing in the script diff touches their subjects); full diffs of `install.sh`, `prep_review.py`, `scenarios_lib.py`, `validate_scenarios.py`, `validate_spec.py`, `validate_tasks.py`, `tests/*.py`; spot reads of `implement.md`, `tickets.md`, `validate.md`, `agents/change-reviewer.md`, `skills/grilling/SKILL.md`
- **Evidence**: graph refreshed 2026-11-16 16:54 · Sonar: analysis 2026-11-16 19:46 UTC of `code-environment` (current: it is later than the head commit at 19:12 UTC, and flagged lines match HEAD, e.g. `validate_tasks.py:144,147`; the server has no branch or PR analysis, so the scan is labelled `main`); quality gate OK, 0 security hotspots, duplication 0.5 %, no coverage report imported · Scenario check: the context's run reported 50 errors, but it used the installed skill at `~/.claude/skills/spec-driven`, which predates this Change and does not know `**Proof**: inspect`. Re-run with the repo's own script, `python3 skills/spec-driven/scripts/validate_scenarios.py integrate-skills --root . --since 8a965132060a`: 81 Scenarios, 81 proven, 0 errors.
- **Reviewer Lessons applied**: none

## Dimensions

| Dimension | Status | Findings |
| --- | --- | --- |
| Functional Correctness | assessed | 1 |
| Practical Judgment | assessed | 0 |
| Thought Partnership | assessed | 1 |
| Verification | assessed | 1 |
| Engineering Craft | assessed | 1 |
| Truthful Reporting | assessed | 0 |
| Communication | assessed | 0 |
| Production Risk | assessed | 1 |

Notes on the dimensions with no Findings:

- **Practical Judgment**: since the Spec Review commit (`abd3b89`), the plan changed only in tasks.md ticks, the `fa0c455` repair (it removed a duplicated block and ticked T11), and the traceability statuses in spec.md. No behaviour was added outside the Tasks' `Where` files. `rg` finds no references to the retired skills left in `skills/`, `agents/`, `README.md`, `CONTEXT.md` or `render-adapters.js`.
- **Truthful Reporting**: the claims hold up.
  - All 31 Tasks are ticked (74 `[x]`, 0 `[ ]`).
  - `git rev-list --count abd3b89..e6cb82f` = 33, matching validation.md.
  - Traceability rows read `Verified`, matching validation.md.
  - Spot-checked citations: `tests/test_install.py:60-62` (FLOW-01.S1), `implement.md:368-370` (FLOW-05.S1) and `tickets.md:105-108` (TKT-07) say what validation.md claims.
  - Every SR1 and SR2 Finding accepted at review is visible in the code. SR2-F1: a folder per foreign plan. SR2-F2: one table, read by header. SR2-F3: `.md` fixtures. SR2-F4: no `retired` status remains (`rg -i '\bretired\b'` finds only retired *skills*). SR2-F5: `context.md` is listed whenever it exists, at `prep_review.py:291-292`. SR2-F6: `wizard` is retired. SR2-F7: phrase plus symlink check.
  - Rejected SR1-F9 was not built: `fixtures.build_repo` requires the real graphify.
  - `Searched:` lines are present for the new symbols. There are no `Removed test:` claims, and none are needed: the base had no `tests/`.
- **Communication**: commit bodies give reasons. The validation.md "Minor observations" list states the remaining doubts openly.
- **Legacy Paths**: `graph_queries.py test-only --since 8a965132060a` reports none. The old Assumptions parser was replaced, not kept alongside the new one.
- **Sonar**:
  - Two new `python:S8786` (regex backtracking) issues: `validate_tasks.py:144` and `:147` (issue keys `8559cb98…`, `d671a825…`). They run on one stripped markdown line at a time, so the cost is negligible. They are relayed here and not raised as Findings.
  - The other 23 open issues are on lines this Change did not add.

## Previous run

First run.

## Findings

### CR1-F1 · `/spec-review .specs/features/<f>/...` stops with "no feature" although `foreign_plan` says such a path names the feature
- **Dimension**: Functional Correctness · **Severity**: Minor · **Confidence**: high
- **Where**: `skills/spec-driven/scripts/prep_review.py:238`, `:250-251`, `:327-329`, `:209-210`; Spec `PLAN-04`
- **Problem**: `foreign_plan` says it returns None when the target names a feature "by name or by a path inside its folder". For the path case it does return None at `:250-251`. But `prep_spec` then passes the raw target string to `pick_feature` (`:329`), and `pick_feature` only accepts a bare feature name (`:209`). So a path into a feature folder is recognised as "not foreign" and then rejected.
- **Evidence**:
  - `:238`: "Returns None when `target` is empty or names a feature (by name or by a path inside its folder)."
  - `:250`: `if parts[:2] == [".specs", "features"] and len(parts) > 2: return None`
  - `:329`: `feature_target(root, pick_feature(root, args.feature))`, called with the unconverted target
  - `:209-210`: `if feature not in feats: raise Stop(f"no feature `{feature}` under .specs/features/ ...")`
  - No test covers a path into `.specs/features/`. PLAN-04.S1 to S3 use only foreign paths.
- **Failure scenario**: The user runs `/spec-review .specs/features/demo/spec.md`, a natural thing to try now that `/spec-review` accepts paths. prep prints `STOP: no feature `.specs/features/demo/spec.md` under .specs/features/ (have: demo)`. Nothing is written and nothing is lost, but the message contradicts itself and the user must guess that only the bare name works.
- **Recommendation**: In `foreign_plan`, return the feature name (`parts[2]`) for a path inside `.specs/features/`, and have `prep_spec` pass that name to `pick_feature`. Alternatively, stop with a message that says to pass the bare feature name. Either way, fix the docstring to match.
- **Would change my mind**: a caller (the `/spec-review` command or review.md) that turns a feature-folder path into the bare name before it calls `prep_review.py`.
- **Disposition**: accept

### CR1-F2 · The foreign-plan slug is lossy, so two different plans can share one report folder and run history
- **Dimension**: Thought Partnership · **Severity**: Minor · **Confidence**: high
- **Where**: `skills/spec-driven/scripts/prep_review.py:311-318`; Decision `D-grill-in-spec-driven.43` (Decided by: user); design.md:120 (slug rule, agent-decided); Scenario `PLAN-04.S2`
- **Problem**: D-.43, which the user decided as the answer to SR2-F1, says each foreign plan gets "its own run numbers and previous run". The slug the agent picked does two lossy things:
  - It drops the file extension.
  - It turns every run of non-alphanumeric characters into one `-`.
  So distinct paths map to the same folder. `next_run` then numbers the second plan's review SR2 and hands it the first plan's report as "Previous run". This is the failure SR2-F1 described, in a narrower set of cases. PLAN-04.S2 tests only `payments/design.md` against `orders/design.md`, which differ in letters.
- **Evidence**:
  - `:311`: a folder target keeps its whole path as the stem (`stem = rel`).
  - `:313`: a file drops its extension (`os.path.splitext(rel)[0]`).
  - `:318`: `slug = re.sub(r"[^A-Za-z0-9]+", "-", stem).strip("-")`
  - Colliding pairs:
    - `.kiro/specs/payments/` (folder) and `.kiro/specs/payments.md` both give `kiro-specs-payments`.
    - `docs/rfcs/042_billing.md` and `docs/rfcs/042-billing.md` both give `docs-rfcs-042-billing`.
    - `docs/a-b.md` and `docs/a/b.md` both give `docs-a-b`.
- **Failure scenario**: A repo holds both `docs/rfcs/042-billing.md` and an older `docs/rfcs/042_billing.md`. The user reviews the first and later the second. The second review is labelled SR2, and the reviewer reconciles Findings about one RFC against the other.
- **Recommendation**: Ask the user whether this edge case matters. If it does, make the slug injective. One way is to append a short hash of the repo-relative path. Another is to have `foreign_target` check for a collision and stop when the existing folder's reports name a different `Plan:` path. Then add a Scenario with two paths that differ only in punctuation.
- **Would change my mind**: the user saying that such near-identical plan paths do not occur in the repos they work in.
- **Disposition**: accept

### CR1-F3 · FLOW-01.S1's "shipped copies" are stubs written from `install.sh`'s phrases, so the test cannot catch a phrase that no longer matches what was shipped
- **Dimension**: Verification · **Severity**: Minor · **Confidence**: high
- **Where**: `tests/test_install.py:49-62`; `tests/fixtures/installed-retired/skills/*/SKILL.md`; `install.sh:16-24`; Scenario `FLOW-01.S1`
- **Problem**: The Scenario's Given is "this repository's shipped copies" of the eight skills. The fixtures are six-line stubs, for example "A small copy of the triage skill this repository shipped", each holding exactly the phrase `install.sh` searches for. The test therefore proves that `install.sh` matches its own fixtures. It does not prove that it matches the `SKILL.md` files real users have installed, which is what decides whether retirement works on a real machine. If someone mistypes a phrase and updates the stub to match, the test still passes, and every real installed copy is then skipped with "not installed by this repo".
- **Evidence**:
  - `tests/fixtures/installed-retired/skills/triage/SKILL.md`: a 6-line stub, not the shipped file.
  - Checked by hand, so the code is correct today: all 8 phrases are present in `git show 8a965132060a:skills/<name>/SKILL.md` and in every earlier version from `git log`. They are also present in the installed copies under `~/.claude/skills/` (`base=1 installed=1` for each).
  - The real retired files are now only in git history, so a test could read them from there.
- **Failure scenario**: A later edit to `RETIRED_SKILLS` changes a phrase and its stub together. CI stays green, and users' installed copies of that retired skill are no longer removed and keep offering the old route.
- **Recommendation**: Build the FLOW-01.S1 fixture from the real shipped files. Either copy the full `SKILL.md` texts from `8a965132060a` into `tests/fixtures/installed-retired/`, or have the test read them with `git show 8a965132060a:skills/<name>/SKILL.md`.
- **Would change my mind**: the stubs being byte-for-byte excerpts of the shipped files, with a check that ties them to those files.
- **Disposition**: reject: T30 deleted the shipped SKILL.md files, so the phrases can no longer drift from them; they only need to match copies already installed, and all eight were checked by hand in this review.

### CR1-F4 · `install.sh` overwrites any existing `skills/grilling` (or `setup-spec-driven`) by name, the same shared-folder risk SR2-F7 fixed for removal
- **Dimension**: Production Risk · **Severity**: Minor · **Confidence**: medium
- **Where**: `install.sh:53-62`; Decision `D-grill-in-spec-driven.35`; SR2-F7
- **Problem**: The copy loop runs `rm -rf "$CLAUDE_DIR/skills/$name"` and then `cp -r` for every skill this repo ships, with no provenance check. The loop itself is older than this Change. What is new is that the Change starts shipping `grilling`, a generic and widely used skill name. D-.35's own reason ("the skills folder is shared with other sources, and names such as `implement` and `triage` are generic") applies equally to installing as to retiring. A team-provided or hand-written `grilling` skill in `~/.claude/skills/`, which opencode at work also reads, would be deleted and replaced without a message. A symlinked one would have its link replaced.
- **Evidence**:
  - `install.sh:58-60`: `rm -rf "$CLAUDE_DIR/skills/$name"` then `cp -r "$dir" "$CLAUDE_DIR/skills/$name"`, with no check of what was there.
  - `install.sh:44`: the retirement loop checks provenance (not a symlink, phrase present). The install loop does not.
  - `ls ~/.claude/skills` shows that this folder already mixes sources (`omarchy`, `diagnose-crash`, `synced/`). The user's claude.ai account also syncs a skill named `grilling` (it appears as `anthropic-skills:grilling` in this session).
- **Failure scenario**: On a work machine a teammate's `~/.claude/skills/grilling` with team-specific rules exists. Running `install.sh` replaces it with this repo's copy and prints only `  grilling`. The team rules are gone, and nothing says so.
- **Recommendation**: Before overwriting, check that an existing `$CLAUDE_DIR/skills/$name` is a real folder whose `SKILL.md` came from this repo (for example, `name:` matches and a repo marker line is present). Otherwise print `skipped <name>: installed by another source` and leave it. Or at least warn when the folder being replaced does not match. Add a Scenario: a foreign `skills/grilling/` survives the install.
- **Would change my mind**: the user confirming that nothing but this repo ever installs a skill named `grilling` or `setup-spec-driven` on their machines.
- **Disposition**: reject: the overwrite-by-name behaviour predates this Change and applies to every skill install.sh copies; fixing it needs an install marker for all skills, which belongs in a separate feature.

### CR1-F5 · `validate_spec.py` now parses tables two ways: Decisions by header name, Requirement Traceability by position
- **Dimension**: Engineering Craft · **Severity**: Minor · **Confidence**: high
- **Where**: `skills/spec-driven/scripts/scenarios_lib.py:207-237` (`_cells`, `find_tables`); `skills/spec-driven/scripts/validate_spec.py:111-118` (`split_row`, `is_separator`), `:245-271`
- **Problem**: This is a possible local Duplicated Code smell (a judgment call). The Change added `find_tables`, a header-name table reader, so that table checks no longer depend on column position (SR1-F8, D-.34). `validate_spec.py` uses it for Decisions & Assumptions. The Requirement Traceability check in the same file still uses the older `split_row`/`is_separator` pair, with "drop the first row" and `cells[0]` logic. `_cells` repeats `split_row` exactly, and `find_tables` re-implements `is_separator` in its separator regex. The `526f030` commit records this choice ("validate_spec.split_row is local to that script"). The result is still two parsers in one file, and two rules for which column holds an ID.
- **Evidence**:
  - `scenarios_lib.py:207-208`: `return [c.strip() for c in line.strip().strip("|").split("|")]`
  - `validate_spec.py:111-113`: `cells = line.strip().strip("|").split("|"); return [c.strip() for c in cells]`
  - `validate_spec.py:249-256`: positional `data[1:]`, `cells[0]` for Traceability, while `:222` uses `find_tables` for Decisions.
- **Failure scenario**: A spec whose Traceability table gains a leading column (for example `| # | Requirement ID | ...`) passes Decisions validation but fails Traceability with "malformed requirement ID: '1'". This is the position dependence SR1-F8 asked to remove.
- **Recommendation**: Move the Traceability check onto `find_tables(section, "Requirement ID")`, then delete `split_row` and `is_separator`.
- **Would change my mind**: a Repo Standard or Decision that fixes the Traceability table's column order and keeps position-based parsing there on purpose.
- **Disposition**: accept
