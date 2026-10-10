# One harness-neutral source, generated per-harness adapters

These skills and agents run in opencode at work, Claude Code at home, and omp, across model providers. The harnesses disagree on agent locations and frontmatter, and on how to make a trigger human-only. opencode ignores `disable-model-invocation` and also loads `~/.claude/skills`. So the repo keeps one prompt body per agent with neutral metadata, and `install.sh` renders Claude Code agents (which omp also reads), opencode agents, opencode commands, and opencode skill-deny permissions from it. Mechanical logic lives in shared scripts such as `prep_review.py`, which every harness calls. Models are inherited from the session, never pinned.

## Considered Options

- Skills only, telling each harness to "spawn a subagent": rejected because tool limits are not enforced and opencode's model could start a review itself.
- Hand-maintained copies per harness: rejected because the copies drift.
- Claude-only features, such as resuming the reviewer subagent with `SendMessage` to grill a Finding: rejected, so grilling happens with the main agent instead.

## Consequences

- Generated files under `~/.claude/agents/` and `~/.config/opencode/` are never edited by hand. Edit the repo source and re-run `install.sh`.
