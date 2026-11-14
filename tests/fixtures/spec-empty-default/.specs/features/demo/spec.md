# Demo Specification

**Scope**: Large

**Grilling Record**: [`.specs/decisions/demo.md`](../../decisions/demo.md)

## Problem Statement

The demo skill does not state its export rule, so agents guess it.

## Existing Capabilities

Searched `export,rule`: no existing equivalent.

## Standards

none found - Smell Baseline only

## Out of Scope

| Feature | Reason |
| --- | --- |
| Email delivery | not requested |

## Decisions & Assumptions

| ID | Decision | Choice | Rationale | Decided by | Binds |
| --- | --- | --- | --- | --- | --- |
| D-demo.1 | Where the rule lives | step 3 of the demo skill | one place to read | user | feature |
| D-demo.2 | Rule wording | one imperative sentence | short rules get followed | agent | feature |

| Assumption | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| rows fit in memory |  | the largest export so far has 800 rows | y |

**Open questions:** none - all resolved or logged above.

## User Stories

### P1: The rule is stated

**User Story**: As an agent, I want the export rule written down, so that I follow it.

**Acceptance Criteria**:

1. **DEMO-01**: The demo skill SHALL state the export rule in step 3.

   ```gherkin
   Scenario: DEMO-01.S1 rule is stated
     Given the demo skill
     When an agent reads step 3
     Then the rule is stated
   ```

   **Proof**: inspect

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| DEMO-01 | P1: The rule is stated | Tasks | Pending |
