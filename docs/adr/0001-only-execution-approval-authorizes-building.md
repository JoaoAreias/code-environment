# Only Execution Approval authorizes building

Upstream tlc-spec-driven treats approving a spec or task list as permission to implement. In practice, specs, designs and task lists get approved provisionally just to see the full plan, and they almost always change once everything is visible. So nothing is built until the human gives an explicit Execution Approval. For a new Spec, that requires a human-triggered Spec Review, run once planning ends, whose Findings all have Dispositions. For fixes, it requires Dispositions on the Findings they address.

## Considered Options

- Auto-dispatching the Spec Reviewer before Spec confirmation: earliest catch for Redundant Features, but it reviews without the design or task plan, and the agent rather than the human decides when to review.
- Agent-detected staleness forcing a re-review after plan edits: rejected. Only the human decides whether a plan change needs another Spec Review.
- Advisory Findings with no recorded Dispositions: rejected because nothing would stop a skimmed-past Blocker from reaching Execute.

## Consequences

- Small scope also writes a minimal `spec.md`, so every Change has a Spec to review.
- Review skills set `disable-model-invocation: true`, and opencode denies them through `permission.skill`, so no agent can start a review by itself.
- Execute reminds the human when no Spec Review exists for the feature. It never starts on a planning approval or on an accepted Finding.
