# Decisions: discovery and the read rule

One rule for finding the Decisions and plans that bind the work you are about to do. Everyone who plans, builds or judges follows it before doing anything else: Specify, Design, Tasks, Execute, the Verifier, the Spec Reviewer and the Change Reviewer, and the skills `tdd`, `diagnosing-bugs`, `improve-codebase-architecture` and `domain-modeling`. Each of them is a **consumer** below.

A **Decision** is a choice made while planning. It lives in a **Grilling Record** under `.specs/decisions/`, indexed by `.specs/decisions/summary.md`. This file says how to *find and read* Decisions. How to *write* a Grilling Record or `summary.md` is defined by the `domain-modeling` skill (`GRILLING-RECORD-FORMAT.md`), not here.

Run the steps in order, every time you start. They are cheap, and nothing stores their result, because a stored list goes stale the day a teammate adds a folder.

---

## 0. Discovery: list the repository

Teammates may plan with other tools, and their material may be gitignored. Two general listings show it without walking dependency trees:

```sh
fd -H --no-ignore-vcs -t d --max-depth 3 -E .git -E node_modules -E .venv -E venv
fd -H --no-ignore-vcs -t f --max-depth 1
```

The first lists directories three levels deep, the second lists the files at the root. `--no-ignore-vcs` shows gitignored paths but still honors `.ignore` and `.fdignore`, so a team can tune the listing without editing this skill.

Read both listings yourself and judge what is relevant. Do not filter them by name: a name filter only finds the flows you already know. You are looking for:

- this workflow's own material: `.specs/`, `CONTEXT.md`, `CONTEXT-MAP.md`;
- legacy decision sources (section 3);
- **planning or decision material from other flows**: another tool's spec folder, RFCs, PRDs, design documents, decision logs, agent rule files. Folders such as `.kiro/`, `openspec/`, `docs/rfcs/` or `docs/design/` are examples, not a list to match against.

Where a directory looks like such material, drill into it (`fd . <dir>`, then read the files that bear on your work).

Then **name what you found**. Before your first question or first action, tell the user which planning or decision material from other flows bears on the work, by path (for example "`.kiro/specs/payments/` and `docs/rfcs/` cover payments"). Material that does not bear on the work is not mentioned. When nothing was found, say nothing.

**Cite the outside sources you use.** Specify and Design write every outside source they actually used into the Context section of the Grilling Record, by path with its commit or date. That citation is the only lasting trace of discovery.

**When `fd` is missing, stop and ask.** If `fd` is not on PATH (`command -v fd` fails), your first message asks the user to install `fd` (https://github.com/sharkdp/fd) and says why: without it the listing would miss gitignored material or drown in dependency folders. Ask no planning question and do no other work until `fd` is available. Do not substitute `find`, `ls -R` or `git ls-files`.

---

## 1. Read `summary.md` and open the records that apply

If `.specs/decisions/summary.md` exists, read it. It has one row per finished Grilling Record:

```
| File | Date | Summary | Status | Binds | Areas | Specs |
```

Open **exactly** the records whose row has Status `active` and meets at least one of these:

1. **It binds the project where you work**: Binds is `project`, and Areas is `*` or overlaps the paths you are touching. An Area overlaps a path when one contains the other: Area `src/billing/` overlaps `src/billing/invoice.py`, and Area `src/billing/retry/` overlaps a change to all of `src/billing/`.
2. **It belongs to your feature**: Specs names the feature you are working on. (A consumer with no feature, such as a bug diagnosis, skips this test.)

Do not open the other records. A row that binds only its own feature (Binds `feature`) and names a different feature in Specs is not yours to read, even when its Areas overlap your paths.

**Skip `draft` records.** A record's Status is `draft` while its grill is still running and `active` once it is finished. No other status exists. A draft has no row in `summary.md`, and its Decisions are not settled yet, so a consumer never reads it as binding. The one exception is Specify resuming its own feature's draft ([specify.md](specify.md)).

Worked example. `summary.md` has `billing-rules.md` (project, Areas `src/billing/`, active), `money.md` (project, Areas `*`, active) and `dark-mode.md` (feature, Areas `src/ui/`, active, Specs `dark-mode`). The folder also holds `billing-ledger.md`, a draft with Areas `src/billing/` and no row. A Task touching `src/billing/invoice.py` for feature `invoice-pdf` opens `billing-rules.md` and `money.md`. It does not open `dark-mode.md` (another feature's own Decisions) or `billing-ledger.md` (a draft).

**What the opened Decisions mean.** Every Decision in an opened record that binds the project is a **Repo Standard** ([standards.md](standards.md) section 1): follow it. A Decision always shows its current choice; a `Changed` line under it says when and why it was rewritten. If your work has to contradict an active Decision, stop and surface the conflict by Decision ID. Never work around it silently. Only the user changes a Decision, and a changed Decision is rewritten in the record that holds it.

---

## 2. When the index is broken, fall back to the headers

`summary.md` is an index kept by hand; each record's header is the source of truth. A bad merge must not block anyone or hide a record. After reading `summary.md`, list the folder (`fd -t f -e md . .specs/decisions`) and compare it with the table. The index is broken when any of these is true:

- a row cannot be parsed (wrong number of cells, an empty File or Status cell);
- a row names a file that does not exist;
- a record with `Status: active` in its header has no row. (A record with `Status: draft` and no row is normal.)

Then:

1. **Warn and name the problem**, one line per problem, for example "`summary.md` names `gone.md`, which does not exist" and "`billing-rules.md` is active but has no row in `summary.md`".
2. **Decide from the headers instead.** Read the header of every `.specs/decisions/*.md` except `summary.md` (the `Status`, `Binds`, `Areas` and `Specs` lines at the top) and apply the filter of section 1 to those headers: open the `active` records that bind the project with overlapping Areas or `*`, or that name your feature; skip `draft` records.
3. Carry on with the work. Do not repair `summary.md` unless you are the session that writes records (Specify, Design, a grill); a reviewer or the Verifier only reports the problem.

When `.specs/decisions/` holds records but no `summary.md` at all, treat it the same way: warn, and decide from the headers.

---

## 3. Legacy decision sources

Decisions recorded before Grilling Records existed stay where they are. They are read, never migrated and never written to again. Check every source below that exists, **with or without `summary.md`**; the `## Legacy decision sources` lines in `summary.md` are a reminder, not the list.

| Source | Where | What to read |
| --- | --- | --- |
| Root ADRs | `docs/adr/` at the repository root | the files that touch the area you work in; they apply system-wide |
| Per-context ADRs | each context's `docs/adr/` | the files of every context your paths fall under |
| Old decision log | `.specs/STATE.md`, section `## Decisions` | the `AD-NNN` entries that touch your area |
| Feature context | `.specs/features/<feature>/context.md` | the whole file, whenever it exists for the feature you work on |

**Finding per-context `docs/adr/` directories.** If `CONTEXT-MAP.md` exists at the root, it lists the contexts: check `<context>/docs/adr/` for each context your paths fall under. If there is no map, discovery's three levels may be too shallow, so probe for every such directory:

```sh
fd -t d -p 'docs/adr$' -E .git -E node_modules -E .venv -E venv
```

Read the ADRs of each directory the probe finds that sits above the paths you touch (`src/billing/docs/adr/` governs `src/billing/total.py`), plus the root one.

**A feature's `context.md`** holds decisions the user locked under older rules. Read it whenever the file exists, whatever kind of plan the feature has (below). spec-driven no longer writes this file.

An active legacy decision that sets a rule for the code counts as a Repo Standard, exactly like a project-binding Decision. Surface a conflict with it the same way, by file name or `AD-NNN`.

---

## 4. Three kinds of plan

How much of the workflow applies to a plan depends on who wrote it and when.

| Kind | How to tell | How it is treated |
| --- | --- | --- |
| **Native plan** | `.specs/features/<feature>/spec.md` has a `**Grilling Record**:` line | every structural check applies |
| **Legacy plan** | `.specs/features/<feature>/spec.md` has no `**Grilling Record**:` line | still read, reviewed and built from; the newer checks (the `Decisions & Assumptions` section, Tickets) only warn |
| **Foreign plan** | anything else: a teammate's PRD, a design document, an RFC, another tool's spec folder, a ticket | read as a source of requirements and decisions; never structurally validated, never edited |

- **The `**Grilling Record**:` line alone separates native from legacy.** Nothing else decides it: not the presence of a `context.md`, not a row in `summary.md`, not the date. A native spec that loses the line is checked as legacy.
- A legacy plan is not rewritten to the new shape. Work on it as it is, and read its `context.md` and the other legacy sources.
- A foreign plan belongs to its author. Do not edit it, reformat it, or run `validate_spec.py` or `validate_tasks.py` on it. A foreign plan in a folder is one plan made of every markdown file in that folder.
- Discovery (section 0) is how foreign plans are found; a record's Context names the ones that were used.
- To **review** a foreign plan, the human runs `/spec-review <path>`; the report goes under `.specs/reviews/<path slug>/` and the plan stays untouched ([review.md](review.md)).
- To **build** from a foreign plan, start with Specify: it takes the plan as input, asks only about its gaps, and writes a native spec that links the source ([specify.md](specify.md)). spec-driven never executes a foreign plan directly.

---

## 5. The Binds test

Every Decision says what it binds, and that decides who has to read it.

- **`project`**: a future feature has to follow this Decision or knowingly change it. Examples: "money is stored as integer cents", "exports are always downloaded, never emailed".
- **`feature`**: the Decision matters only inside the feature that made it. Example: "the export button sits right of the filter bar".

Ask one question: *if someone built the next feature without knowing this, could they break it or contradict it?* If yes, it binds the project. There is no other test: reversibility, surprise and size do not matter, because every Decision is recorded either way.

A record's header and its `summary.md` row say `project` as soon as one of its Decisions binds the project. The agent proposes Binds inside each recommendation during a grill, and the user can correct it.
