# Demo Specification

**Scope**: Large

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

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| rows fit in memory | yes, below 10,000 rows | the largest export so far has 800 rows | y |

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
