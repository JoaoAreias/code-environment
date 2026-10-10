# Spec-Driven Workflow

How a feature goes from request to accepted code: what gets specified, what gets reviewed before and after building, against what, and what each review produces.

## Language

**Change**:
The set of code differences under review, taken between a fixed base and the current head.
_Avoid_: PR, patch, diff

**Spec**:
The written statement of what a Change was meant to do: requirements with acceptance criteria, plus any recorded design, task plan and decisions, as produced by spec-driven development.
_Avoid_: issue, ticket, task, requirements doc

**Finding**:
One problem a reviewer raises about a Spec or a Change, with its evidence, stated fully enough that anyone can assess it later without the reviewer.
_Avoid_: issue, comment, gap

**Disposition**:
The human's recorded decision on one Finding: accept (the plan or code changes) or reject (with a reason). A Finding still being grilled has no Disposition yet.
_Avoid_: resolution, status, triage

**Spec Review**:
One assessment of a Spec by the Spec Reviewer, started by a human, producing Findings.
_Avoid_: plan review, spec validation

**Change Review**:
One assessment of a Change by the Change Reviewer, started by a human, producing Findings.
_Avoid_: code review (alone), PR review

**Execution Approval**:
The human's explicit go-ahead to execute planned work. For a new Spec it comes only after a Spec Review whose Findings all have Dispositions; for fixes, only after the Findings they address have Dispositions. Agreeing to a Spec, design or task plan along the way is provisional and never authorizes building, and neither does accepting a Finding.
_Avoid_: spec approval, sign-off

**Claim**:
A statement, made by whoever produced or checked a Change, that something about it is true: a task is done, a requirement is verified, tests pass, a decision was taken for a reason.
_Avoid_: report, summary

## Standards

**Repo Standard**:
A rule a codebase documents about how its code must be written. It always overrides the Smell Baseline.
_Avoid_: guideline, convention, style guide

**Smell Baseline**:
A fixed set of design smells checked in every codebase, each one a judgment call rather than a violation, suppressed where a Repo Standard endorses the pattern.
_Avoid_: lint rules, code smells (alone)

## Duplication

**Redundant Feature**:
A capability a Spec asks for that the codebase already provides.
_Avoid_: duplicate feature, existing feature

**Semantic Duplicate**:
Code in a Change that re-implements behavior existing code already provides, under different names or text.
_Avoid_: logic duplication, reinvented wheel

**Textual Duplicate**:
Code in a Change that is a copy or near-copy, token for token, of other code.
_Avoid_: copy-paste, clone

## Tests

**Acceptance Criterion**:
One rule in a Spec stating what the system shall do, written so it has a single reading and a precise expected outcome.
_Avoid_: requirement (alone), AC rule

**Scenario**:
One concrete Given/When/Then example of an Acceptance Criterion, identified within its Spec. Scenarios, not tests, are the contract a Change must honor.
_Avoid_: test case, example, user story

**Behavior Test**:
A test that proves exactly one Scenario through the code's public interface, and survives any refactor that keeps that Scenario true.
_Avoid_: good test, real test

**Unclaimed Test**:
A test that proves no Scenario. It carries no protection: it may be rewritten or removed when the code changes.
_Avoid_: orphan test, extra test

**Implementation-Coupled Test**:
A test that asserts how the code works (internal calls, private state, structure) instead of what it achieves, so it breaks on refactors that change no behavior.
_Avoid_: unit test (as a pejorative), brittle test, mock test

**Grandfathered Test**:
A test written before Scenarios existed that no Change has yet modified or broken. It keeps its protection until a Change touches it; then it must be claimed by a back-filled Scenario or treated as an Unclaimed Test.
_Avoid_: legacy test, old test

**Legacy Path**:
An older implementation kept alive beside its replacement only because some test still exercises it.
_Avoid_: dead code, old version, compat layer

## Learning

**Lesson**:
A one-sentence, project-local rule distilled from a grounded signal (a verification failure or a Finding's Disposition), trusted only once it recurs across distinct features. Author Lessons teach whoever plans and builds; Reviewer Lessons teach the reviewers what not to raise again.
_Avoid_: rule, learning, memory, tip

## Roles

**Verifier**:
The independent checker that confirms a Change honors its Spec's Scenarios and that its tests would catch regressions.
_Avoid_: validator, tester

**Spec Reviewer**:
The independent judge that assesses a Spec, with its design and plan, once planning ends and before anything is built: whether it asks for a Redundant Feature, whether the request itself is sound, and what production risk it carries.
_Avoid_: spec validator, planner

**Change Reviewer**:
The independent judge that runs after the Verifier and assesses a Change the way a staff engineer would: judgment, production risk, design fit, and whether the Claims about it hold.
_Avoid_: reviewer (alone), code-review skill, critic, auditor
