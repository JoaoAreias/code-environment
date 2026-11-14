# Demo Tasks

**Spec**: `.specs/features/demo/spec.md`
**Status**: Draft

## Test Coverage Matrix

| Layer | Example paths | Test type | Proof type | Coverage Expectation | Proven by |
| --- | --- | --- | --- | --- | --- |
| Skill prose | `skills/demo/SKILL.md` | inspect | inspect | every `inspect` Scenario checked once by the Verifier | one row per Scenario in `validation.md` |

## Gate Check Commands

| Gate | Command | Used by |
| --- | --- | --- |
| build | `true` | every task |

## Execution Plan

### Phase 1: K1 The rule is stated

```
T1 → T2
```

## Task Breakdown

### Phase 1: K1 The rule is stated

#### T1: State the export rule

**What**: add the rule to step 3.
**Where**: `skills/demo/SKILL.md`
**Depends on**: None
**Requirement**: DEMO-01

**Tests**: inspect
**Scenarios**: DEMO-01.S1
**Gate**: build

#### T2: Mention the rule in the README

**What**: one line pointing at step 3.
**Where**: `README.md`
**Depends on**: T1
**Requirement**: none (documentation)

**Tests**: none (documentation)
**Scenarios**: none - this task writes no tests
**Gate**: build
