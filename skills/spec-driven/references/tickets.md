# Tickets

**Goal**: slice a Spec's work into day-sized **Tickets** the product team can follow, add fix Tickets when a review or the Verifier finds problems, and publish Tickets to the issue tracker safely when the user asks.

A **Ticket** is a slice of a Spec's planned work sized to about one day, demoable on its own. It is made of **Tasks** and names the Tickets that block it. Tickets are written in the `## Tickets` section of `.specs/features/[feature]/tasks.md` by the Tasks phase ([tasks.md](tasks.md)); that file is their source of truth. An issue on the tracker is a published copy of a Ticket, never the other way round.

This file has three parts:

1. [Slicing](#1-slicing-a-spec-into-tickets): how the Tasks phase cuts a Spec into Tickets.
2. [Fix Tickets](#2-fix-tickets): what happens when a Verifier round or a Change Review produces fix tasks.
3. [Publishing](#3-publishing-tickets): creating tracker issues, only on the user's explicit "publish tickets".

`<skill-dir>` below is the `spec-driven` skill directory.

---

## 1. Slicing a Spec into Tickets

Slice top-down: the Spec into Tickets first, then each Ticket into atomic Tasks. Use the terms of the project's glossary (`CONTEXT.md`) in titles and descriptions, and respect the Decisions the read rule found ([decisions.md](decisions.md)).

### One-day vertical slices

- **About one day each.** A Ticket is roughly one day of work for whoever builds it. If it looks like several days, split it. If it is a few minutes of work, merge it into a neighbouring Ticket. A Ticket that needs more than about ten Tasks is too big.
- **Vertical, not horizontal.** Each Ticket cuts a narrow but COMPLETE path through every layer it needs (schema, API, UI, tests). "All the database changes" or "write the tests" is a horizontal slice of one layer and is not a Ticket.
- **Demoable on its own.** When a Ticket is finished, someone can see or verify what it delivers without waiting for a later Ticket. If you cannot say what would be shown in a demo, the slice is wrong.
- **Prefactoring first.** When the code has to be reshaped before the change is easy ("make the change easy, then make the easy change"), that reshaping is its own earliest Ticket, and the Tickets that need it are blocked by it.
- **Blocked-by edges.** Each Ticket names the Tickets that must be finished before it can start. A Ticket with no blockers says `none`. Edges point only to Tickets listed earlier in the section, so the listing order is always a valid order to build and to publish in.
- **Complete cover.** Every acceptance criterion and every Scenario of the Spec is covered by a Ticket, and every Task belongs to exactly one Ticket.
- **Every scope gets Tickets.** A Small feature is less than a day of work: it gets exactly one Ticket, `K1`, that lists every Task.

### Wide refactors: expand-contract

A **wide refactor** is the one exception to vertical slicing. It is one mechanical change (rename a column, retype a shared symbol) whose blast radius fans across the whole codebase, so a single edit breaks call sites everywhere at once and no vertical slice can land green. Do not force it into a vertical slice. Sequence it as **expand-contract** Tickets:

1. **Expand**: one Ticket adds the new form beside the old one, so nothing breaks.
2. **Migrate**: the call sites move over in batches sized by blast radius (per package, per directory). Each batch is its own Ticket, blocked by the expand Ticket. The build stays green from batch to batch because the old form still exists.
3. **Contract**: a last Ticket deletes the old form once no caller remains. It is blocked by every migrate Ticket.

When even the batches cannot stay green alone, keep the same sequence but let the migrate Tickets share an integration branch, and add a final integrate-and-verify Ticket that all of them block. Green is promised only at that Ticket; say so in its `Delivers` line.

### What a Ticket holds

The markup is fixed, because `validate_tasks.py` parses it ([tasks.md](tasks.md) step 5 and template):

```markdown
## Tickets

### K1: <title: the deliverable, in the user's terms>
**Delivers**: <what works for the user once this Ticket is done>
**Covers**: <acceptance criterion IDs> · <Scenario IDs>
**Blocked by**: none | K<n> (earlier Tickets only)
**Tasks**: T1, T2, T3
**Tracker**: <issue ID - written by publishing, never by hand>
```

- The heading is `### K<n>: <title>`. Tickets are numbered `K1`, `K2`, ... in listing order and never renumbered.
- **Delivers** describes the end-to-end behaviour from the user's or the product team's view, not a layer-by-layer implementation list.
- **Covers** names the criteria and Scenarios this Ticket delivers.
- **Tasks** lists the Task IDs that make up the Ticket. Each Ticket is one Execution Plan phase.
- **Tracker** exists only on a published Ticket. A Ticket without a `**Tracker**` line is unpublished.

---

## 2. Fix Tickets

Work found after the plan was built never goes back into a finished Ticket. Each round that produces fix tasks adds **one fix Ticket for that round**:

- **A Verifier round** that reports gaps: the gaps become fix tasks, and all of them go into one new Ticket named after the round, for example `### K3: Fix Verifier round 1`.
- **A Change Review** whose accepted Findings become fix tasks: all of them go into one new Ticket named after the review, for example `### K4: Fix CR1`.

One round, one Ticket: two Verifier rounds give two fix Tickets, and a Change Review gives its own. A fix Ticket is an ordinary Ticket with the same fields:

```markdown
### K4: Fix CR1
**Delivers**: fixes for CR1-F1 (null total) and CR1-F2 (wrong rounding)
**Covers**: CSV-02.S1, CSV-04.S2
**Blocked by**: K2
**Tasks**: T9, T10
```

- **Append it** at the end of the `## Tickets` section with the next free `K` number. Existing Tickets keep their numbers, their Task lists and their Tracker IDs.
- **Blocked by** names the Tickets it repairs, which are always earlier ones.
- **Covers** names the Scenarios it repairs.
- **Tasks** lists every fix task of that round. Each fix task is appended to the Task Breakdown in the usual shape and carries a `**Fixes**` field naming what it fixes (`**Fixes**: CR1-F1`, or the Verifier gap). Every fix task is listed in its fix Ticket, so `validate_tasks.py` still finds every Task in exactly one Ticket.
- **Add a phase** for it to the Execution Plan, after the existing phases.
- A shipped Ticket stays closed. Do not reopen it or add Tasks to it.
- A fix Ticket is published like any other Ticket: only on "publish tickets", under the rules below.

---

## 3. Publishing Tickets

Publishing creates one issue on the team's tracker for each Ticket. It writes outside the repository, where the product team sees it, so it follows four rules without exception. They exist so that the user decides when the team sees the work, and so that running the command twice, or after a failure, never produces a duplicate issue.

### Only on an explicit "publish tickets"

Publish only when the user explicitly says "publish tickets" (or words that plainly mean it). Never publish on your own initiative, never as a step of Tasks, Execute or a review, and never because the plan "is ready". Do not offer to publish at the end of another phase.

Publishing is independent of Execution Approval. "Publish tickets" does not authorize building, and Execution Approval does not authorize publishing. The user may publish before deciding to build, after it, or never.

### Rule 1: a Spec Review with every Disposition comes first

Before creating anything, check the feature folder `.specs/features/[feature]/`:

1. **At least one Spec Review exists.** Look for `spec-review-<n>.md`. If there is none, **refuse**: create no tracker issue, and tell the user that a Spec Review must run first (the human runs `/spec-review [feature]`; you never run it yourself) and that its Findings need Dispositions before Tickets can be published.
2. **Every Finding of the latest Spec Review has a Disposition.** Open the report with the highest `<n>` and read each Finding's `**Disposition**` line. A line that still reads `(pending)` or `_(pending)_`, is empty, or is missing means the Finding has no Disposition. If any Finding has none, **refuse**: create no tracker issue, and list every pending Finding by its ID (for example "SR1-F3 is still pending") so the user can decide them ([review.md](review.md)).

When you refuse, say why in one or two sentences and stop. Do not publish a part of the Tickets, and do not record Dispositions on the user's behalf to get past the check.

### Before the first issue

- **Find the tracker.** Read `docs/agents/issue-tracker.md`. The `setup-spec-driven` skill writes it; it says which tracker this repository uses (GitHub through `gh`, GitLab through `glab`, local markdown files, or a workflow the user described) and the commands for it. If the file does not exist, stop and ask the user to run `/setup-spec-driven` first. Do not guess a tracker.
- **Read the Tickets** from the `## Tickets` section of `tasks.md` and run `python3 <skill-dir>/scripts/validate_tasks.py [feature]`. Do not publish from a `tasks.md` that fails it.
- **Sort them into published and unpublished.** A Ticket with a `**Tracker**` line is published. A Ticket without one is unpublished. Tell the user which Tickets you are about to create before you create the first one.

### Rule 2: dependency order, and the ID is written back right after each issue

Create **one issue per unpublished Ticket**, in the order the Tickets are listed (blockers first), one at a time:

1. Create the issue for the Ticket.
2. **Immediately** write its ID into that Ticket in `tasks.md`, as a `**Tracker**: <issue ID>` line under the Ticket's `**Tasks**` line. Save the file before you do anything else.
3. Only then move to the next Ticket.

Never create several issues and write the IDs back afterwards: if the session stopped in between, nobody could tell which Tickets already have an issue. Because blockers are created first, each issue can reference the real IDs of the issues that block it.

Example: `tasks.md` has `K1` and `K2`, with `K2` blocked by `K1`, and neither is published. The tracker gets one issue for `K1` and then one for `K2`; after the run both `K1` and `K2` in `tasks.md` carry a `**Tracker**` line naming their issue ID.

When the run ends, successfully or not, commit `tasks.md` (and the issue files of a local tracker) locally in one commit, for example `docs(tasks): record tracker IDs for [feature]`, so the IDs are not lost. Do not push.

### Rule 3: a published Ticket is never created again

A Ticket that already has a Tracker ID is **skipped**. Never create a second issue for it, whatever changed and however many times the user says "publish tickets". Its `**Tracker**` line is left exactly as it is.

Example: `K1` names tracker issue 41 and `K2` names none. "Publish tickets" creates exactly one new issue, for `K2`. `K1` still names issue 41.

**Drift.** A published Ticket may have changed in `tasks.md` since its issue was created (a new title, a different `Delivers`, more Scenarios, other blockers). For each published Ticket, compare its current text with its issue. Where they differ, **list the drift** to the user, Ticket by Ticket, saying what changed. Update an existing issue only when the user gives a go-ahead for it, and then edit that issue in place; never close it and open a new one. Without a go-ahead the issue stays as it is.

If a create call ended without a clear answer (a timeout, a dropped connection), do not create again blindly: first look on the tracker for an issue with that Ticket's title. If it exists, write its ID back and carry on; if it does not, treat it as a failure (Rule 4).

Touch only the issues this workflow created. Do not close, relabel or edit any other issue.

### Rule 4: stop at the first failure, resume on the next "publish tickets"

When the tracker rejects a call or the command fails:

1. **Stop.** Create no further issue in this run. Do not skip the failed Ticket and continue with the next one, and do not retry in a loop.
2. **Keep what was written.** The Tracker IDs already in `tasks.md` stay. Do not delete the issues that were created.
3. **Report** which Tickets were published, each with its issue ID, and which were not, naming the Ticket that failed and the error the tracker gave.

The next time the user says "publish tickets", the same procedure runs again. Rule 3 skips every Ticket that has a Tracker ID, so the run resumes at the first unpublished Ticket and creates only what is still missing.

Example: `K1`, `K2` and `K3` are unpublished. The tracker accepts `K1` and `K2` and then rejects `K3`. Afterwards `K1` and `K2` in `tasks.md` name their issue IDs and `K3` names none; you report `K3` as not published, with the error, and stop. When the user says "publish tickets" again, only `K3` is created.

### What an issue says

Every issue is a published copy of one Ticket:

- **It links to its Spec.** Give the Spec's path, `.specs/features/[feature]/spec.md`, as a link where the tracker can render one, and name the Ticket (`K2`) and the feature.
- **It says the work is built through the Spec.** Include this sentence, or one that says the same: "This Ticket is built through the spec-driven workflow from the linked Spec. It is here so the team can follow the work; it is not a standalone work order." No issue may read as an invitation to build straight from the tracker.
- **It carries no label that invites an agent to pick it up.** Do not apply any "ready for agent" style label or any other triage label, do not write a status that says so, and do not describe the issue as something an agent can grab. The older ticket flow applied such a label; this one never does. Apply a label only when the user names one.
- **It describes behaviour, not files.** Avoid file paths and code snippets in the body, apart from the link to the Spec: they go stale fast.

Issue body:

```markdown
## What it delivers

<The Ticket's Delivers line: the end-to-end behaviour, from the user's perspective.>

## Spec

Ticket K<n> of feature `<feature>`: [spec.md](<link or path to .specs/features/<feature>/spec.md>)

This Ticket is built through the spec-driven workflow from the linked Spec. It is here so the team can follow the work; it is not a standalone work order.

## Covers

- <criterion ID>: <the criterion in one line>
- <Scenario ID>: <the Scenario's title>

## Blocked by

- <the issue ID of each blocking Ticket, or "None (can start immediately)">
```

The issue title is the Ticket's title, prefixed with its ID (`K2: Export orders as CSV`).

### The shape per tracker

The Tickets are the same on every tracker. Only the command and the shape of the blocking edges change. `docs/agents/issue-tracker.md` has the exact commands; in short:

| Tracker | Create an issue | The Tracker ID | Blocking edges |
| --- | --- | --- | --- |
| **GitHub** | `gh issue create --title "..." --body "..."` | the issue number, written as `#41` | the tracker's native blocking or sub-issue relationship where it has one; otherwise the `## Blocked by` section lists the blocking issues' numbers |
| **GitLab** | `glab issue create --title "..." --description "..."` | the issue number, written as `#41` | the same: a native relationship where there is one, otherwise the `## Blocked by` section |
| **Local markdown** | write one file per Ticket, `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order; never one combined file | the file's path from the repository root | a `Blocked by:` line near the top naming the blocking issues' IDs |
| **Other** (Jira, Linear, ...) | follow the workflow described in `docs/agents/issue-tracker.md` | whatever identifier that tracker returns | its native blocking link where it has one, otherwise the `## Blocked by` section |

A local-markdown issue file starts like this and then continues with the issue body above:

```markdown
# <NN>: <Ticket title>

Status: open
Blocked by: <IDs of the blocking issue files, or "None (can start immediately)">
```

The Spec itself is never copied into the tracker or into `.scratch/`; the issue links to it.

---

## Tips

- **Tickets first, Tasks second** - a Ticket is a day-sized, demoable slice; a Task is one commit inside it
- **Wide refactor? Expand, migrate in batches, contract** - never one giant Ticket
- **One fix Ticket per round** - a Verifier round or a Change Review each gets its own; finished Tickets stay closed
- **"Publish tickets" is the only trigger** - and only after a Spec Review whose Findings all have Dispositions
- **Write the ID back before the next issue** - it is what makes a retry safe
- **A Ticket with a Tracker ID is never created again** - list drift, update on a go-ahead
- **Stop at the first tracker failure** - report what was and was not published; the next "publish tickets" resumes
