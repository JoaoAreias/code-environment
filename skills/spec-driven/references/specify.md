# Specify

**Goal**: Capture WHAT to build with testable, traceable requirements.

Specify is the grill. The agent interviews the user one question per turn until both share the same understanding of the feature, writes the whole interview into a **Grilling Record** as it goes, and only then writes `spec.md`. There is no pace menu and no separate discussion step, and Specify never writes a per-feature `context.md`: every answer ends up as an acceptance criterion or as a row of the spec's `## Decisions & Assumptions` section.

Two sibling skills own the rules Specify runs on, so they are stated once:

- **`grilling`** owns the interview: one question per turn, options, one recommendation, the "you decide" and "decide the rest" escapes.
- **`domain-modeling`** owns the formats: the glossary (`CONTEXT.md`), the Grilling Record and `.specs/decisions/summary.md`.

This file adds only what is specific to a spec: what happens before the first question, what the grill must cover, and how its answers become `spec.md`.

`<skill-dir>` below is the `spec-driven` skill directory.

## Implicit-Requirement Dimensions

The canonical rubric for requirements that are easy to miss. The grill closes with it (step 2); it is defined here, not duplicated.

| Dimension | What to cover |
| --------- | ------------- |
| Input validation & bounds | Limits, formats, sanitization |
| Failure / partial-failure states | Timeouts, partial saves, rollbacks |
| Idempotency / retry / duplicate handling | Safe retries, dedup keys |
| Auth boundaries & rate limits | Who can call what, throttle rules |
| Concurrency / ordering | Race conditions, ordering guarantees |
| Data lifecycle / expiry | TTL, archival, deletion |
| Observability | Logging, metrics, tracing hooks |
| External-dependency failure | Circuit breakers, fallbacks |
| State-transition integrity | Valid transitions, guards |

---

## Process

### 1. Before the first question

Do all of this before you ask the user anything. It is reading, not planning: none of it needs the user, except the one stop in 1.2.

**1.1 Load confirmed lessons.** Run `python3 <skill-dir>/scripts/lessons.py list --status confirmed` (optionally `--scope [area]` or `--query [term]` for the area this feature touches) and apply what comes back as guidance, so past verification failures shape this spec instead of repeating. Load only `confirmed` - never `candidate` or `quarantined`. If no store exists yet or no code tool is available, skip silently. See [lessons.md](lessons.md).

**1.2 Find the Decisions and plans that already apply.** Follow [decisions.md](decisions.md) from top to bottom:

- **Check `fd` first.** If `fd` is not on PATH, your first message asks the user to install `fd` and says why. Ask no planning question and do none of the steps below until `fd` is available.
- **Run discovery**: the two `fd` listings. Note every piece of planning or decision material from other flows that bears on this feature (another tool's spec folder, RFCs, PRDs, design documents), including gitignored ones.
- **Read `.specs/decisions/summary.md`** and open the `active` Grilling Records that bind the project in the area this feature touches, or that name this feature. Skip `draft` records, except this feature's own (1.6).
- **If the index is broken** (a row names a missing file or cannot be parsed, or an `active` record has no row), warn the user, name each problem (for example "`summary.md` names `gone.md`, which does not exist; `billing-rules.md` is active but has no row"), and decide which records to open from each record's header instead. A record whose header is `active`, binds the project and covers your area is opened even though it has no row.
- **Check the legacy decision sources** that exist: root and per-context `docs/adr/`, `.specs/STATE.md` `## Decisions`, and this feature's `context.md` when it has one.
- **Read the glossary**: `CONTEXT.md`, or the `CONTEXT.md` files `CONTEXT-MAP.md` points to for this area. Use its terms in every question and in the spec.

Everything this step finds is given. Do not ask the user to decide again what an active Decision already decides; if the feature has to contradict one, that conflict is a question for the grill, named by Decision ID.

**1.3 Search for existing capabilities (Knowledge Verification Chain Step 1).** Search the codebase for what already exists in this feature's area, following [standards.md](standards.md) section 4 (graphify, `graph_queries.py symbols` with concept words and synonyms, then `rg`). The most expensive planning mistake is a **Redundant Feature**: a capability the codebase already provides. Use what you find to ground your questions, not to constrain the spec to the current implementation. Keep the queries and findings: they go into the spec's `## Existing Capabilities` section.

**1.4 Discover Repo Standards** per [standards.md](standards.md) section 1. Active project-binding Decisions found in 1.2 are Repo Standards too. The sources and the rules that touch this feature go into the spec's `## Standards` section.

**1.5 Load the two sibling skills.** Load `grilling` and `domain-modeling` by name with your harness's skill tool (the Skill tool in Claude Code, the `skill` tool in opencode). If the harness offers no tool to load a skill by name, or the load fails, read the same text from the skills directory that contains spec-driven: `<skill-dir>/../grilling/SKILL.md` and `<skill-dir>/../domain-modeling/SKILL.md`, plus `<skill-dir>/../domain-modeling/GRILLING-RECORD-FORMAT.md`. Either way, you have read the grilling rules and the record format before your first question. If neither route works, stop and tell the user the two skills must be installed beside spec-driven.

**1.6 Look for a record to continue.** A feature has one Grilling Record, and Specify never starts a second one for the same work. List `.specs/decisions/` and check, in this order:

- **A `draft` record for this feature** (header `Status: draft`, `Specs` naming the feature): an earlier session was interrupted. Resume it: read its Session path, take every answer there as given, and do not ask any of those questions again. Your first question is the next unanswered branch. Do not create another record.
- **A non-feature record this feature grows out of** (a record with `Specs: none`, typically written by `/grill-with-docs`, that the user names or that plainly covers this request): continue that record instead of starting a new one. See "Continuing a non-feature record" below.
- **Neither**: the record is created at the first answer (step 2).

**Your first message.** What you found decides how you open:

1. If `fd` is missing, the message asks the user to install `fd` and contains nothing else.
2. Otherwise, when discovery found outside material that bears on the feature, start by naming it, by path (for example "I found `.kiro/specs/payments/` and `docs/rfcs/0007-ledger.md`, which both cover payments"), together with any broken-index warning. This comes before the first question.
3. If the search in 1.3 found a Redundant Feature, name the existing capability by its file path (for example "`src/export/csv.py` already exports orders to CSV") and make the one question of this message: what does the user need beyond it? No other question is asked until that one is answered.
4. Otherwise the message ends with the first grill question, or with the next unanswered branch when you are resuming a draft.

### 2. Grill until shared understanding

Run the interview by the `grilling` rules. They hold for every scope, Small included:

- **Every turn of yours contains exactly one question.** Never two, even when they look independent.
- **Every question lists its options and marks one as recommended**, with a line of reasoning. Options are concrete ("download the file" or "email the file"), never "Option A" or "how should it work?". The recommendation also says what the answer would bind (`project` or `feature`, by the Binds test in [decisions.md](decisions.md) section 5).
- **Ask in dependency order.** A question whose answer prunes others comes first.
- **Facts you look up; decisions you ask.** Anything discoverable by reading the environment (the codebase, config, docs, existing conventions, the Decisions from 1.2) you resolve yourself through the Knowledge Verification Chain. Reserve questions for decisions that are the user's to make: scope, priorities, product behavior, trade-offs. A question you could have answered by reading the code erodes trust and wastes a turn.
- **Challenge vagueness.** Never accept fuzzy answers. "Good" means what? "Users" means who? "Simple" means how? Make the abstract concrete: "Walk me through using this."
- **Sharpen the language as you go.** `domain-modeling` updates `CONTEXT.md` inline the moment a term is resolved.

**What the grill has to settle.** Walk the decision tree until you can write every acceptance criterion without guessing:

- the problem, who has it, and what success looks like;
- what is in scope and what is explicitly out;
- every piece of user-visible behavior that could reasonably go more than one way. The kind of feature tells you where to look:

  | The feature is something users... | Branches to look for |
  | --------------------------------- | -------------------- |
  | **SEE** | Layout, density, interactions, empty states |
  | **CALL** (an API) | Response format, errors, auth, versioning |
  | **RUN** (a CLI) | Output format, flags, modes, verbosity |
  | **READ** | Structure, tone, depth |
  | have **ORGANIZED** | Grouping, naming, duplicates, exceptions |
  | rely on for **state or contracts** | The implicit-requirement dimensions above |

Do not ask about architecture, libraries or code structure; those are Design's questions.

**The two escapes.**

- **"you decide"**: when the user answers a question with "you decide", your recommended option becomes that question's answer. Record it in the Grilling Record as a Decision that chooses the recommended option and reads `Decided by: agent`. Then ask the next question.
- **"decide the rest"**: when the user answers "decide the rest", your next turn lists one default for every branch you have not asked yet, each with a short reason, and asks which of them the user wants to change. Then wait. Write nothing to `spec.md` until the user replies. The defaults the user leaves alone become Decisions with `Decided by: agent`; the ones the user changes are `Decided by: user`. "Decide the rest" is not the confirmation of shared understanding: the closing branches and the check below still follow.

**Write the Grilling Record as you go.** Follow `GRILLING-RECORD-FORMAT.md` in `domain-modeling`. The record is what survives a compaction, a crash or a pause, so it is never written from memory at the end.

- **First answer: create the record.** As soon as the user answers the first question, create `.specs/decisions/<slug>.md` with the header line `Status: draft` and `Specs` naming the feature. Its Context holds what step 1 found, and its Session path holds that first question, its options, the recommendation and the answer. The slug is 2 to 4 words, normally the feature's name, and no existing record may use it: list `.specs/decisions/` first. If `<slug>.md` already exists and belongs to other work (an earlier feature, another grill), create the record under a different slug and leave the existing file unchanged.
- **Every later answer: append before you ask again.** Append the question, every option offered, the recommendation and the answer to the Session path, and add the Decision the answer settles, before the next question is shown. After the third answer the file holds three answered questions; the fourth question comes after that write.
- **Rejected options stay.** The Session path lists every option that was offered, including the ones the user turned down and any question that had to be asked a second time.
- **One choice per Decision**, each with choice, reason, trade-off, Binds and Decided by.
- **Cite the outside sources you used.** Every plan, RFC or document from another flow that shaped a question or an answer is cited in the record's Context, by path with its commit or date.

**Keep the scope fixed.** The grill clarifies the feature the user asked for; it does not add capabilities. When the user or you raise an idea that belongs to another feature, say so, note it as a deferred idea, and return to the current branch. Deferred ideas become rows of the spec's Out of Scope table with reason `deferred`. Products or behaviors the user points at ("I want it like X") go into the spec's optional `## References` section.

**Close with the dimensions sweep.** When the main branches are answered, the implicit-requirement dimensions become the grill's closing branches. Take them one at a time, like any other question:

- **Large / Complex:** go through every dimension in the table above. Resolve a dimension yourself when earlier answers or the code already settle it; ask about each dimension you cannot resolve that way, one question per turn. Every dimension ends as a requirement or as an explicit `N/A because [reason]`. No blank entries.
- **Medium:** cover only the dimensions obviously present in this feature's domain; collapse the rest into a single `remaining dimensions N/A for this scope`.
- **Small:** skip the sweep.

The `N/A because ...` escape is mandatory: it prevents inventing requirements to fill the checklist. Bound the sweep to THIS feature's scope; never add requirements outside the feature boundary. The spec records the outcome: its `## Decisions & Assumptions` section lists every dimension with the ID of the criterion that covers it or with its `N/A because` reason.

**Shared-understanding check.** When no branch is left, list the defaults you chose for branches that were never asked, summarise the Decisions, and ask the user to confirm shared understanding. That is the last question of the grill. Corrections the user makes here are answers like any other and go into the record.

#### Starting from a foreign plan

When the user asks to specify or build a feature from a foreign plan (a teammate's PRD, RFC or design document, another tool's spec folder), the plan is the input to Specify. spec-driven never executes it directly.

- **Read it first, completely**, during step 1. Treat what it already answers as given.
- **Ask only about its gaps**: what the plan leaves open, leaves ambiguous, or does not cover and a spec needs (precise outcomes, failure behavior, the dimensions sweep), and any place where it contradicts the code or an active Decision. Do not ask about anything the plan already answers.
- **Never edit the foreign plan.** It stays unchanged, byte for byte. If it looks wrong, say so to the user; its author changes it.
- **Link it, copy none of it.** The native `spec.md` carries a `**Source plan**:` line that links the plan with the commit that last changed it (`git log -1 --format=%h -- <path>`), or with the date you read it when the file is not committed. The spec states requirements in its own criteria and Scenarios and does not paste text from the plan. The record's Context cites the plan the same way and says which of its answers were taken as given.

#### Continuing a non-feature record

When the feature grows out of a Grilling Record whose `Specs` is `none`, Specify continues that record:

- Do not create a new record. Append to the existing file: new questions go into its Session path under a new subsection (`### Specify <feature> (<date>)`), and new Decisions continue its numbering. Its earlier Session path and Decisions stand; do not re-ask them.
- At the first answer you append, set the record's `Specs` header to the feature's name and change the `Specs` cell of its `summary.md` row from `none` to the feature's name.
- The record stays `active`. At shared understanding, bring its Consequences, Related, Areas, Binds and its `summary.md` row up to date.

### 2.5 Close the record, then write the spec

When the user confirms shared understanding, finish the record **before** writing `spec.md`:

1. **Complete the record.** Every Decision has its choice, reason, trade-off, Binds and Decided by, and holds exactly one choice. The record has all five required sections: Context, Session path, Decisions, Consequences and Related. Write Consequences and Related now.
2. **Set the header to `Status: active`.**
3. **Add the record's row to `.specs/decisions/summary.md`**, at its place in Date order (after every row with an earlier Date, then by File). The row holds File, Date, a one-to-two-sentence Summary, Status `active`, Binds, Areas, and Specs naming the feature.
4. **If this is the first Grilling Record in the repository**, create `summary.md` with it and add the legacy lines under `## Legacy decision sources`: one line naming `docs/adr/` when that directory exists (one per context that has its own), and one line naming `.specs/STATE.md` when it has a `## Decisions` section.

Then write `.specs/features/[feature]/spec.md` from the template below:

- **`**Grilling Record**:` line** at the top, linking the record. This line is what marks the plan as native.
- **Every Decision in the record gets a row** in the `## Decisions & Assumptions` table, and each row's ID links to that Decision's anchor in the record (`D-<slug>.k`). The record holds the full text; the row holds the choice and a short rationale.
- **Answers about behavior also become acceptance criteria** with Scenarios (steps 3 and 3.5). A choice such as "download, not email" is a Decisions row and shapes the criteria that describe the download.
- **Facts you assumed** without being able to verify them go into the Assumptions table, with the default you chose.
- **Deferred ideas** are Out of Scope rows with reason `deferred`; references are the optional `## References` section.
- **Do not write `context.md`.** The feature folder gets `spec.md` and nothing else from this phase.

**User stories and priorities.** Group the criteria into user stories: **P1 = MVP** (must ship), **P2** (should have), **P3** (nice to have). Each story MUST be **independently testable** - you can implement and demo just that story.

### 3. Write Acceptance Criteria (EARS notation)

Write every acceptance criterion in **EARS** (Easy Approach to Requirements Syntax). Each criterion resolves to exactly one pattern, which keeps it unambiguous and directly testable. Choose the pattern that fits the requirement instead of forcing everything into a single shape:

| Pattern | Keyword | Template | Use for |
| ------- | ------- | -------- | ------- |
| Ubiquitous | (none) | The [system] SHALL [response] | Always-on invariants and constraints |
| Event-driven | WHEN | WHEN [trigger] THEN the [system] SHALL [response] | A response to a discrete trigger |
| State-driven | WHILE | WHILE [state] the [system] SHALL [response] | Behavior that holds during a state |
| Optional-feature | WHERE | WHERE [feature is present] the [system] SHALL [response] | Behavior gated behind an optional capability or flag |
| Unwanted-behavior | IF / THEN | IF [undesired condition] THEN the [system] SHALL [response] | Errors, failures, invalid input, timeouts |
| Complex | combination | WHILE [state], WHEN [trigger] the [system] SHALL [response] | Richer behavior combining the above |

**Why patterns beat one shape:** failure states, state transitions, and optional behavior become first-class criteria instead of footnotes squeezed into WHEN/THEN. The patterns map onto the implicit-requirement dimensions above: state-transition integrity to State-driven; failure and external-dependency failure to Unwanted-behavior; feature flags to Optional-feature.

**Rules:** one requirement per criterion (never bundle two behaviors); use concrete values (a specific status code, a specific message, a bound) rather than "quickly" or "gracefully"; every criterion contains a SHALL and is measurable. `python3 <skill-dir>/scripts/validate_spec.py` flags any criterion without a SHALL and any that matches no recognized pattern.

### 3.5 Write Scenarios (the test contract)

Every Acceptance Criterion carries its own requirement ID and at least one Gherkin **Scenario**: a concrete Given/When/Then example. Scenarios, not tests, are the contract: each test written later proves exactly one Scenario and copies its ID and text verbatim ([standards.md](standards.md) section 3).

````markdown
1. **PAY-01**: IF the card is expired THEN the system SHALL decline the payment with error `card_expired`.

   ```gherkin
   Scenario: PAY-01.S1 expired card
     Given a card that expired last month
     When the customer pays 10.00
     Then the payment is declined with "card_expired"
     And no charge is created
   ```

   **Proof**: test
````

- IDs: the criterion is `<CAT>-<NN>`; its Scenarios are `<CAT>-<NN>.S1`, `.S2`, ... Edge cases use the same format.
- Concrete values, one observable outcome through the public interface, behavior a caller cares about. A Scenario that says *how* ("calls the gateway client") is a future Implementation-Coupled Test; rewrite it as *what*.
- Where an implicit-requirement dimension applies (partial failure, rollback, retries, concurrency, external-dependency failure), at least one Scenario covers the failure mode.
- **Proof type.** Each Scenario's fence is followed by a `**Proof**:` line. `test` means a Behavior Test proves it; it is the default and is assumed when the line is absent. `inspect` is for a change no test can exercise (a prompt, infrastructure code, configuration): the Verifier proves it by reading the final files. Never mark a Scenario `inspect` to avoid writing a test that could be written.
- `validate_spec.py` rejects a criterion without an ID or without a Scenario, and a Scenario without Given/When/Then.

### 4. Requirement Closure Gate (before confirm)

Before presenting the spec for confirmation, run the three checks below. The spec is not presentable for confirmation until every item is resolved or assumption-logged - this is the guarantee that no requirement leaves the spec silently unclear.

**Scope-tiered:** Large/Complex = full gate; Medium = resolve obvious ambiguities, log the rest as assumptions; Small = skip entirely (consistent with skipping the sweep).

1. **Unambiguity + precision (hard).** Every AC must (a) have a single interpretation and (b) define a precise, spec-defined expected outcome. Any AC that fails either check: resolve with the user, split it, or log it as an explicit assumption with the chosen interpretation and rationale. No AC proceeds readable two ways or with an undefined outcome.

2. **Open-questions / assumptions closure.** Enumerate every unresolved decision that surfaced during clarification. Each must be either (a) resolved with the user OR (b) recorded as an **assumption** (chosen default + rationale) in the spec's Decisions & Assumptions section. Nothing proceeds unmarked.

3. **Agent-made choices are marked.** Every branch the user handed over with "you decide" or "decide the rest", and every default you chose for a branch that was never asked, is a Decision with `Decided by: agent` in the Grilling Record and a row in the spec's Decisions & Assumptions section (chosen default + rationale) - never silently dropped.

Fix inline. This gate is bounded to THIS feature's stated dimensions and actual behavior - never to "anything imaginable." The Out of Scope table and anti-scope-creep rules remain the counterweights: the gate clarifies existing requirements, it never invents new ones.

**Deterministic backing (run before you present the spec).** The structural half of this gate is enforced by a script so it cannot drift when a step is forgotten: `python3 <skill-dir>/scripts/validate_spec.py <spec-path-or-feature>` checks that required sections exist, every AC is EARS-shaped (has a SHALL), no Decisions row has an empty Choice or Rationale, no Assumptions row has an empty Chosen default or Rationale, and requirement IDs are well-formed. A non-zero exit means fix before confirming. The script checks structure; you still own the judgment calls (is the interpretation right, is the outcome precise). If no code-execution tool is available, run the same checks by reading the spec.

---

## Template: `.specs/features/[feature]/spec.md` (Small scope)

Small changes still get a spec on disk so both reviewers can read it, and still get a short grill and a Grilling Record. No sweep, no closure gate, no traceability table.

````markdown
# [Feature Name] Specification

**Scope**: Small

**Grilling Record**: [`.specs/decisions/[slug].md`](../../decisions/[slug].md)

## Problem Statement

[1-2 sentences.]

## Existing Capabilities

[Queries run (graphify / graph_queries.py / rg), what they found, and why this is not a Redundant Feature.]

## Standards

[Repo Standard sources and the rules that touch this change, including active project Decisions by ID, or "none found - Smell Baseline only".]

## Decisions & Assumptions

[One row per Decision in the Grilling Record. Write the single word `none` when the grill produced no Decision and no assumption.]

| ID | Decision | Choice | Rationale | Decided by | Binds |
| --- | --- | --- | --- | --- | --- |
| [D-[slug].1](../../decisions/[slug].md#[anchor]) | [what was being decided] | [what was chosen] | [why, in a few words] | [user or agent] | [project or feature] |

## Acceptance Criteria

1. **[FEAT]-01**: WHEN [event] THEN the system SHALL [behavior]

   ```gherkin
   Scenario: [FEAT]-01.S1
     Given [state]
     When [trigger]
     Then [precise outcome]
   ```

   **Proof**: test

## Steps

1. [Step] → files: [list] → verify: [Scenario IDs / gate] → commit: [message]
````

---

## Template: `.specs/features/[feature]/spec.md` (Medium, Large, Complex)

````markdown
# [Feature Name] Specification

**Scope**: Medium | Large | Complex

**Grilling Record**: [`.specs/decisions/[slug].md`](../../decisions/[slug].md)

**Source plan**: [`[path/to/foreign-plan.md]`]([relative link]) at commit [short hash] (only when the spec was written from a foreign plan; use the date read when the plan is not committed)

## Problem Statement

[Describe the problem in 2-3 sentences. What pain point are we solving? Why now?]

## Existing Capabilities

[Queries run (graphify / graph_queries.py / rg), what they found, and why this is not a Redundant Feature. Name what this feature will reuse. Name planning material from other flows that discovery found and this spec used.]

## Standards

[Repo Standard sources found, then one line per rule that touches this feature, including active project Decisions by ID - or "none found - Smell Baseline only".]

## Goals

- [ ] [Primary goal with measurable outcome]
- [ ] [Secondary goal with measurable outcome]

## Out of Scope

Explicitly excluded. Documented to prevent scope creep. Ideas that came up during the grill and belong to another feature are listed here with reason `deferred`.

| Feature          | Reason                              |
| ---------------- | ----------------------------------- |
| [Feature X]      | [Why excluded]                      |
| [Deferred idea]  | deferred: [where it belongs]        |

---

## Decisions & Assumptions

Full text, reasons and trade-offs live in the Grilling Record. Every ambiguity is resolved or recorded here - nothing is left silently unclear. Decided by `user` is locked; `agent` may be revisited in Design or review.

| ID | Decision | Choice | Rationale | Decided by | Binds |
| --- | --- | --- | --- | --- | --- |
| [D-[slug].1](../../decisions/[slug].md#[anchor]) | [what was being decided] | [what was chosen] | [why, in a few words] | [user or agent] | [project or feature] |

| Assumption | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| [a fact assumed without being verified] | [what we'll do] | [why] | [y/n] |

**Implicit-requirement sweep** (every dimension for Large and Complex; for Medium, the dimensions present plus one line `remaining dimensions N/A for this scope`):

| Dimension | Resolution |
| --- | --- |
| Input validation & bounds | [criterion ID, or "N/A because ..."] |
| Failure / partial-failure states | [criterion ID, or "N/A because ..."] |
| Idempotency / retry / duplicate handling | [criterion ID, or "N/A because ..."] |
| Auth boundaries & rate limits | [criterion ID, or "N/A because ..."] |
| Concurrency / ordering | [criterion ID, or "N/A because ..."] |
| Data lifecycle / expiry | [criterion ID, or "N/A because ..."] |
| Observability | [criterion ID, or "N/A because ..."] |
| External-dependency failure | [criterion ID, or "N/A because ..."] |
| State-transition integrity | [criterion ID, or "N/A because ..."] |

**Open questions:** none - all resolved or logged above (required before the spec is confirmed).

---

## User Stories

### P1: [Story Title] ⭐ MVP

**User Story**: As a [role], I want [capability] so that [benefit].

**Why P1**: [Why this is critical for MVP]

**Acceptance Criteria** (each is one EARS rule with an ID, followed by its Scenarios and their proof type):

1. **[FEAT]-01**: WHEN [user action/event] THEN the system SHALL [expected behavior]

   ```gherkin
   Scenario: [FEAT]-01.S1 [short title]
     Given [concrete starting state]
     When [the trigger]
     Then [the precise expected outcome]
   ```

   **Proof**: test

2. **[FEAT]-02**: IF [invalid input / failure] THEN the system SHALL [graceful handling]

   ```gherkin
   Scenario: [FEAT]-02.S1
     Given [state]
     When [failing trigger]
     Then [precise failure outcome]
   ```

   **Proof**: test

**Independent Test**: [How to verify this story works alone - e.g., "Can demo by doing X and seeing Y"]

---

### P2: [Story Title]

**User Story**: As a [role], I want [capability] so that [benefit].

**Why P2**: [Why this isn't MVP but important]

**Acceptance Criteria**:

1. **[FEAT]-03**: WHEN [event] THEN the system SHALL [behavior]

   ```gherkin
   Scenario: [FEAT]-03.S1
     Given [state]
     When [trigger]
     Then [outcome]
   ```

   **Proof**: inspect

**Independent Test**: [How to verify]

---

### P3: [Story Title]

**User Story**: As a [role], I want [capability] so that [benefit].

**Why P3**: [Why this is nice-to-have]

**Acceptance Criteria**:

1. **[FEAT]-04**: WHEN [event] THEN the system SHALL [behavior]

   ```gherkin
   Scenario: [FEAT]-04.S1
     Given [state]
     When [trigger]
     Then [outcome]
   ```

   **Proof**: test

---

## Edge Cases

Edge cases are usually unwanted-behavior (IF/THEN) or boundary (WHEN) criteria, written like any other criterion: ID, EARS rule, Scenarios.

1. **[FEAT]-05**: IF [error scenario] THEN the system SHALL [graceful handling]

   ```gherkin
   Scenario: [FEAT]-05.S1
     Given [state]
     When [error trigger]
     Then [handling outcome]
   ```

   **Proof**: test

---

## Requirement Traceability

Each Acceptance Criterion's ID gets a row, tracked across design, tasks, and validation.

| Requirement ID | Story       | Phase  | Status  |
| -------------- | ----------- | ------ | ------- |
| [FEAT]-01      | P1: [Story] | Design | Pending |
| [FEAT]-02      | P1: [Story] | Design | Pending |
| [FEAT]-03      | P2: [Story] | -      | Pending |
| [FEAT]-04      | P3: [Story] | -      | Pending |
| [FEAT]-05      | Edge case   | -      | Pending |

**ID format:** `[CATEGORY]-[NUMBER]` (e.g., `AUTH-01`, `CART-03`, `NOTIF-02`)

**Status values:** Pending → In Design → In Tasks → Implementing → Verified

**Coverage:** X total, Y mapped to tasks, Z unmapped ⚠️

---

## Success Criteria

How we know the feature is successful:

- [ ] [Measurable outcome - e.g., "User can complete X in < 2 minutes"]
- [ ] [Measurable outcome - e.g., "Zero errors in Y scenario"]

---

## References

[Optional. Products, screens or behaviors the user pointed at during the grill ("I want it like X"). Leave the section out when there are none.]
````

**The Decision link.** A row's ID links to the Decision's heading in the record. For the heading `### D-csv-export.1 · Delimiter` the link is `../../decisions/csv-export.md#d-csv-export1--delimiter`: the heading in lowercase, punctuation dropped, each space turned into a hyphen.

---

## Tips

- **P1 = Vertical Slice** - A complete, demo-able feature, not just backend or frontend
- **EARS is code** - If you can't write a criterion as a test, rewrite it; pick the pattern (WHEN / WHILE / WHERE / IF / ubiquitous) that fits
- **Requirement IDs are mandatory** - Every story maps to trackable IDs
- **Edge cases matter** - What breaks? What's empty? What's huge?
- **Out of Scope prevents creep** - If it's not here, it doesn't get built; deferred ideas land here, not in a side file
- **One question per turn** - with options and one recommendation; "you decide" and "decide the rest" keep trivial branches cheap
- **The record is written as you go** - created at the first answer, appended after every answer, finished and indexed before `spec.md` exists
- **Closure gate before confirm** - Three checks: unambiguity + precision, open-questions/assumptions closure, agent-made choices marked; scope-tiered; bounded to stated dimensions; never invents requirements
- **Scenarios are the test contract** - every AC has an ID and at least one concrete Given/When/Then Scenario, each with its proof type
- **Search before you specify** - `## Existing Capabilities` records the graph search; a Redundant Feature is raised before anything else
- **Present after the gate passes** - Present the spec only after the closure gate passes and `validate_spec.py` exits clean. The user's agreement here is provisional: it means "continue planning", never "build". Building waits for `/spec-review` and Execution Approval ([review.md](review.md))
