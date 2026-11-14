# old-demo Specification

**Scope**: Small

## Problem Statement

The demo skill does not state its export rule, so agents guess it.

## Existing Capabilities

Searched `export,rule`: no existing equivalent.

## Standards

none found - Smell Baseline only

## Decisions & Assumptions

none

## Acceptance Criteria

1. **DEMO-01**: The demo skill SHALL state the export rule in step 3.

   ```gherkin
   Scenario: DEMO-01.S1 rule is stated
     Given the demo skill
     When an agent reads step 3
     Then the rule is stated
   ```

   **Proof**: inspect

## Steps

1. Add the rule to step 3 of `skills/demo/SKILL.md`.
