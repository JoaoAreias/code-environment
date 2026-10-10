# code-environment

Personal Claude Code skills, agents and hooks, kept here as the source of
truth and pushed into `~/.claude/` (and `~/.config/opencode/`) with
`install.sh`.

## Install / upgrade

```bash
git pull
./install.sh
```

Safe to re-run: skill, agent and hook files are always overwritten with the
repo's copy; `settings.json` and `opencode.json` entries are only added if
missing (never duplicated).

`install.sh`:
- removes retired skills (`tlc-spec-driven`, now `spec-driven`) from
  `~/.claude/skills/`
- copies every `skills/<name>/` folder that has a `SKILL.md` into
  `~/.claude/skills/<name>/`
- renders `agents/*.md` (harness-neutral sources) through
  `render-adapters.js` into `~/.claude/agents/` (Claude Code; omp reads them
  too) and, when opencode is installed, into `~/.config/opencode/agents/`
- turns the human-only `spec-review` and `code-review` skills into opencode
  commands and denies opencode's model loading them as skills
  (`permission.skill` in `opencode.json`)
- installs graphify (`uv tool install graphifyy`) if it is missing
- copies every file in `hooks/` into `~/.claude/hooks/`
- adds caveman's `SessionStart`/`UserPromptSubmit` hooks and `statusLine`
  to `~/.claude/settings.json` (backing it up once, on first run, to
  `settings.json.bak`)

`CLAUDE_CONFIG_DIR` and `OPENCODE_CONFIG_DIR` override the target
directories. Edit the repo sources, never the rendered files.

## Layout

```
skills/<name>/SKILL.md   one skill per folder, one level deep
agents/<name>.md         harness-neutral agent sources (rendered by install.sh)
hooks/                   caveman's hook scripts (flat — see below)
render-adapters.js       per-harness rendering of agents and commands
CONTEXT.md               glossary for the spec-driven workflow
docs/adr/                decisions behind it
install.sh
```

Skills must sit exactly one level under `skills/` (`skills/<name>/SKILL.md`)
— that's what Claude Code, opencode and `omp` scan for.

`hooks/` must stay flat: `caveman-config.js` locates the caveman skill via
a relative path (`../skills/caveman/SKILL.md`), so `hooks/` and `skills/`
have to remain siblings.

## Spec-driven workflow and reviews

```
Specify → Design* → Tasks* → /spec-review → Execution Approval → Execute → Verifier → /code-review
```

- `spec-driven` plans and builds features. Acceptance criteria carry Gherkin
  Scenarios, and Scenarios, not tests, are the contract. It searches the
  codebase with graphify before adding anything, and applies Repo Standards
  plus a smell baseline.
- `/spec-review` runs the `spec-reviewer` agent on the finished plan, before
  anything is built (Redundant Features, risky approaches, weak proposed tests).
- `/code-review` runs the `change-reviewer` agent on the built Change after the
  Verifier passed, with graphify and SonarQube evidence.
- Only a human starts a review, and nothing is built without an explicit go
  after the Spec Review's Findings have Dispositions. Terms are defined in
  [CONTEXT.md](CONTEXT.md); the reasons are in [docs/adr/](docs/adr/).

Requirements: `python3`, `node`, `git`, graphify (installed by `install.sh`),
and a configured SonarQube MCP server for `/code-review` (the review stops
and says so when it is missing).

## Skills

| Skill | Source |
|---|---|
| `ask-matt`, `codebase-design`, `diagnosing-bugs`, `domain-modeling`, `grill-with-docs`, `implement`, `improve-codebase-architecture`, `prototype`, `research`, `resolving-merge-conflicts`, `setup-matt-pocock-skills`, `tdd`, `to-spec`, `to-tickets`, `triage`, `wayfinder`, `wizard` | [mattpocock/skills](https://github.com/mattpocock/skills), `skills/engineering` |
| `caveman` | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) — skill only, not the proxy |
| `spec-driven` | Adapted from Tech Leads Club — Spec-Driven Development v3.3.0 by Felipe Rodrigues ([felipfr](https://github.com/felipfr)), licensed [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/). Modified: renamed; Execution Approval; Gherkin Scenarios as the test contract; graphify search; Repo Standards and smell baseline; review lessons; new scripts. |
| `spec-review`, `code-review` | This repo (the old mattpocock `code-review` was replaced) |
| `escrita-natural` | [JoaoAreias/escrita-natural](https://github.com/JoaoAreias/escrita-natural) |

`engineering-README.md` is the original category doc from mattpocock/skills
— reference only, not a skill itself.

## Agents

| Agent | Started by | Job |
|---|---|---|
| `spec-reviewer` | `/spec-review` | Judges a finished plan before build; writes `spec-review-N.md` |
| `change-reviewer` | `/code-review` | Judges a built Change after the Verifier; writes `change-review-N.md` |

## Notes

- Caveman's hooks (`caveman-activate.js`, `caveman-mode-tracker.js`,
  `caveman-statusline.sh`) speak Claude Code's own hook protocol — they
  don't run under `omp`. The `caveman` skill itself works in both via
  shared `SKILL.md` discovery.
- Only the caveman "small rock" skill is installed here, not its BSL-1.1
  proxy component.
- Agents never pin a model: they inherit the session's model in every harness.
