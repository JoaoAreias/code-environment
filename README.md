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
- removes installed copies of the skills this repo has retired (the names
  are in `RETIRED_SKILLS` at the top of `install.sh`). `~/.claude/skills/` is
  shared with other sources, so a folder is deleted only when it is not a
  symlink and its `SKILL.md` holds the text this repo shipped under that
  name. Anything else is left alone and reported as
  `skipped <name>: not installed by this repo`
- copies every `skills/<name>/` folder that has a `SKILL.md` into
  `~/.claude/skills/<name>/`
- renders `agents/*.md` (harness-neutral sources) through
  `render-adapters.js` into `~/.claude/agents/` (Claude Code; omp reads them
  too) and, when opencode is installed, into `~/.config/opencode/agents/`
- turns the human-only `spec-review` and `code-review` skills into opencode
  commands and denies opencode's model loading them as skills
  (`permission.skill` in `opencode.json`)
- installs graphify (`uv tool install graphifyy`) if it is missing
- warns when `fd` is not on PATH (it does not install it)
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
tests/                   unittest suite for the scripts and install.sh
CONTEXT.md               glossary for the spec-driven workflow
.specs/decisions/        Grilling Records: the Decisions behind it, with summary.md as index
.specs/features/         this repo's own specs, designs, tasks and review reports
docs/adr/                legacy decisions (0001-0003): still read, never written again
install.sh
```

Skills must sit exactly one level under `skills/` (`skills/<name>/SKILL.md`)
— that's what Claude Code, opencode and `omp` scan for.

`hooks/` must stay flat: `caveman-config.js` locates the caveman skill via
a relative path (`../skills/caveman/SKILL.md`), so `hooks/` and `skills/`
have to remain siblings.

## Spec-driven workflow and reviews

`spec-driven` is the only way an agent builds code here. Every Change, a
one-line bug fix included, goes through the same flow:

```
Specify (grill) → Design (Medium+) → Tasks + Tickets → /spec-review → Dispositions
  → ["publish tickets"] → Execution Approval → Execute (tdd) → Verifier → /code-review
```

1. **Specify is a grill.** The agent asks one question per turn, each with
   concrete options and a recommendation ("you decide" and "decide the rest"
   are the two shortcuts), and writes every question and answer into a
   Grilling Record as it goes. At shared understanding it writes `spec.md`:
   acceptance criteria with Gherkin Scenarios. Scenarios, not tests, are the
   contract. Before asking anything it searches the codebase with graphify
   for an existing equivalent and reads the Decisions and Repo Standards
   that bind the work.
2. **Design** is required at Medium scope and above. Its Decisions go into
   the feature's Grilling Record, and `design.md` links to them.
3. **Tasks and Tickets, at every scope.** `tasks.md` is always written. The
   Spec is sliced into Tickets of about one day each, demoable on their own,
   and each Ticket is cut into atomic Tasks, one commit per Task. A Small
   change gets one Ticket.
4. **The human runs `/spec-review`.** The `spec-reviewer` agent judges the
   finished plan before anything is built: Redundant Features, risky
   approaches, weak proposed tests, and whether the spec matches its
   Grilling Record.
5. **Dispositions.** The human accepts or rejects each Finding. An accepted
   Finding changes the plan, and a Decision it changes is rewritten in place
   in its record with a `Changed` line.
6. **"publish tickets" (optional).** On that explicit request, and only once
   the latest Spec Review's Findings all have Dispositions, the Tickets are
   published to the issue tracker that `setup-spec-driven` configured. Each
   tracker ID is written back into `tasks.md`, and a published Ticket is
   never created twice. Publishing does not start the build.
7. **Execution Approval.** Nothing is built until the human explicitly says
   to execute. Agreeing to a spec, a design or a task list along the way
   authorizes nothing.
8. **Execute runs the `tdd` loop per Task.** For each Scenario proven by a
   test: write the test, see it fail, then write the code that makes it
   pass. Each Task passes its gate and gets one atomic Conventional Commit.
9. **The Verifier runs automatically after the last Task.** It is a fresh
   agent, not the author. It checks every Scenario against the built Change
   and runs a discrimination sensor on the tests. A Scenario marked
   `**Proof**: inspect` (a prompt, configuration, infrastructure code) has no
   test: the Verifier reads the final files and records one PASS row with
   `file:line` evidence for it in `validation.md`. Gaps come back as Tasks in
   one fix Ticket per round.
10. **The human runs `/code-review`.** The `change-reviewer` agent judges
    the built Change like a staff engineer, with graphify and SonarQube
    evidence, and checks it against the active Decisions. The agent only
    says the review is available. It never starts it.

Only a human starts a review. Terms are defined in [CONTEXT.md](CONTEXT.md).

No other skill builds code. `diagnosing-bugs` ends at a confirmed root cause
and hands the repro, the root cause and the seam to a Small Specify.
`prototype` keeps the prototype on a throwaway branch and hands its verdict
to Specify. `/grill-with-docs` and `/improve-codebase-architecture` end with
a Grilling Record.

### Decisions live in `.specs/decisions/`

Every grilling session writes one Grilling Record,
`.specs/decisions/<slug>.md`: the context, every question with its options
and the answer, and the Decisions that came out of it, each with its choice,
reason and trade-off. `.specs/decisions/summary.md` is the index, one row
per finished record. A record is `draft` while its grill runs and `active`
once it is finished. Decision IDs look like `D-<slug>.3`.

A Decision that changes is rewritten in place with a `Changed` line; git
keeps the old text. Skills that need the Decisions (spec-driven's phases,
both reviewers, `tdd`, `diagnosing-bugs`, `improve-codebase-architecture`,
`domain-modeling`) all find them through one read rule,
[`skills/spec-driven/references/decisions.md`](skills/spec-driven/references/decisions.md).

Older decision logs are legacy decision sources. A `docs/adr/` folder, a
`## Decisions` section in `.specs/STATE.md` and a feature's `context.md` are
still read wherever they exist. They are never written again and are not
migrated. This repo's own [docs/adr/](docs/adr/) is one of them; the reasons
for the current flow are in
[`.specs/decisions/grill-in-spec-driven.md`](.specs/decisions/grill-in-spec-driven.md).

### Plans from older rules and other flows

| Kind | What it is | How it is treated |
|---|---|---|
| Native plan | `spec.md` has a `**Grilling Record**:` line | every structural check applies |
| Legacy plan | a spec-driven `spec.md` without that line | read, reviewed and built from as it is; the newer checks only warn; never rewritten to the new shape |
| Foreign plan | anything written outside spec-driven: a teammate's PRD, RFC or design doc, another tool's spec folder | read and reviewable with `/spec-review <path>` (the report goes to `.specs/reviews/<path slug>/`); never validated, never edited |

To build from a foreign plan, start Specify with it as input. Specify asks
only about its gaps and writes a native spec that links the source.

### Requirements

- `python3`, `node` and `git`.
- **graphify**, installed by `install.sh`. spec-driven and both reviewers
  search the code graph before anything is added. The graph cache is
  `graphify-out/` in each repo. It is often gitignored, and it is still
  never deleted or cleaned: refresh it with `graphify update .`.
- **`fd`** ([sharkdp/fd](https://github.com/sharkdp/fd)), which you install
  yourself. spec-driven lists each repo with it to find Decisions and other
  flows' plans, gitignored ones included. `install.sh` warns when it is
  missing, and Specify stops and asks for it.
- A configured SonarQube MCP server for `/code-review` (the review stops and
  says so when it is missing).

The repo's own tests run with `python3 -m unittest discover -s tests -v`.
They call the real graphify, not a stub.

## Skills

| Skill | What it does |
|---|---|
| `spec-driven` | The flow above: Specify, Design, Tasks, Execute and the Verifier, with their validator scripts |
| `spec-review`, `code-review` | Human-only commands that start the Spec Review and the Change Review |
| `grilling` | The interview rules: one question per turn, options, a recommendation, two shortcuts |
| `domain-modeling` | The formats for the glossary (`CONTEXT.md`), the Grilling Record and `summary.md` |
| `tdd` | The test-first loop Execute runs for each Task |
| `setup-spec-driven` | Per-repo setup: which issue tracker Tickets are published to, and where the domain docs live |
| `grill-with-docs` | A grill for something that is not a feature; writes a Grilling Record and the glossary |
| `improve-codebase-architecture` | Finds deepening opportunities, reports them as HTML, grills the one you pick into a Grilling Record |
| `codebase-design` | Shared vocabulary for deep modules, interfaces and seams |
| `diagnosing-bugs` | Diagnosis loop for hard bugs; hands the confirmed root cause to a Small Specify |
| `prototype` | Throwaway prototype that answers a design question; hands its verdict to Specify |
| `research` | Researches a question against primary sources and saves the findings as Markdown |
| `resolving-merge-conflicts` | Resolves an in-progress merge or rebase conflict |
| `caveman` | Compressed communication mode |
| `escrita-natural` | Natural Portuguese prose, without translationese or chatbot register |

Where they come from:

| Skill | Source |
|---|---|
| `codebase-design`, `diagnosing-bugs`, `domain-modeling`, `grill-with-docs`, `grilling`, `improve-codebase-architecture`, `prototype`, `research`, `resolving-merge-conflicts`, `setup-spec-driven`, `tdd` | Based on [mattpocock/skills](https://github.com/mattpocock/skills) (`skills/engineering`), MIT. They started as copies and have been changed to fit this workflow: Decisions go into Grilling Records, and every route to building code leads to spec-driven. |
| `spec-driven` | Adapted from Tech Leads Club — Spec-Driven Development v3.3.0 by Felipe Rodrigues ([felipfr](https://github.com/felipfr)), licensed [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/). Modified: renamed; Specify as a grill with Grilling Records; Tickets; Execution Approval; Gherkin Scenarios as the test contract with `test` and `inspect` proofs; graphify search; Repo Standards and smell baseline; review lessons; new scripts. |
| `spec-review`, `code-review` | This repo |
| `caveman` | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) — skill only, not the proxy |
| `escrita-natural` | [JoaoAreias/escrita-natural](https://github.com/JoaoAreias/escrita-natural) |

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
