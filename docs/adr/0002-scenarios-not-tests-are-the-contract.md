# Scenarios, not tests, are the contract

Upstream tlc-spec-driven says "tests are the spec: implementation conforms to tests", which protects every test, including Implementation-Coupled Tests. Agents then kept Legacy Paths alive just to keep those tests green. So each Acceptance Criterion (still written in EARS) now gets Gherkin Scenarios with IDs in the Spec. Each test carries its Scenario's ID and Given/When/Then text in a docstring. The Scenario is the contract, and the test is a disposable proof of it. An Unclaimed Test has no protection. A Grandfathered Test that a Change touches must be claimed by a back-filled Scenario or dropped.

## Considered Options

- Gherkin replacing EARS: rejected because invariants ("the system SHALL always…") read badly as examples.
- Gherkin written only on tests: rejected because the proposed tests would be invisible to the Spec Reviewer at planning time.
- `.feature` files with a BDD runner: rejected because it adds a stack-specific dependency, and its step-definition glue tends to become Implementation-Coupled itself.
- Scenario ID only on the test: rejected because a test read alone would no longer state the behavior it proves.

## Consequences

- `validate_spec.py` requires every Acceptance Criterion to have Scenarios.
- `validate_scenarios.py` cross-checks tests against Scenarios: missing tests, Unclaimed Tests, and drifted text.
- Removing a test is recorded as a Claim in the commit message, and the Change Reviewer audits it.
