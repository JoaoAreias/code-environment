# grill-in-spec-driven · Grill inside spec-driven; Grilling Records replace ADRs

- **Date**: 2026-10-11 to 2026-11-14
- **Started from**: `/grill-with-docs` in Claude Code, main session, branch `feat/integrate-skills`
- **Specs**: `integrate-skills`
- **Binds**: project
- **Areas**: `skills/`, `agents/`, `install.sh`, `render-adapters.js`, `README.md`, `CONTEXT.md`, `.specs/`
- **Status**: active
- **Note**: written by hand to the rules this session decided, before any skill implements them. It is also the first test of the Grilling Record template. Spec Reviews SR1 and SR2 (2026-11-14) changed several Decisions; they were rewritten in place (D-grill-in-spec-driven.15) and carry a `Changed` line. The file was first named `0001-integrate-grill-into-spec-driven.md` with IDs `D-0001.k`.

## Context

The user plans features with two skills that overlap: `/grill-with-docs`, which they prefer for getting requirements because it is far more thorough, and `spec-driven`, which owns the spec, the gates and the reviewers. They asked to merge the specification phase of both into one.

What the code showed at the start:

- `skills/grill-with-docs/SKILL.md:7` only calls two skills, `grilling` and `domain-modeling`. Its output is `CONTEXT.md` plus ADRs in `docs/adr/`; it writes no spec.
- spec-driven Specify (`skills/spec-driven/references/specify.md`) searches the codebase with graphify, discovers Repo Standards, asks questions, runs an implicit-requirement sweep, writes EARS criteria with Gherkin Scenarios, and gates the result with `validate_spec.py`. Its Discuss sub-step (`references/discuss.md:47-51`) offers three paces (Quick, Guided at up to two questions per turn, Detailed) and writes a per-feature `context.md`.
- Two decision logs with the same three-criteria rule: `docs/adr/` (domain-modeling, `skills/domain-modeling/ADR-FORMAT.md`) and `.specs/STATE.md ## Decisions` with `AD-NNN` entries (`skills/spec-driven/references/memory.md:11-18`). `~/Projects/interest-rate-project` has both at once: 8 `AD-NNN` entries and 7 ADR files.
- A name clash: per-feature `context.md` (gray-area decisions) next to the root `CONTEXT.md` (glossary).
- `grilling` is not in this repo. It exists only as a claude.ai-synced skill under `~/.claude/skills/synced/`, so opencode at work does not have it, although `grill-with-docs`, `triage`, `improve-codebase-architecture` and `wayfinder` (`skills/wayfinder/SKILL.md:79,111`) call it by name.
- `ADR-FORMAT.md:15` says "That's it. An ADR can be a single paragraph", and `:19` says most ADRs need none of the optional sections. Models follow this and write tiny files.
- `skills/ask-matt/SKILL.md` routed feature work through `/grill-with-docs` → `/to-spec` → `/to-tickets` → `/implement`, never mentioned spec-driven, and described `/code-review` as the old two-axis review. `skills/implement/SKILL.md:13` ends with "use /code-review", although `/code-review` is now the human-triggered Change Review.
- `skills/to-tickets/SKILL.md:33` sizes tickets to "a single fresh context window", and `:4` blocks model invocation.
- spec-driven's auto-sizing (`skills/spec-driven/SKILL.md:51-52`) skipped Tasks for Small and Medium, and Design for Medium.

Forces and constraints:

- The user works alone with an agent on small local projects and in teams on much larger work repos (opencode at work, Claude Code at home, omp too). Everything must work in all three harnesses.
- The user often approves planning artifacts only to see the whole picture; only an explicit Execution Approval authorizes building.
- Vendored skills are starting points the user adapts freely.
- Outside sources consulted: none beyond this repo, `~/Projects/interest-rate-project/.specs/STATE.md` and its `docs/adr/` listing.

## Session path

Each question was asked alone, with a recommendation, and answered before the next.

### Q1 · Where does the merged specification phase live?
- **Options**: (a) spec-driven Specify becomes the grill (grilling plus domain-modeling, then writes `spec.md`; Discuss folds in; `/grill-with-docs` stays for non-feature grilling). (b) Same, and retire `/grill-with-docs`. (c) `/grill-with-docs` is the front door and hands off to spec-driven, whose Specify shrinks to synthesis.
- **Recommended**: (a). spec-driven owns the artifact, gates and reviewer contract; (c) splits one phase across two skills.
- **Answer**: (a). → D-grill-in-spec-driven.1

### Q2 · Question pace inside Specify?
- **Options**: (a) always one question per turn with a recommendation, no pace menu, with "you decide" and "decide the rest" escapes. (b) Keep the pace menu, default Detailed. (c) Grill only Large/Complex; Quick for the rest.
- **Recommended**: (a). The pace menu is what dilutes the grill; the escapes make trivial branches cost one word.
- **Answer**: (a). → D-grill-in-spec-driven.2

### Q3 · What happens to Discuss and the per-feature `context.md`?
- **Options**: (a) drop `context.md`; behavior answers become criteria and Scenarios, other answers become rows of a "Decisions & Assumptions" table with a Decided-by column; Deferred Ideas become Out of Scope rows; Specific References become an optional section. (b) Keep a separate file under another name. (c) Keep `context.md`.
- **Recommended**: (a). One file for Design and the reviewer, and the clash with `CONTEXT.md` disappears.
- **Answer**: (a). → D-grill-in-spec-driven.3

### Q4 · Which decision log survives?
- **Options**: (a) `docs/adr/` only. (b) `STATE.md AD-NNN` only. (c) Both, split by topic.
- **Recommended**: (a).
- **Answer**: none of them as offered. The user rejected the ADR name itself: they mostly work alone with an agent, so a record nobody else discussed or agreed is not an "architecture decision record", and the name misleads. Existing records should move, and other skills should read the specs instead of `docs/adr/`. → D-grill-in-spec-driven.4

### Q5 · What is the record called and where does it live? (first round)
- **Options**: (a) "Decision" with `D-NNN` in one `.specs/DECISIONS.md`. (b) One file per Decision under `.specs/decisions/`. (c) Keep `STATE.md ## Decisions` with `AD-NNN`.
- **Recommended**: (a).
- **Answer**: all rejected. The user added that work repos are far larger than local ones, so a single growing file does not scale.

### Q5 · Where do Decisions live? (second round)
- **Options**: (a) inside the feature Spec's table with an ID and a Binds column, found through an aggregator script. (b) Area-scoped files under `.specs/decisions/<area>.md`. (c) Something else.
- **Recommended**: (a), with a known gap for decisions made outside any feature.
- **Answer**: (a), "much better". Refined by Q6 and Q7.

### Q6 · Where does a Decision live when no feature made it?
- **Options**: (a) a Decision-only Spec. (b) One `.specs/PROJECT.md`. (c) No Decision without a feature.
- **Recommended**: (a).
- **Answer**: none of them. `.specs/decisions/` holding ADR-shaped files, plus `.specs/decisions/summary.md`, never called ADRs. → D-grill-in-spec-driven.5

### Q7 · Which Decisions get a file, and what does `summary.md` index?
- **Options**: (a) featureless ones only, with `summary.md` also listing project rows from specs. (b) Every project-binding Decision gets a file whatever its origin; `summary.md` indexes the folder; no aggregator. (c) Featureless only, plus the aggregator.
- **Recommended**: (b). One way to find what binds the project.
- **Answer**: (b), plus: the files must be complete and describe the whole grilling session, not one decision; models keep writing tiny files here. → D-grill-in-spec-driven.5

### Q8 · What is the unit of one file?
- **Options**: (a) one file per grilling session, every Decision inside with its own ID, required sections Context, Session path, Decisions, Consequences, Related, and a validator gate. (b) One file per Decision with the same sections.
- **Recommended**: (a). Grill decisions form one chain; splitting them is how files end up tiny.
- **Answer**: (a), but no validation gate: fix it in the prompt. → D-grill-in-spec-driven.6

### Q9 · Does every feature grill write a session file?
- **Options**: (a) only when it produces a project-binding Decision. (b) Always; `spec.md` rows link to it. (c) Always, but in the feature folder.
- **Recommended**: (a), to keep the shared folder small.
- **Answer**: (b). Agent default stated with the next question and not objected to: one ID per Decision, `D-NNNN.k`, used in both the record and `spec.md`. → D-grill-in-spec-driven.7

### Q10 · What does `summary.md` list?
- **Options**: (a) every Decision. (b) Project-binding Decisions only. (c) One line per session file.
- **Recommended**: (b).
- **Answer**: a table of all decision files: the file name, a one-to-two-sentence description of the file, whether it is active, and the related specs; open to more columns. Read by the agent as one row per file, with Status values `active`, `partly superseded: D-x by D-y`, `superseded by NNNN`. → D-grill-in-spec-driven.8

### Q11 · Which extra columns?
- **Options**: Binds; Areas; Date (skip); Decided by (skip, belongs per Decision inside the file).
- **Recommended**: add Binds and Areas.
- **Answer**: Binds and Areas. → D-grill-in-spec-driven.8

### Q12 · What is the session file called?
- **Options**: (a) Grilling Record. (b) Session Record. (c) Decision Log entry.
- **Recommended**: (a). Names exactly what it is and implies no team agreement.
- **Answer**: (a). → D-grill-in-spec-driven.9

### Q13 · What makes a Decision bind the project?
- **Options**: (a) one test: a future feature has to follow it or knowingly supersede it; drop the three-criteria test; the agent proposes Binds inside each recommendation. (b) That test and all three old criteria. (c) The user tags every Decision.
- **Recommended**: (a).
- **Answer**: (a). → D-grill-in-spec-driven.10

### Q14 · When does Specify write to disk?
- **Options**: (a) Grilling Record written incrementally, one answer at a time; `spec.md` only after shared understanding. (b) Everything at the end. (c) Everything incremental, including a growing spec draft.
- **Recommended**: (a). This very session had already been compacted once.
- **Answer**: (a). → D-grill-in-spec-driven.11

### Q15 · How are existing ADRs and `AD-NNN` entries migrated?
- **Options**: (a) a human-triggered migration procedure run by the agent. (b) A mechanical script. (c) Migrate the two local repos by hand.
- **Recommended**: (a).
- **Answer**: none. Leave old records where they are; `summary.md` gets a line pointing at `docs/adr/` as a legacy decision path that should be checked. Agent extension stated and not objected to: the same for `STATE.md ## Decisions`. This reverses the "migrate" part of Q4. → D-grill-in-spec-driven.12

### Q16 · Where does the glossary live?
- **Options**: (a) where domain-modeling puts it today. (b) Under `.specs/`.
- **Recommended**: (a).
- **Answer**: (a). → D-grill-in-spec-driven.13

### Q17 · Where do the grilling rules come from, given opencode at work?
- **Options**: (a) vendor `skills/grilling/` as the one source; domain-modeling owns the glossary and record formats; Specify calls both by name and adds only spec-specific steps. (b) Inline everything into `specify.md` and vendor `grilling` anyway. (c) Inline only, no vendoring.
- **Recommended**: (a), with a fallback to the sibling skill directories for harnesses that cannot load skills by name.
- **Answer**: (a). → D-grill-in-spec-driven.14

### Q18 · When a review Finding changes a Decision, where is that recorded?
- **Options**: (a) an `## Amendments` section in the feature's existing Grilling Record. (b) A new record per review round. (c) Only edit `spec.md`.
- **Recommended**: (a). (b) would make one-line records for plain accepts.
- **Answer**: (a). → D-grill-in-spec-driven.15

### Q19 · Where do Design-phase Decisions go?
- **Options**: (a) a `## Design` section in the feature's Grilling Record, Design questions asked grill-style, `design.md` Tech Decisions become links. (b) Keep Design's own table, only project ones go to the record. (c) A separate record for Design.
- **Recommended**: (a).
- **Answer**: (a). → D-grill-in-spec-driven.16

### Q20 · How do consumers read Decisions?
- **Options**: (a) read `summary.md`, open rows that are active or partly superseded and either bind the project with overlapping Areas (or `*`) or name the current feature; always check legacy paths; active project Decisions count as Repo Standards. (b) Open every active project row. (c) Read `summary.md` and use judgment.
- **Recommended**: (a).
- **Answer**: (a), plus: list the repo to find relevant files from collaborators who use different flows. → D-grill-in-spec-driven.17

### Q21 · How does that repo scan work? (first round)
- **Options**: (a) one discovery step merged with Repo Standards discovery, using `git ls-files` filtered by path names, run at every Specify, stored in `summary.md`. (b) Every consumer scans every time. (c) Scan once.
- **Recommended**: (a).
- **Answer**: all rejected. `git ls-files` misses gitignored files that may matter; a full listing walks `node_modules` and virtualenvs.

### Q21 · Walk method (second round)
- **Options**: (a) a stdlib Python script with rule-based pruning and name matching. (b) `fd --no-ignore-vcs` with excludes.
- **Recommended**: (a).
- **Answer**: (b), with an instruction to pause and ask the user to install `fd` when it is missing.

### Q21b · What does the listing show?
- **Context**: the agent's first draft of the fd command matched paths against names like `adr`, `decision` and `spec`. The user rejected it: too complicated and tied to this repo's own conventions, which defeats the purpose of finding other people's flows.
- **Options**: (a) directories to depth 3 plus root files. (b) Everything to depth 2.
- **Recommended**: (a).
- **Answer**: (a). → D-grill-in-spec-driven.18

### Q22 · When does discovery run, and is the result stored?
- **Options**: (a) every consumer runs it; no stored list; Specify and Design cite the outside sources they used in the Grilling Record. (b) Every consumer runs it and Specify also stores the hits. (c) Only spec-driven runs it.
- **Recommended**: (a).
- **Answer**: (a). → D-grill-in-spec-driven.19

### Q23 · What do the reviewers check against Grilling Records?
- **Options**: (a) all proposed checks: agent-decided high-impact Decisions, unasked branches, dropped or contradicted answers, invented requirements, conflicts with active Decisions or outside sources, record completeness; change-reviewer flags contradictions of active Decisions and silent departures from user decisions. (b) Conflicts only. (c) All, completeness capped at Cosmetic.
- **Recommended**: (a).
- **Answer**: (a). → D-grill-in-spec-driven.20

### Q24 · What happens to the mattpocock main flow and its router?
- **Options**: (a) spec-driven becomes `ask-matt`'s main flow, ticket skills stay as an issue-tracker flow. (b) Retire `to-spec`, `to-tickets`, `implement`. (c) Leave them.
- **Recommended**: (a).
- **Answer**: kill `ask-matt` (never used). Keep the earlier separation between the model-triggered check (the Verifier) and the human-triggered `/code-review`. Implementation comes only through spec-driven, and spec-driven must create tickets the product team can reference, each about a day of work. → D-grill-in-spec-driven.21

### Q25 · Which skills retire?
- **Options**: (a) `ask-matt`, `implement`, `to-spec`, `to-tickets`, spec-driven absorbs tickets, the setup skill stays. (b) Keep `to-tickets` as a publisher spec-driven calls. (c) Retire only `ask-matt` and `implement`.
- **Recommended**: (a).
- **Answer**: (a), and also retire `triage` and `wayfinder`; rename `setup-matt-pocock-skills` and retire the "matt-pocock" naming, because the skills are only based on mattpocock/skills now. Agent assumptions stated and not objected to: delete `skills/engineering-README.md`; keep the README attribution as "based on" because the MIT license requires the notice. → D-grill-in-spec-driven.21

### Q26 · New name for the setup skill?
- **Options**: (a) `setup-spec-driven`. (b) `setup-repo`. (c) No setup skill.
- **Recommended**: (a).
- **Answer**: (a). → D-grill-in-spec-driven.22

### Q27 · How does a Ticket relate to a Task?
- **Options**: (a) a Ticket is a day-sized vertical slice made of Tasks, sliced top-down; Small and Medium skip `tasks.md`, so the Spec is one Ticket. (b) Tasks first, grouped into Tickets afterwards. (c) Ticket equals Task.
- **Recommended**: (a).
- **Answer**: (a), but Tasks are never skipped at any scope: the user reviews the work through `tasks.md`. → D-grill-in-spec-driven.23, D-grill-in-spec-driven.24

### Q28 · When are Tickets published to the tracker?
- **Options**: (a) on an explicit "publish tickets" after the latest Spec Review's Dispositions, independent of Execution Approval, with tracker IDs written back and later drift listed. (b) Together with Execution Approval. (c) Right after Tasks, before review.
- **Recommended**: (a).
- **Answer**: (a). → D-grill-in-spec-driven.25

### Q29 · What happens to `tdd`?
- **Options**: (a) `tdd` becomes Execute's per-Task loop; its seam confirmation is satisfied by Scenarios and Design; bug fixes also go through spec-driven. (b) Keep it standalone. (c) Retire it.
- **Recommended**: (a). It closes the last side door around "implementation comes through spec-driven".
- **Answer**: (a). Consequences stated by the agent and not objected to: `diagnosing-bugs` Phase 5 hands its repro, root cause and seam to a Small Specify instead of fixing; `improve-codebase-architecture` treats active Decisions as it treated ADRs and records rejections in its Grilling Record. → D-grill-in-spec-driven.26

### Q30 · Does this change go through spec-driven itself?
- **Options**: (a) dogfood: write this record, `summary.md`, a spec and day-sized tasks by hand to the new rules, then the human runs `/spec-review`. (b) Record and summary only. (c) No dogfooding.
- **Recommended**: (a).
- **Answer**: (a). → D-grill-in-spec-driven.27

### Shared-understanding check
- The agent listed ten defaults for branches never asked. The user corrected one: Design is also required for Medium scope. The other nine stood without objection. → D-grill-in-spec-driven.28, D-grill-in-spec-driven.29 to D-grill-in-spec-driven.37
- The user then confirmed shared understanding: "yes, write them".

### Spec Review SR1 grill (2026-11-14)
The user ran `/spec-review integrate-skills` (report `.specs/features/integrate-skills/spec-review-1.md`, 11 Findings) and asked to be grilled on each one. Each Finding was restated with its evidence re-checked, then one question at a time.

- **SR1-F1** (30 agent-behavior Scenarios have no proof the gates accept). Agent first recommended a manual UAT walkthrough recorded in `validation.md`; the user asked what UAT meant and for a clearer statement. The user then proposed a marker for changes a unit test cannot prove (markdown, IaC) so an independent subagent checks them later. Question: who checks, (a) the existing Verifier or (b) a new `inspector` agent. Recommended (a). **Answer**: (a). Follow-up: move Scenarios to the Tasks that wire them and re-slice Tickets. **Answer**: accept. → D-grill-in-spec-driven.42
- **SR1-F2** (old-rule plans break and their `context.md` is never read). Options: (a) tolerate legacy plans, (b) migrate on touch, (c) no transition. Recommended (a). **Answer**: tolerate legacy plans and also plans from other workflows, so the user can review and work with teammates who do not use spec-driven. Follow-up: how spec-driven builds from a foreign plan: (a) as input to a native Spec, (b) execute it directly, (c) review only. Recommended (a). **Answer**: (a). → D-grill-in-spec-driven.43, D-grill-in-spec-driven.44
- **SR1-F3** (record numbers collide across branches). Options: (a) slug-based names, (b) keep `NNNN` and renumber on merge, (c) timestamp names. Recommended (a). **Answer**: (a). → D-grill-in-spec-driven.7, D-grill-in-spec-driven.8, D-grill-in-spec-driven.30
- **SR1-F4** (publishing Tickets has no rule for re-runs and failures). Recommended four rules; alternative dropped the review precondition. **Answer**: all four. → D-grill-in-spec-driven.25
- **SR1-F5** (the implicit-requirement sweep was skipped). The agent resolved seven dimensions from facts and earlier answers and asked two. Partial failure: (a) write the record as the grill goes, with a `draft` status, (b) write at the end. Recommended (a). **Answer**: (a). Input validation of `summary.md`: (a) warn and fall back to reading record headers, (b) stop and ask. Recommended (a). **Answer**: (a). → D-grill-in-spec-driven.11, D-grill-in-spec-driven.17, D-grill-in-spec-driven.47
- **SR1-F6** (fix tasks belong to no Ticket). Options: (a) one fix Ticket per review or Verifier round, (b) fix tasks join the Ticket they repair, (c) exempt fix tasks. Recommended (a). **Answer**: (a). → D-grill-in-spec-driven.45
- **SR1-F7** (multi-context repos lose context-scoped decisions). Recommended following `CONTEXT-MAP.md` or an `fd` probe for every `docs/adr/`, and protecting every `CONTEXT.md` in the review snapshot. **Answer**: accept. → D-grill-in-spec-driven.17, D-grill-in-spec-driven.33
- **SR1-F8** (Decisions & Assumptions cell check underspecified). Recommended checking each table by header name, with two Scenarios. **Answer**: accept. → D-grill-in-spec-driven.34
- **SR1-F9** (tests depend on host graphify and on hiding `fd`). Recommended a graphify stub and a symlinked bin directory. **Answer**: rejected the stub; tests require the real graphify. The user added that an agent at work had deleted `graphify-out/` because it was gitignored, and asked for a rule that it is never deleted. For hiding `fd`, the user said the Verifier's judgment is enough and no automated test is needed. → D-grill-in-spec-driven.38, D-grill-in-spec-driven.46
- **SR1-F10** (`prototype` and the `ready-for-agent` label leave routes outside spec-driven). The user asked for a clearer statement. Recommended: `prototype` hands its verdict to Specify, and published Tickets drop the label. **Answer**: accept. → D-grill-in-spec-driven.25, D-grill-in-spec-driven.26
- **SR1-F11** (one ID bundles nine Decisions). Recommended splitting. **Answer**: the user replaced supersession altogether: a changed Decision is rewritten in place and git keeps the history. Follow-up: (a) a rewritten Decision gets a `Changed` line naming when and why, (b) no marker. Recommended (a). **Answer**: (a). The split into nine Decisions stood. → D-grill-in-spec-driven.15, D-grill-in-spec-driven.29 to D-grill-in-spec-driven.37

### Spec Review SR2 grill (2026-11-14)
The user ran `/spec-review integrate-skills` again on the reworked plan (report `.specs/features/integrate-skills/spec-review-2.md`, 7 Findings) and asked to be grilled on each one.

- **SR2-F1** (foreign-plan review reports named by file basename collide). Options: (a) one folder per foreign plan named from its repo-relative path, with folder targets reviewed as one plan, (b) flat files with the path slug in the name. Recommended (a). **Answer**: (a). → D-grill-in-spec-driven.43
- **SR2-F2** (the `inspect` row and the Verifier's existing table can disagree). Options: (a) one table, the existing Scenario-Anchored one, read by header name, (b) a separate `## Inspect proofs` section. Recommended (a). **Answer**: (a). → D-grill-in-spec-driven.42
- **SR2-F3** (fixture specs inside test functions register as Scenario claims). Recommended fixtures as `.md` files under `tests/fixtures/`; alternative was changing the checker. **Answer**: accept. → D-grill-in-spec-driven.38
- **SR2-F4** (a `retired` record status the user never chose). The agent had added it while rewriting D-grill-in-spec-driven.8 and wrongly marked it as the user's. Options: (a) drop it, (b) keep it with a user-only rule. Recommended (a). **Answer**: (a). → D-grill-in-spec-driven.8, D-grill-in-spec-driven.17
- **SR2-F5** (two definitions of a legacy plan). Recommended two rules: `context.md` is read whenever it exists, and a feature named in a `summary.md` Specs cell counts as native even without the `**Grilling Record**:` line. **Answer**: only the first rule. → D-grill-in-spec-driven.17, D-grill-in-spec-driven.33, D-grill-in-spec-driven.43
- **SR2-F6** (`wizard` commits scripts outside spec-driven). Options: (a) a named exception to the Goal, (b) route committed wizards through a Small Specify. Recommended (a). The user asked what `wizard` was; they had never used it and did not know where it came from. The agent reported it was vendored from mattpocock/skills in commit `5544263` and nothing depends on it, added (c) retire it, and changed its recommendation to (c). **Answer**: (c). → D-grill-in-spec-driven.21, D-grill-in-spec-driven.35
- **SR2-F7** (`install.sh` deletes retired skills by name alone in a shared folder). Options: (a) delete only folders whose `SKILL.md` matches what this repo shipped and that are not symlinks, (b) ask before each deletion, (c) leave it. Recommended (a). **Answer**: (a). → D-grill-in-spec-driven.35

## Decisions

### D-grill-in-spec-driven.1 · Specify is the grill
- **Choice**: spec-driven's Specify phase runs the grilling discipline together with domain-modeling, then writes `spec.md`. Discuss folds into it. `/grill-with-docs` stays for grilling things that are not features.
- **Reason**: spec-driven owns the artifact, the gates and the reviewer contract, and the grill gets more complete requirements than Specify's own questions.
- **Trade-off**: Specify gets longer; `/grill-with-docs` remains a second entry point to the same interview.
- **Binds**: project · **Decided by**: user

### D-grill-in-spec-driven.2 · One question per turn, always
- **Choice**: every planning question is asked alone, with options and a recommended answer, in dependency order. No pace menu. Two escapes: "you decide" (the agent's default is recorded with `Decided by: agent`) and "decide the rest" (the agent lists its defaults for every remaining branch in one turn, overridable in one reply).
- **Reason**: the pace menu dilutes the grill; the escapes keep trivial branches cheap.
- **Trade-off**: more turns on features where Quick pace would have been enough.
- **Binds**: project · **Decided by**: user

### D-grill-in-spec-driven.3 · No per-feature `context.md`
- **Choice**: behavior answers become acceptance criteria with Scenarios; other answers become rows in the spec's "Decisions & Assumptions" table. Deferred Ideas become Out of Scope rows with reason `deferred`; Specific References become an optional `## References` section.
- **Reason**: one file for Design and the spec-reviewer, and no `context.md`/`CONTEXT.md` clash.
- **Trade-off**: `spec.md` grows; the separate "locked vs discretion" file is gone (the Decided-by column replaces it).
- **Binds**: project · **Decided by**: user

### D-grill-in-spec-driven.4 · No ADRs
- **Choice**: nothing in this workflow writes or names ADRs. Decisions live under `.specs/`, and every skill reads them there.
- **Reason**: "Architecture Decision Record" implies a team discussed and agreed. A solo developer and an agent produce a record of their own choices; the name misleads.
- **Trade-off**: breaks with a widespread convention other tools and people recognize.
- **Binds**: project · **Decided by**: user

### D-grill-in-spec-driven.5 · Decision files under `.specs/decisions/` with a `summary.md` index
- **Choice**: Decisions live in ADR-shaped files under `.specs/decisions/`, never called ADRs. Every project-binding Decision gets a file whatever its origin. `.specs/decisions/summary.md` is the single index; there is no aggregator script.
- **Reason**: work repos are large. One growing file does not scale, and Decisions buried in spec tables need a second lookup mechanism.
- **Trade-off**: a feature's Decisions live in two places (the record holds the full text, the spec links to it).
- **Binds**: project · **Decided by**: user

### D-grill-in-spec-driven.6 · One Grilling Record per grilling session, complete by prompt
- **Choice**: one file per session, holding every Decision with its own ID. Required sections: Context (problem, forces, code facts with `file:line`, constraints, outside sources), Session path (every question in order with options, recommendation and answer, including rejected options and retries), Decisions (choice, reason, trade-off, Binds, Decided by, and a `Changed` line once rewritten), Consequences, Related. A feature's record also has `## Design` and, after a Spec or Change Review adds Decisions, `## Review`. One choice per Decision: a list of unrelated choices is split into separate Decisions. Completeness is enforced by the template's wording, not by a validator.
- **Reason**: grill decisions form one chain; per-Decision files lose the "why". The old template literally told models to write one paragraph.
- **Trade-off**: no deterministic guard; a model can still write a thin record, and only the spec-reviewer (D-grill-in-spec-driven.20) catches it.
- **Binds**: project · **Decided by**: user
- **Changed**: 2026-11-14 by integrate-skills (spec-review-1 SR1-F11): Status field removed from Decisions, `## Amendments` replaced by `## Review`, one choice per Decision.
### D-grill-in-spec-driven.7 · Every feature grill writes a Grilling Record named by slug
- **Choice**: every feature grill writes its record to `.specs/decisions/<slug>.md`; `spec.md` Decision rows link to it. The slug is 2 to 4 words and must not already exist in `.specs/decisions/`; the agent checks before creating the file. One ID per Decision, `D-<slug>.k`, used in the record, `spec.md`, `design.md` and reviews.
- **Reason**: the user wants the full history, including rejected alternatives, for every feature. Slug names cannot collide silently across branches: the same slug on two branches is a git add/add conflict, different slugs never clash.
- **Trade-off**: IDs are longer than `D-0004.3`; the folder grows with every feature, mitigated by the Binds and Areas columns (D-grill-in-spec-driven.8).
- **Binds**: project · **Decided by**: user
- **Changed**: 2026-11-14 by integrate-skills (spec-review-1 SR1-F3): numbered `NNNN-slug.md` names and `D-NNNN.k` IDs replaced by slug names and `D-<slug>.k` IDs.
### D-grill-in-spec-driven.8 · `summary.md` is a table of all decision files
- **Choice**: one row per finished Grilling Record with columns `File | Date | Summary | Status | Binds | Areas | Specs`. Rows are sorted by Date, then File. Summary is one or two sentences. A record's Status is `draft` while its grill runs and `active` once it is finished; only finished records have a row, so the Status cell reads `active`. A Decision that stops applying is rewritten to say so (D-grill-in-spec-driven.15); its record stays `active`. Binds is `project` when any Decision in the file binds the project. Areas lists the code paths the Decisions govern, `*` for repo-wide. `summary.md` is an index: each record's header is the source of truth.
- **Reason**: a cheap first read in big repos; consumers filter by Binds and Areas before opening files. Sorting by date keeps concurrent additions apart.
- **Trade-off**: one more file the agent must keep in sync by hand.
- **Binds**: project · **Decided by**: user
- **Changed**: 2026-11-14 by integrate-skills (spec-review-1 SR1-F3, SR1-F11; spec-review-2 SR2-F4): Date column added, rows sorted, supersession statuses removed; the `retired` status the agent had added was dropped, leaving `draft` and `active`.
### D-grill-in-spec-driven.9 · The file is a Grilling Record
- **Choice**: the glossary term is **Grilling Record**. _Avoid_: ADR, decision record, session notes.
- **Reason**: names what the file is and promises nothing about team agreement.
- **Trade-off**: "grill" also names discussing a Finding in review; those notes stay `**Grill notes**:` lines unless a Decision changes (D-grill-in-spec-driven.15).
- **Binds**: project · **Decided by**: user

### D-grill-in-spec-driven.10 · Binds test
- **Choice**: a Decision binds the project when a future feature must follow it or knowingly change it; otherwise it binds its feature. The old three-criteria test is dropped. The agent states the proposed Binds inside each recommendation.
- **Reason**: every Decision is now written, so the old gate has no job; Binds now decides who must read a Decision.
- **Trade-off**: more project rows than the old sparse log had.
- **Binds**: project · **Decided by**: user
- **Changed**: 2026-11-14 by integrate-skills (spec-review-1 SR1-F11): "knowingly supersede" became "knowingly change", since Decisions are rewritten in place.

### D-grill-in-spec-driven.11 · Write timing
- **Choice**: before the first question, Specify loads confirmed lessons, reads `summary.md` rows for the touched Areas and `CONTEXT.md`, runs discovery, runs the graphify capability search and discovers Repo Standards, raising any Redundant Feature first. The Grilling Record is created after the first answer with header `Status: draft` and gets each answer appended immediately; `CONTEXT.md` updates inline. A session that finds a `draft` record for its feature resumes from that record's Session path. At shared understanding the agent finishes Decisions and Consequences, sets `Status: active`, adds the `summary.md` row, writes `spec.md`, runs `validate_spec.py` and presents. Consumers ignore `draft` records.
- **Reason**: an incremental record survives compaction, crashes and pauses; criteria depend on the whole tree, so the spec waits.
- **Trade-off**: a half-written record exists while the grill runs.
- **Binds**: project · **Decided by**: user
- **Changed**: 2026-11-14 by integrate-skills (spec-review-1 SR1-F5): `draft` status, resume rule, and consumers ignoring drafts added.
### D-grill-in-spec-driven.12 · No migration; legacy paths are pointed to
- **Choice**: existing `docs/adr/` files and `STATE.md ## Decisions` entries stay where they are and are never written again. `summary.md` carries a line for each that exists, saying it is a legacy decision source consumers must also check.
- **Reason**: the user chose to leave old records alone.
- **Trade-off**: repos keep two places to look until old records age out.
- **Binds**: project · **Decided by**: user (STATE.md extension: agent, not objected to)
- **Changed**: 2026-11-14 by integrate-skills (spec-review-1 SR1-F2): "legacy decision path" became "legacy decision source", because CONTEXT.md already defines Legacy Path as old code kept alive by tests.

### D-grill-in-spec-driven.13 · Glossary location unchanged
- **Choice**: root `CONTEXT.md`, or a root `CONTEXT-MAP.md` pointing to per-context `CONTEXT.md` files.
- **Reason**: the glossary describes the code's domain; per-context files sit beside their code in big repos; existing repos need no move.
- **Trade-off**: planning artifacts are not all under `.specs/`.
- **Binds**: project · **Decided by**: user

### D-grill-in-spec-driven.14 · Vendored `grilling` is the one source of grill rules
- **Choice**: `skills/grilling/` is vendored into this repo and gains the escapes (D-grill-in-spec-driven.2) and the Binds-in-recommendation rule (D-grill-in-spec-driven.10). domain-modeling owns the `CONTEXT.md` format, the Grilling Record format and the `summary.md` format; `ADR-FORMAT.md` is replaced. `specify.md` calls the Skill tool for `grilling` and `domain-modeling` and adds only spec-specific steps: capability search, Standards, the dimensions sweep as closing branches, criteria and Scenarios, and the gate. Where a harness cannot load skills by name, Specify reads `../grilling/SKILL.md` and `../domain-modeling/SKILL.md` next to its own directory.
- **Reason**: one source per rule, and four other callers stop failing in opencode.
- **Trade-off**: Specify depends on two sibling skills being installed.
- **Binds**: project · **Decided by**: user

### D-grill-in-spec-driven.15 · Changed Decisions are rewritten in place
- **Choice**: when a review Disposition, a later phase or a later feature changes a Decision, the Decision's text is rewritten in its original record and gains one line: `Changed: <date> by <feature> (<source, e.g. spec-review-1 SR1-F3>): <what changed>`. Git keeps the old text. New Decisions that a review adds go into the record's `## Review` section with the next ID. The Session path is never rewritten; a review grill appends its own subsection to it. A Finding that changes no Decision leaves only its Disposition line. The `summary.md` row is updated when the record's summary or Areas change.
- **Reason**: documentation stays clear when every Decision shows its current choice; git already versions the history.
- **Trade-off**: a reader of an old spec may see a Decision that no longer matches what that spec built; the `Changed` line points them to the history.
- **Binds**: project · **Decided by**: user
- **Changed**: 2026-11-14 by integrate-skills (spec-review-1 SR1-F11): `## Amendments` and supersession replaced by in-place rewriting with a `Changed` line.
### D-grill-in-spec-driven.16 · Design writes into the feature's Grilling Record
- **Choice**: Design appends a `## Design` section to the feature's record. Design questions follow the grill rules (the approach choice is one question). Its Decisions continue the record's numbering, each with Binds and Decided by, including agent-only choices. `design.md` Tech Decisions become links to those IDs. Changing another record's Decision rewrites it in that record (D-grill-in-spec-driven.15).
- **Reason**: one record holds grill, Design and review decisions for a feature.
- **Trade-off**: records get long for Large features.
- **Binds**: project · **Decided by**: user
- **Changed**: 2026-11-14 by integrate-skills (spec-review-1 SR1-F11): cross-record supersession replaced by in-place rewriting.
### D-grill-in-spec-driven.17 · One read rule for every consumer
- **Choice**: every consumer of Decisions (Specify, Design, Tasks, Execute, the Verifier, both reviewers, `tdd`, `diagnosing-bugs`, `improve-codebase-architecture`, domain-modeling) runs discovery (D-grill-in-spec-driven.18), then reads `summary.md` if present and opens the `active` records that either bind the project with Areas overlapping the paths being touched (or Areas `*`) or name the current feature in Specs. `draft` records are skipped. When a `summary.md` row cannot be parsed, names a missing file, or a record has no row, the consumer warns, names the problem, lists `.specs/decisions/*.md` and decides from each record's header instead. Legacy sources are checked when present, with or without `summary.md`: `STATE.md ## Decisions`; the root `docs/adr/`; each context's `docs/adr/` listed in `CONTEXT-MAP.md`, or, without a map, every directory found by `fd -t d -p 'docs/adr$'` with the discovery excludes; and the current feature's `context.md` whenever that file exists, whatever the plan kind. Active project-binding Decisions count as Repo Standards.
- **Reason**: cheap reads in big repos, nothing silently ignored, collaborators' material on other flows is found, and a bad merge of `summary.md` does not block anyone.
- **Trade-off**: every consumer pays a small read cost on every run.
- **Binds**: project · **Decided by**: user
- **Changed**: 2026-11-14 by integrate-skills (spec-review-1 SR1-F2, SR1-F5, SR1-F7; spec-review-2 SR2-F4, SR2-F5): drafts skipped, malformed-index fallback, per-context `docs/adr/` added; `retired` removed; `context.md` read whenever it exists.
### D-grill-in-spec-driven.18 · Discovery is a general fd listing
- **Choice**: two commands, read by the agent, which judges relevance and drills deeper where something looks like planning or decision material from another flow:
  ```sh
  fd -H --no-ignore-vcs -t d --max-depth 3 -E .git -E node_modules -E .venv -E venv
  fd -H --no-ignore-vcs -t f --max-depth 1
  ```
  `--no-ignore-vcs` shows gitignored files but still honors `.ignore`/`.fdignore`, so a team tunes the listing without editing the skill. When `fd` is missing, the agent pauses and asks the user to install it.
- **Reason**: `git ls-files` misses gitignored material; a full listing drowns in dependency trees; name filters only find flows we already know.
- **Trade-off**: depends on `fd`; the agent's judgment, not a pattern, decides what is relevant.
- **Binds**: project · **Decided by**: user

### D-grill-in-spec-driven.19 · Discovery runs every time and is not stored
- **Choice**: every consumer runs discovery as step 0 of the read rule. Nothing stores the result. Specify and Design cite the outside sources they actually used in the Grilling Record's Context.
- **Reason**: a stored list goes stale when a teammate adds a folder; two depth-limited fd calls are cheap.
- **Trade-off**: repeated work across consumers.
- **Binds**: project · **Decided by**: user

### D-grill-in-spec-driven.20 · Reviewer checks against Grilling Records
- **Choice**: both reviewers follow the read rule. spec-reviewer adds: Thought Partnership (high-impact `Decided by: agent` Decisions; branches never asked), Truthful Reporting (a Session-path answer the spec dropped or contradicts; spec content with no answer, Existing Capability or Repo Standard behind it), Practical Judgment (a conflict with an active project Decision or a discovered outside source that the record does not address), Communication (an incomplete record: thin Context, missing rejected options, a Decision without trade-off, several choices under one ID). change-reviewer adds: a Change contradicting an active Decision that was not rewritten, and a silent departure from a `Decided by: user` choice as a false Claim. Severity follows finding-format rules.
- **Reason**: the reviewer is the only completeness guard now that there is no validator (D-grill-in-spec-driven.6).
- **Trade-off**: more reviewer reading per run.
- **Binds**: project · **Decided by**: user
- **Changed**: 2026-11-14 by integrate-skills (spec-review-1 SR1-F2, SR1-F11): legacy `context.md` moved into the read rule, "without an amendment" became "not rewritten", bundled choices added to Communication.
### D-grill-in-spec-driven.21 · Retirements and the review distinction
- **Choice**: retire `ask-matt`, `implement`, `to-spec`, `to-tickets`, `triage`, `wayfinder` and `wizard`; delete `skills/engineering-README.md`; drop the "matt-pocock" naming. Implementation happens only through spec-driven, with no exception. spec-driven absorbs tickets; the useful parts of `to-tickets` (vertical slices, expand–contract for wide refactors, per-tracker publishing shapes) move into a spec-driven reference. The Verifier stays model-triggered and automatic; `/code-review` stays human-triggered; nothing model-driven runs `/code-review`. The README keeps a "based on mattpocock/skills" attribution, as MIT requires.
- **Reason**: the skills have diverged into a different workflow; one implementation path keeps every change specified, reviewed and verified. `wizard` committed scripts to the repo outside that path and the user had never used it.
- **Trade-off**: no lightweight ticket-only or triage flow remains, and no generator for manual-step scripts.
- **Binds**: project · **Decided by**: user (README and engineering-README handling: agent, not objected to)
- **Changed**: 2026-11-14 by integrate-skills (spec-review-2 SR2-F6): `wizard` added to the retired skills.
### D-grill-in-spec-driven.22 · `setup-spec-driven`
- **Choice**: `setup-matt-pocock-skills` becomes `setup-spec-driven`. It configures the issue tracker spec-driven publishes Tickets to and the domain docs layout. The triage-labels section goes; the domain docs section points at `.specs/decisions/`. It still writes `docs/agents/*.md` and the `## Agent skills` block in `CLAUDE.md` or `AGENTS.md`.
- **Reason**: names the workflow it configures; opencode and omp agents read `AGENTS.md`.
- **Trade-off**: one more setup step per repo before Tickets can be published.
- **Binds**: project · **Decided by**: user

### D-grill-in-spec-driven.23 · Tickets are day-sized slices of Tasks
- **Choice**: the Tasks phase slices top-down: the Spec into Tickets (about one day each, demoable alone, with Blocked-by edges), then each Ticket into atomic Tasks. Every Task belongs to exactly one Ticket. A Ticket carries title, what it delivers from the user's view, the criterion and Scenario IDs it covers, Blocked by, and its Task list. Wide refactors use expand–contract Tickets.
- **Reason**: the product team follows coherent deliverables; Tasks stay one commit each.
- **Trade-off**: two levels of breakdown to maintain.
- **Binds**: project · **Decided by**: user

### D-grill-in-spec-driven.24 · Tasks at every scope
- **Choice**: `tasks.md` is written for every scope, Small included. The "Execute lists steps inline" fallback goes away.
- **Reason**: the user reviews the work through `tasks.md`.
- **Trade-off**: more planning text for one-line changes.
- **Binds**: project · **Decided by**: user

### D-grill-in-spec-driven.25 · Publishing Tickets
- **Choice**: Tickets are published only on the user's explicit "publish tickets", independently of Execution Approval, and only when at least one Spec Review exists and every Finding of the latest one has a Disposition. Tickets go out in dependency order. Each Tracker ID is written into `tasks.md` immediately after its issue is created. A Ticket that already has a Tracker ID is never created again; when its content changed since publishing, the agent lists the drift and updates the issue only on a go-ahead. A tracker failure stops publishing and reports which Tickets were and were not published; the next "publish tickets" resumes at the first unpublished Ticket. Published issues link to their Spec and say the work is built through it; they carry no `ready-for-agent` label or "agent-grabbable" wording.
- **Reason**: tracker writes are outward-facing; the product team may need Tickets before the build decision; a retry must never duplicate issues; no route may let an agent build straight from the tracker.
- **Trade-off**: published Tickets can drift until the user approves an update.
- **Binds**: project · **Decided by**: user
- **Changed**: 2026-11-14 by integrate-skills (spec-review-1 SR1-F4, SR1-F10): review precondition, write-back per issue, skip-if-published, stop-and-resume on failure, and no `ready-for-agent` label.
### D-grill-in-spec-driven.26 · `tdd` is Execute's loop; no side doors
- **Choice**: Execute calls `tdd` by name and runs red, green, refactor per Scenario. `tdd`'s seam confirmation is satisfied by the Scenarios and Design; it asks only for interfaces neither names. `tdd` no longer advertises building features on its own; bug fixes go through spec-driven at Small scope. `diagnosing-bugs` keeps Phases 1–4 and hands its repro, root cause and seam to a Small Specify instead of applying the fix. `prototype` keeps the prototype on a throwaway branch as evidence and hands its verdict to Specify instead of folding it into the real code. `improve-codebase-architecture` treats active Decisions as it treated ADRs and records rejection reasons as Decisions in its Grilling Record.
- **Reason**: closes every route to implementation outside spec-driven; a test that fails first proves it can catch the bug.
- **Trade-off**: a one-line bug fix now needs a Small spec, a Spec Review and an Execution Approval.
- **Binds**: project · **Decided by**: user (diagnosing-bugs and improve-codebase-architecture handling: agent, not objected to)
- **Changed**: 2026-11-14 by integrate-skills (spec-review-1 SR1-F10): `prototype` hands its verdict to Specify.
### D-grill-in-spec-driven.27 · Dogfood this change
- **Choice**: this record, `summary.md`, `.specs/features/integrate-skills/spec.md`, `design.md` and `tasks.md` are written by hand to the new rules; the human runs `/spec-review`, records Dispositions and gives Execution Approval before anything is built.
- **Reason**: tests the new templates on a real case before any skill depends on them.
- **Trade-off**: the installed spec-driven still follows the old rules, so validators run against artifacts in the new shape.
- **Binds**: feature · **Decided by**: user

### D-grill-in-spec-driven.28 · Design at Medium scope and above
- **Choice**: Design is required for Medium, Large and Complex. Medium's `design.md` holds components, the reuse table and links to its Decisions; the approach question is asked only when real alternatives exist. Small skips Design when there is no architectural choice.
- **Reason**: the user corrected the default at the shared-understanding check.
- **Trade-off**: more planning for Medium features.
- **Binds**: project · **Decided by**: user

### D-grill-in-spec-driven.29 · The sweep closes the grill
- **Choice**: the implicit-requirement dimensions sweep becomes the grill's closing branches, tiered by scope as before (every dimension for Large and Complex, present ones for Medium, none for Small). Each dimension resolves to a criterion or an `N/A because ...` line in the spec.
- **Reason**: keeps the sweep's coverage without a second interview.
- **Trade-off**: long grills get a few more questions at the end.
- **Binds**: project · **Decided by**: agent (listed at the shared-understanding check, not objected to)
- **Changed**: 2026-11-14 by integrate-skills (spec-review-1 SR1-F11): split out of a bundle of nine defaults.

### D-grill-in-spec-driven.30 · Record names and sections
- **Choice**: Grilling Records are named `<slug>.md` with Decision IDs `D-<slug>.k` (D-grill-in-spec-driven.7). A feature's record grows `## Design` and `## Review` sections.
- **Reason**: one naming rule across records, specs and reviews.
- **Trade-off**: long IDs in prose.
- **Binds**: project · **Decided by**: agent (listed at the shared-understanding check, not objected to)
- **Changed**: 2026-11-14 by integrate-skills (spec-review-1 SR1-F3, SR1-F11): split out of a bundle; `NNNN-slug.md` replaced by `<slug>.md`, `## Amendments` by `## Review`.

### D-grill-in-spec-driven.31 · Non-feature grills write records too
- **Choice**: a `/grill-with-docs` session about something that is not a feature writes a Grilling Record with Specs `none`. If it turns into a feature, Specify continues that record.
- **Reason**: every grill leaves the same kind of record.
- **Trade-off**: some records have no spec to link.
- **Binds**: project · **Decided by**: agent (listed at the shared-understanding check, not objected to)
- **Changed**: 2026-11-14 by integrate-skills (spec-review-1 SR1-F11): split out of a bundle.

### D-grill-in-spec-driven.32 · `summary.md` holds only the index
- **Choice**: `summary.md` stores the table and the legacy-path lines, nothing else.
- **Reason**: a short first read.
- **Trade-off**: usage notes live in domain-modeling, not next to the table.
- **Binds**: project · **Decided by**: agent (listed at the shared-understanding check, not objected to)
- **Changed**: 2026-11-14 by integrate-skills (spec-review-1 SR1-F11): split out of a bundle.

### D-grill-in-spec-driven.33 · Review snapshot covers decisions and every glossary
- **Choice**: `prep_review.py`'s pre-review snapshot commit also covers `.specs/decisions/`, `CONTEXT-MAP.md` and every file named `CONTEXT.md`. A feature's `context.md` is listed in the Review context whenever it exists, whatever the plan kind. The Review context names the feature's Grilling Record.
- **Reason**: a grill edits those files, and a review must not stop on its own planning output; a `context.md` holds locked decisions the reviewer must see.
- **Trade-off**: a stray glossary edit elsewhere gets committed with the plan.
- **Binds**: project · **Decided by**: agent (listed at the shared-understanding check, not objected to); `context.md` rule: user
- **Changed**: 2026-11-14 by integrate-skills (spec-review-1 SR1-F2, SR1-F7, SR1-F11; spec-review-2 SR2-F5): split out of a bundle; every `CONTEXT.md` and `CONTEXT-MAP.md` added; `context.md` listed whenever it exists.
### D-grill-in-spec-driven.34 · Validator changes
- **Choice**: `validate_spec.py` renames "Assumptions & Open Questions" to "Decisions & Assumptions" and requires it at every scope (`none` allowed). It finds the Decisions and Assumptions tables by their header names and checks Choice and Rationale, and Chosen default and Rationale, naming the row on error. `validate_tasks.py` gains Ticket checks: every Task in exactly one Ticket, Blocked-by edges pointing backward. For a legacy spec-driven plan (D-grill-in-spec-driven.43) the new heading and Ticket checks are warnings, not errors. Foreign plans are not validated.
- **Reason**: the gates follow the new artifacts without breaking older plans.
- **Trade-off**: two validators carry a legacy branch.
- **Binds**: project · **Decided by**: agent (listed at the shared-understanding check, not objected to)
- **Changed**: 2026-11-14 by integrate-skills (spec-review-1 SR1-F2, SR1-F8, SR1-F11): split out of a bundle; header-name cell check and legacy warnings added.

### D-grill-in-spec-driven.35 · Installer changes
- **Choice**: `install.sh` adds the retired skills and `setup-matt-pocock-skills` to `RETIRED_SKILLS`, installs `grilling`, and warns when `fd` is missing. For each retired name it holds a short phrase from the `SKILL.md` this repo shipped. It deletes an installed folder only when that folder is not a symlink and its `SKILL.md` contains the phrase; otherwise it prints `skipped <name>: not installed by this repo` and leaves the folder alone.
- **Reason**: installed copies of retired skills would otherwise keep offering old routes; the skills folder is shared with other sources, and names such as `implement` and `triage` are generic.
- **Trade-off**: a retired copy the user edited heavily may no longer match and is left in place with a warning.
- **Binds**: project · **Decided by**: agent (listed at the shared-understanding check, not objected to); provenance check: user
- **Changed**: 2026-11-14 by integrate-skills (spec-review-1 SR1-F11; spec-review-2 SR2-F7): split out of a bundle; deletion now requires a matching `SKILL.md` and skips symlinks.
### D-grill-in-spec-driven.36 · `STATE.md` keeps only the handoff
- **Choice**: `STATE.md` keeps only `## Handoff`; old `AD-NNN` entries are read as legacy.
- **Reason**: Decisions now live in Grilling Records.
- **Trade-off**: none beyond the legacy read.
- **Binds**: project · **Decided by**: agent (listed at the shared-understanding check, not objected to)
- **Changed**: 2026-11-14 by integrate-skills (spec-review-1 SR1-F11): split out of a bundle.

### D-grill-in-spec-driven.37 · Improvement ideas during Execute
- **Choice**: improvement ideas noticed during Execute are surfaced to the user; an Out of Scope row with reason `deferred` is added only on a go-ahead.
- **Reason**: no scope creep and no silent edits to an approved plan.
- **Trade-off**: ideas the user ignores are lost.
- **Binds**: project · **Decided by**: agent (listed at the shared-understanding check, not objected to)
- **Changed**: 2026-11-14 by integrate-skills (spec-review-1 SR1-F11): split out of a bundle.
## Design

### D-grill-in-spec-driven.38 · Test strategy for a prompt-and-script repository
- **Choice**: deterministic behavior (the validators, `prep_review.py`, `install.sh`) is proven by stdlib `unittest` tests under `tests/`, one test per Scenario with the Scenario ID and Given/When/Then text in the docstring, each running against a throwaway fixture repository in a temporary directory. Fixture specs, tasks and validation files live as `.md` files under `tests/fixtures/` and are copied in by a helper; no test function contains sample Scenario text. The tests use the real `graphify`; no stub. Behavior a unit test cannot prove (skill prose, the installer's missing-`fd` warning) uses proof type `inspect` (D-grill-in-spec-driven.42) and is checked by the Verifier.
- **Reason**: the repository has no test suite and no Repo Standard for one; `pytest` is not installed, `unittest` is. A text-matching test over skill prose would be an Implementation-Coupled Test. graphify is a required tool, so the tests require it too. The Scenario checker reads every line of a test function, so inline fixture text would count as extra claims.
- **Trade-off**: `inspect` Scenarios are not re-checked automatically on later Changes; the tests fail on a machine without graphify.
- **Binds**: feature · **Decided by**: agent; graphify and the `fd` check: user
- **Changed**: 2026-11-14 by integrate-skills (spec-review-1 SR1-F1, SR1-F9; spec-review-2 SR2-F3): manual UAT replaced by `inspect`; real graphify required; the missing-`fd` check moved to `inspect`; fixtures moved to `tests/fixtures/`.
### D-grill-in-spec-driven.39 · Ticket markup in `tasks.md`
- **Choice**: a `## Tickets` section with one `### K<n>: <title>` block per Ticket, carrying `**Delivers**`, `**Covers**`, `**Blocked by**` and `**Tasks**` fields. Ticket headings use `K` so they never match the `T<n>` task pattern. Each Ticket is one Execution Plan phase.
- **Reason**: keeps the existing task parser untouched and makes the Ticket checks a separate pass.
- **Trade-off**: `K` is an arbitrary letter the reader must learn.
- **Binds**: project · **Decided by**: agent

### D-grill-in-spec-driven.40 · `prep_review.py` gates the mandatory plan files
- **Choice**: `prep_review.py spec` stops with `STOP` when `tasks.md` is missing at any scope, or when `design.md` is missing at Medium scope and above.
- **Reason**: makes D-grill-in-spec-driven.24 and D-grill-in-spec-driven.28 deterministic at the one point every plan passes through before review.
- **Trade-off**: a Small feature with a trivial `tasks.md` still needs the file.
- **Binds**: project · **Decided by**: agent

### D-grill-in-spec-driven.41 · One home for the read rule and discovery
- **Choice**: the read rule (D-grill-in-spec-driven.17), discovery (D-grill-in-spec-driven.18) and the legacy-path check live in one new file, `skills/spec-driven/references/decisions.md`. spec-driven's phases link to it; both reviewer agents read it through `{{SPEC_DRIVEN_DIR}}`; `tdd`, `diagnosing-bugs`, `improve-codebase-architecture` and `domain-modeling` point to it as `../spec-driven/references/decisions.md`. domain-modeling keeps only the formats it owns (D-grill-in-spec-driven.14).
- **Reason**: one source for a rule ten consumers follow; spec-driven owns `.specs/`.
- **Trade-off**: four non-spec-driven skills now depend on spec-driven being installed beside them.
- **Binds**: project · **Decided by**: agent

## Review

Decisions added by Spec Review SR1 (`.specs/features/integrate-skills/spec-review-1.md`).

### D-grill-in-spec-driven.42 · Proof types: `test` and `inspect`
- **Choice**: every Scenario has a proof type, `test` (default) or `inspect`, shown in the Test Coverage Matrix and on its Task. `inspect` is for changes a unit test cannot prove: markdown prompts, IaC, configuration. The per-Task gate passes only `test` Scenario IDs to `validate_scenarios.py --only`. The Verifier, the existing independent sub-agent, checks each `inspect` Scenario against the final files. `validation.md` has one results table, the Verifier's existing Scenario-Anchored table, with exactly one row per Scenario of either proof type; for an `inspect` Scenario the evidence cell holds the `file:line` read and one sentence on why that text meets the Then steps (IaC may cite command output such as `terraform plan`). `validate_scenarios.py` finds that table by its `Scenario` and `Result` headers and accepts an `inspect` Scenario only when its row's Result is `PASS`, with or without the `✅` mark; a `❌ GAP` row, a missing row or a duplicate ID fails. Each Task claims only Scenarios its own change delivers.
- **Reason**: prompt behavior cannot be unit tested, and the old gates failed every Scenario without a test. Two tables keyed by the same ID could disagree.
- **Trade-off**: inspection proves the text says the right thing, not that a model obeys it.
- **Binds**: project · **Decided by**: user
- **Changed**: 2026-11-14 by integrate-skills (spec-review-2 SR2-F2): the separate inspect row format was replaced by one row in the existing Scenario-Anchored table, read by header name.
### D-grill-in-spec-driven.43 · Three kinds of plan
- **Choice**: a **native** plan has a `**Grilling Record**:` line in `spec.md` and gets every check. A **legacy** spec-driven plan is a `.specs/features/<f>/spec.md` without that line; it gets the new heading and Ticket checks as warnings. That line alone decides between the two. A **foreign** plan is anything else (a teammate's PRD, a design doc, another tool's spec folder, a ticket): it is never structurally validated and never edited, and its content is read as a requirement and decision source. Discovery notes foreign plan folders in the record's Context. `/spec-review <path>` on a foreign plan skips the validators, says why, and writes its report to `.specs/reviews/<repo-relative path as a slug>/spec-review-<n>.md` (for example `.kiro/specs/payments/design.md` gives `kiro-specs-payments-design/`), so each plan has its own run numbers and previous run. When that folder already belongs to a different plan path (`docs/042_billing.md` and `docs/042-billing.md` give the same slug), a short hash of the repo-relative path is appended to the slug, so two plans never share a report folder. A folder target is one plan: every markdown file in it is reviewed together and the slug comes from the folder path.
- **Reason**: the user works with teammates who do not follow this workflow and must be able to review and build on their plans. Other tools reuse file names such as `design.md` in every feature folder.
- **Trade-off**: three code paths in the validators and `prep_review.py`; a native spec that loses its `**Grilling Record**:` line is checked as legacy.
- **Binds**: project · **Decided by**: user
- **Changed**: 2026-11-14 by integrate-skills (spec-review-2 SR2-F1, SR2-F5): report folder per foreign plan and folder targets added; the "or with a `context.md`" clause removed.
- **Changed**: 2026-11-16 by integrate-skills (change-review-1 CR1-F2): a short path hash is appended to the report slug when another plan already owns that folder.
### D-grill-in-spec-driven.44 · Building from a foreign plan
- **Choice**: spec-driven never executes a foreign plan directly. Specify takes it as input, grills only the gaps, and writes a native `spec.md` that links to the source with its commit or date and copies none of it.
- **Reason**: Execute needs Scenarios, Tasks and gates; the teammate's document stays theirs.
- **Trade-off**: building from a teammate's plan needs a Specify pass first.
- **Binds**: project · **Decided by**: user

### D-grill-in-spec-driven.45 · Fix Tickets
- **Choice**: each Change Review or Verifier round that produces fix tasks adds one Ticket, for example `### K7: Fix CR1` or `### K8: Fix Verifier round 2`, Blocked by the Tickets it repairs and covering the Scenarios it repairs. It is published only on "publish tickets" under D-grill-in-spec-driven.25.
- **Reason**: every Task belongs to a Ticket, shipped Tickets stay closed, and the product team sees fix work.
- **Trade-off**: more Tickets on the tracker.
- **Binds**: project · **Decided by**: user

### D-grill-in-spec-driven.46 · `graphify-out/` is never deleted
- **Choice**: spec-driven's `SKILL.md` and `standards.md` state that `graphify-out/` is the graph cache, that many repos gitignore it or list it in `.git/info/exclude`, that ignored does not mean disposable, and that agents never delete or clean it; they refresh it with `graphify update .`.
- **Reason**: an agent at work deleted the graph because it was gitignored; the graph saves tokens and makes answers direct in large codebases.
- **Trade-off**: none.
- **Binds**: project · **Decided by**: user

### D-grill-in-spec-driven.47 · Implicit-requirement sweep for this feature
- **Choice**: concurrency: D-grill-in-spec-driven.7. Idempotency and retry: D-grill-in-spec-driven.25. External-dependency failure: tracker failure per D-grill-in-spec-driven.25, missing `fd` per D-grill-in-spec-driven.18, missing graphify stops `prep_review.py` as today. State-transition integrity: rewriting a Decision in another record (D-grill-in-spec-driven.15). Partial failure: the draft record (D-grill-in-spec-driven.11). Input validation: the `summary.md` fallback (D-grill-in-spec-driven.17). Auth and rate limits: N/A because there is no service and tracker access uses the user's own CLI login. Observability: N/A because nothing runs unattended; records and `validation.md` are the audit trail. Data lifecycle: records are never deleted; a Decision that stops applying is rewritten to say so.
- **Reason**: the Large-scope sweep was skipped in the first grill.
- **Trade-off**: none.
- **Binds**: feature · **Decided by**: user (two branches), agent (the rest)
- **Changed**: 2026-11-14 by integrate-skills (spec-review-2 SR2-F4): `retired` removed from the data-lifecycle line.

## Consequences

- spec-driven's Specify, Design, Tasks, Execute, validate and memory references, its SKILL.md auto-sizing table, its validators and `validate_scenarios.py` change; `discuss.md` is deleted.
- `skills/grilling/` is added; `domain-modeling` loses `ADR-FORMAT.md` and gains the Grilling Record and `summary.md` formats.
- Seven skills are deleted and `setup-matt-pocock-skills` becomes `setup-spec-driven`; `install.sh` removes their installed copies when they came from this repo.
- Both reviewer agents, `review.md` and `finding-format.md` change.
- `tdd`, `diagnosing-bugs`, `improve-codebase-architecture`, `grill-with-docs` and `prototype` read and write Decisions the new way; `prototype` and `diagnosing-bugs` hand off to Specify.
- Off-limits from now on: writing ADRs or `AD-NNN` entries, per-feature `context.md`, pace menus, building outside spec-driven, publishing Tickets without an explicit go-ahead, any model-driven `/code-review`, editing a teammate's foreign plan, and deleting `graphify-out/`.
- This repo's `docs/adr/0001-0003` stay as legacy and are listed in `summary.md`.

## Related

- Spec: `.specs/features/integrate-skills/spec.md`
- Spec Reviews: `.specs/features/integrate-skills/spec-review-1.md`, `.specs/features/integrate-skills/spec-review-2.md`
- Change Review: `.specs/features/integrate-skills/change-review-1.md`
- Glossary terms added or changed in `CONTEXT.md`: Decision, Grilling Record, Ticket, Task, Spec
- Legacy decisions in this repo: `docs/adr/0001-only-execution-approval-authorizes-building.md`, `docs/adr/0002-scenarios-not-tests-are-the-contract.md`, `docs/adr/0003-one-source-generated-harness-adapters.md`
