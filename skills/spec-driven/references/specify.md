# Specify

**Goal**: Capture WHAT to build with testable, traceable requirements.

If the feature has ambiguous gray areas (multiple valid approaches for user-facing behavior), the agent will automatically trigger the [discuss gray areas](discuss.md) process within this phase. For clear, well-defined features, it goes straight to the next phase.

## Implicit-Requirement Dimensions

The canonical rubric for requirements that are easy to miss. Referenced by [discuss.md](discuss.md) - defined here, not duplicated.

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

### 1. Clarify Requirements

**Load confirmed lessons first:** Before clarifying, load the project's confirmed lessons so past verification failures shape this spec instead of repeating. Run `python3 <skill-dir>/scripts/lessons.py list --status confirmed` (optionally `--scope [area]` or `--query [term]` for the area this feature touches) and apply what comes back as guidance. Load only `confirmed` - never `candidate` or `quarantined`. If no store exists yet or no code tool is available, skip silently. See [lessons.md](lessons.md).

**Existing-capability search first (Knowledge Verification Chain Step 1):** Before asking questions, search the codebase for what already exists in this feature's area, following [standards.md](standards.md) section 4 (graphify, `graph_queries.py symbols` with concept words and synonyms, then `rg`). The most expensive planning mistake is a **Redundant Feature**: a capability the codebase already provides. If you find one, say so before anything else and ask what the user actually needs. Use what you find to ground your questions, not to constrain the spec to the current implementation. Record queries and findings in the spec's `## Existing Capabilities` section.

**Discover Repo Standards:** per [standards.md](standards.md) section 1, list the standards sources and the rules that touch this feature in the spec's `## Standards` section.

You are a thinking partner, not an interviewer. Start open - let the user dump their mental model. Follow the energy: whatever they emphasize, dig into that.

Ask conversationally (not as a checklist):

- "What problem are you solving?"
- "Who is the user and what's their pain?"
- "What does success look like?"

If needed:

- "What are the constraints (time, tech, resources)?"
- "What is explicitly out of scope?"

**Facts you look up; decisions you ask.** Anything discoverable by reading the environment (the codebase, config, docs, existing conventions) you resolve yourself through the Knowledge Verification Chain - do not spend the user's attention asking for it. Reserve questions for genuine decisions that are the user's to make: scope, priorities, product behavior, trade-offs. A question you could have answered by reading the code erodes trust and wastes a turn.

**Challenge vagueness.** Never accept fuzzy answers. "Good" means what? "Users" means who? "Simple" means how? Make the abstract concrete: "Walk me through using this." "What does that actually look like?"

**Know when to stop - then run the dimensions sweep.** When you understand what they're building, why, who it's for, and what done looks like, run a closing **implicit-requirement dimensions sweep** before offering to proceed:

- **Large / Complex:** Cover every dimension above - each must resolve to a requirement OR an explicit `N/A because [reason]`. No blank entries allowed.
- **Medium:** Cover only dimensions obviously present for this feature's domain; collapse the rest to a single `remaining dimensions N/A for this scope`.
- **Small:** Skip the sweep entirely.

The `N/A because...` escape is mandatory - it prevents inventing requirements to fill the checklist. Bound the sweep to THIS feature's scope; never add requirements outside the feature boundary.

### 2. Capture User Stories with Priorities

**P1 = MVP** (must ship), **P2** (should have), **P3** (nice to have)

Each story MUST be **independently testable** - you can implement and demo just that story.

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
````

- IDs: the criterion is `<CAT>-<NN>`; its Scenarios are `<CAT>-<NN>.S1`, `.S2`, ... Edge cases use the same format.
- Concrete values, one observable outcome through the public interface, behavior a caller cares about. A Scenario that says *how* ("calls the gateway client") is a future Implementation-Coupled Test; rewrite it as *what*.
- Where an implicit-requirement dimension applies (partial failure, rollback, retries, concurrency, external-dependency failure), at least one Scenario covers the failure mode.
- `validate_spec.py` rejects a criterion without an ID or without a Scenario, and a Scenario without Given/When/Then.

### 4. Requirement Closure Gate (before confirm)

Before presenting the spec for confirmation, run the three checks below. The spec is not presentable for confirmation until every item is resolved or assumption-logged - this is the guarantee that no requirement leaves the spec silently unclear.

**Scope-tiered:** Large/Complex = full gate; Medium = resolve obvious ambiguities, log the rest as assumptions; Small = skip entirely (consistent with skipping the sweep).

1. **Unambiguity + precision (hard).** Every AC must (a) have a single interpretation and (b) define a precise, spec-defined expected outcome. Any AC that fails either check: resolve with the user, split it, or log it as an explicit assumption with the chosen interpretation and rationale. No AC proceeds readable two ways or with an undefined outcome.

2. **Open-questions / assumptions closure.** Enumerate every unresolved decision that surfaced during clarification. Each must be either (a) resolved with the user OR (b) recorded as an **assumption** (chosen default + rationale) in the spec's Assumptions & Open Questions section. Nothing proceeds unmarked.

3. **Declined gray areas become assumptions.** Any gray area the user declined to discuss or that went undiscussed is written to the spec's Assumptions & Open Questions section (agent's chosen default + rationale) - never silently dropped. See [discuss.md](discuss.md).

Fix inline. This gate is bounded to THIS feature's stated dimensions and actual behavior - never to "anything imaginable." The Out of Scope table and anti-scope-creep rules remain the counterweights: the gate clarifies existing requirements, it never invents new ones.

**Deterministic backing (run before you present the spec).** The structural half of this gate is enforced by a script so it cannot drift when a step is forgotten: `python3 <skill-dir>/scripts/validate_spec.py <spec-path-or-feature>` checks that required sections exist, every AC is EARS-shaped (has a SHALL), no Assumptions row has an empty default or rationale, and requirement IDs are well-formed. A non-zero exit means fix before confirming. The script checks structure; you still own the judgment calls (is the interpretation right, is the outcome precise). If no code-execution tool is available, run the same checks by reading the spec.

---

## Template: `.specs/features/[feature]/spec.md` (Small scope)

Small changes still get a spec on disk so both reviewers can read it. No sweep, no closure gate, no traceability table.

````markdown
# [Feature Name] Specification

**Scope**: Small

## Problem Statement

[1-2 sentences.]

## Existing Capabilities

[Queries run (graphify / graph_queries.py / rg), what they found, and why this is not a Redundant Feature.]

## Standards

[Repo Standard sources and the rules that touch this change, or "none found - Smell Baseline only".]

## Acceptance Criteria

1. **[FEAT]-01**: WHEN [event] THEN the system SHALL [behavior]

   ```gherkin
   Scenario: [FEAT]-01.S1
     Given [state]
     When [trigger]
     Then [precise outcome]
   ```

## Steps

1. [Step] → files: [list] → verify: [Scenario IDs / gate] → commit: [message]
````

---

## Template: `.specs/features/[feature]/spec.md` (Medium, Large, Complex)

````markdown
# [Feature Name] Specification

**Scope**: Medium | Large | Complex

## Problem Statement

[Describe the problem in 2-3 sentences. What pain point are we solving? Why now?]

## Existing Capabilities

[Queries run (graphify / graph_queries.py / rg), what they found, and why this is not a Redundant Feature. Name what this feature will reuse.]

## Standards

[Repo Standard sources found, then one line per rule that touches this feature - or "none found - Smell Baseline only".]

## Goals

- [ ] [Primary goal with measurable outcome]
- [ ] [Secondary goal with measurable outcome]

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature     | Reason         |
| ----------- | -------------- |
| [Feature X] | [Why excluded] |
| [Feature Y] | [Why excluded] |

---

## Assumptions & Open Questions

Every ambiguity is resolved or recorded here - nothing is left silently unclear.

| Assumption / decision | Chosen default  | Rationale | Confirmed? |
| --------------------- | --------------- | --------- | ---------- |
| [ambiguity]           | [what we'll do] | [why]     | [y/n]      |

**Open questions:** none - all resolved or logged above (required before the spec is confirmed).

---

## User Stories

### P1: [Story Title] ⭐ MVP

**User Story**: As a [role], I want [capability] so that [benefit].

**Why P1**: [Why this is critical for MVP]

**Acceptance Criteria** (each is one EARS rule with an ID, followed by its Scenarios):

1. **[FEAT]-01**: WHEN [user action/event] THEN the system SHALL [expected behavior]

   ```gherkin
   Scenario: [FEAT]-01.S1 [short title]
     Given [concrete starting state]
     When [the trigger]
     Then [the precise expected outcome]
   ```

2. **[FEAT]-02**: IF [invalid input / failure] THEN the system SHALL [graceful handling]

   ```gherkin
   Scenario: [FEAT]-02.S1
     Given [state]
     When [failing trigger]
     Then [precise failure outcome]
   ```

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
````

---

## Tips

- **P1 = Vertical Slice** - A complete, demo-able feature, not just backend or frontend
- **EARS is code** - If you can't write a criterion as a test, rewrite it; pick the pattern (WHEN / WHILE / WHERE / IF / ubiquitous) that fits
- **Requirement IDs are mandatory** - Every story maps to trackable IDs
- **Edge cases matter** - What breaks? What's empty? What's huge?
- **Out of Scope prevents creep** - If it's not here, it doesn't get built
- **Closure gate before confirm** - Three checks: unambiguity + precision, open-questions/assumptions closure, declined gray areas logged; scope-tiered; bounded to stated dimensions; never invents requirements
- **Scenarios are the test contract** - every AC has an ID and at least one concrete Given/When/Then Scenario
- **Search before you specify** - `## Existing Capabilities` records the graph search; a Redundant Feature is raised before anything else
- **Present after the gate passes** - Present the spec only after the closure gate passes and `validate_spec.py` exits clean. The user's agreement here is provisional: it means "continue planning", never "build". Building waits for `/spec-review` and Execution Approval ([review.md](review.md))
