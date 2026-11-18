# Grilling Record Format

A **Grilling Record** is the complete written account of one grilling session: the context, every question asked with its options and answer, the Decisions the session produced and their consequences. Records live in `.specs/decisions/`, one file per session, next to `summary.md`, the index of that folder.

A record covers the whole session, not one decision. A reader who was not there must be able to see what was asked, what was offered, what was rejected and why. **A record shorter than its session is wrong.** No script checks this: the wording below is the only guard, and the Spec Reviewer raises a Finding against a thin record.

Create `.specs/decisions/` lazily, when the first record is written.

## File name and Decision IDs

- The file is `.specs/decisions/<slug>.md`. The slug is 2 to 4 lowercase words joined by hyphens that name the subject, for example `csv-export` or `billing-events`. A feature's record normally uses the feature's name.
- The slug must be unique in `.specs/decisions/`. List the folder before creating the file. If `<slug>.md` already exists and belongs to another session, pick a different slug (for example `csv-export-orders`) and leave the existing file untouched. Two branches that pick the same slug then collide as a visible git conflict; different slugs never clash.
- Every Decision has an ID `D-<slug>.k`, where `k` counts from 1 through the whole file: the grill's Decisions first, then the ones Design adds, then the ones reviews add. The same ID is used in the record, `spec.md`, `design.md` and review reports. IDs are never reused or renumbered.

## Record template

Every section below is required in every record. `## Design` and `## Review` are added to a feature's record when those phases produce Decisions; the other five sections are never left out, never merged and never left empty in a finished record.

````md
# <slug> · <title that states what the session was about>

- **Date**: <YYYY-MM-DD the session started> (add `to <YYYY-MM-DD>` when it ran over several days)
- **Started from**: <the skill or command, the harness, the branch>
- **Specs**: <feature name(s) whose spec links this record, or `none`>
- **Binds**: <`project` when any Decision below binds the project, else `feature`>
- **Areas**: <the code paths the Decisions govern, comma separated; `*` for repo-wide>
- **Status**: <`draft` while the grill runs, `active` once it is finished>

## Context

<The problem in the user's terms and why it came up now.>

<What the code and the repository showed at the start: one bullet per fact, each with `file:line`.>

<Forces and constraints: who is affected, deadlines, tools, earlier Decisions that apply (by ID).>

<Outside sources used: every plan, RFC, document or decision from another flow that this session
actually used, by path, with its commit or date. Write "none" when there were none.>

## Session path

<One block per question, in the order asked. Nothing is summarised away.>

### Q1 · <the question as asked>
- **Options**: (a) <option>. (b) <option>. (c) <option>.
- **Recommended**: (a). <the reasoning given>
- **Answer**: <the user's answer in their terms, including "you decide">. → D-<slug>.1

### Q2 · <the question as asked>
- **Options**: ...
- **Recommended**: ...
- **Answer**: none of them. <what the user said instead and why they rejected the options>

### Q2 · <the same decision, asked again> (second round)
- **Options**: ...
- **Recommended**: ...
- **Answer**: (b). → D-<slug>.2

### Shared-understanding check
- <defaults the agent listed for branches never asked, which ones the user corrected, and the user's confirmation>

## Decisions

### D-<slug>.1 · <short title>
- **Choice**: <what was chosen, stated as a fact: "exports use a comma delimiter">
- **Reason**: <why this option won>
- **Trade-off**: <what is given up or made harder by choosing it>
- **Binds**: <project | feature> · **Decided by**: <user | agent>

## Design

<Feature records only. Decisions the Design phase makes, same shape, continuing the numbering.>

## Review

<Decisions a Spec Review or Change Review adds, same shape, continuing the numbering.
Each one cites the Finding that caused it, for example "spec-review-1 SR1-F4".>

## Consequences

- <what changes because of these Decisions: files, skills, behaviours>
- <what is off-limits from now on>

## Related

- Spec: <path, or "none">
- Reviews: <paths of review reports that changed this record>
- Glossary terms added or changed in `CONTEXT.md`: <terms, or "none">
- Other records and legacy decision sources this one builds on or changes: <IDs and paths, or "none">
````

## Completeness rules

- **Session path: every question, every option.** Each block holds the question, every option that was offered, the recommended option with its reasoning, and the answer. Rejected options stay listed, because the options the user turned down are the part a later reader cannot reconstruct. A question that was asked again after the user rejected every option gets a second block ("second round"); the first block stays.
- **"You decide" is an answer.** Record it as the answer, and mark the Decision it produced `Decided by: agent`. Defaults the user accepted through "decide the rest" are also `Decided by: agent`; the ones the user overrode are `Decided by: user`.
- **One choice per Decision.** A Decision states exactly one choice. If you are about to write a list of unrelated choices under one ID, split it into one Decision per choice. Details that only spell out the same choice stay together.
- **Every Decision has all five fields**: Choice, Reason, Trade-off, Binds, Decided by. A Trade-off is never blank; when nothing is given up, write "none" and say why in a few words.
- **Binds** is `project` when a future feature has to follow the Decision or knowingly change it, and `feature` otherwise. The full test is in `../spec-driven/references/decisions.md`.
- **Context carries evidence.** Code facts cite `file:line`. Outside sources that were used are cited by path with their commit or date; sources that were found but not used are not listed.
- **Consequences and Related are filled in**, not left as headings. If a session truly changed nothing, say so in one sentence.
- Write in full sentences a newcomer can follow. Do not compress a record to save space.

## When the record is written

The record is written while the session runs, so it survives a context compaction, a crash or a pause.

1. **First answer: create the file.** As soon as the user answers the first question, create `.specs/decisions/<slug>.md` with the header (`Status: draft`), the Context as far as it is known, and a Session path holding that first question with its options, the recommendation and the answer. If the answer settles a choice, add its Decision under `## Decisions` right away, with at least Choice, Binds and Decided by. The other required headings are present from the start; a heading whose content comes later holds the single line `_(written when the grill closes)_`.
2. **Every later answer: append before asking again.** Append the question block and the Decision it settles to the file before you show the next question. The file on disk always holds every answered question.
3. **Resuming.** A record with `Status: draft` is an unfinished session. A session that finds a draft record for its subject (for a feature: a draft whose `Specs` names the feature) continues that file: it reads the Session path, takes every answer there as given, and asks the next unanswered branch. It never starts a second record for the same subject and never re-asks an answered question.
4. **Shared understanding: finish the record.** When the user confirms shared understanding, complete every Decision (Reason and Trade-off included), write Consequences and Related, bring Context up to date, set `Status: active`, and add the record's row to `summary.md` (below). A record is finished only when all of that is done.

A record's Status is `draft` or `active`. No other status exists, and a record is never deleted. Consumers skip `draft` records.

## Changing a Decision later

A Decision always shows its current choice. Git keeps the earlier text.

- **Rewrite in place.** When a review Disposition, a later phase or a later feature changes a Decision, rewrite that Decision's Choice (and Reason and Trade-off where they changed) in the record that holds it, and add one line at the end of the Decision:

  ```md
  - **Changed**: <YYYY-MM-DD> by <feature> (<source, for example spec-review-1 SR1-F2>): <what changed>
  ```

  A Decision changed a second time gets a second `Changed` line.
- **The Decision stays where it is.** A later feature that changes a Decision in another record rewrites it in that other record, with a `Changed` line naming the later feature. The later feature's own record mentions the change in its Session path and Related section; it does not restate the old choice as a new Decision of its own.
- **No replacement markers.** Never mark a Decision as replaced, withdrawn or outdated, never give a Decision a status of its own, and never add a newer Decision that overrides an older one while the older text stays. A Decision that stops applying is rewritten to say that it no longer applies and why, with a `Changed` line. Its record stays `active`.
- **Decisions a review adds** go under `## Review` with the next free ID and cite the Finding that caused them. A Finding that changes no Decision leaves only its Disposition in the review report.
- **The Session path is never rewritten.** A grill held during a review appends its own subsection to the Session path, for example `### Spec Review SR1 grill (<date>)`, with one entry per Finding discussed: what was asked, the options, the recommendation, the answer and the Decision IDs it touched.
- Update the record's `summary.md` row whenever its Summary, Binds, Areas or Specs change.

## `summary.md`

`.specs/decisions/summary.md` is the index every consumer reads first. It holds the table and the legacy lines, nothing else: no Decision text and no usage notes beyond its fixed opening paragraph. It is only an index. Each record's header is the source of truth, and when the two disagree the header wins and the row is corrected.

````md
# Decisions

One row per finished Grilling Record, sorted by Date, then File. Read this first, then open the `active` records that either bind the project with Areas overlapping the paths you touch (or Areas `*`) or name your feature in Specs. Each record's header is the source of truth; if a row looks wrong, read the headers in this folder instead.

| File | Date | Summary | Status | Binds | Areas | Specs |
| --- | --- | --- | --- | --- | --- | --- |
| [billing-retries.md](billing-retries.md) | 2026-03-02 | Failed charges are retried three times over 24 hours, then the invoice is marked unpaid. | active | project | `src/billing/` | `billing-retries` |
| [csv-export.md](csv-export.md) | 2026-04-17 | Orders are exported as a downloaded CSV file, never emailed. Comma delimiter, UTF-8, one row per order line. | active | feature | `src/export/`, `src/ui/orders/` | `csv-export` |

## Legacy decision sources

- `docs/adr/` holds decisions recorded before Grilling Records existed. Check them as well; they are never written to again.
- `.specs/STATE.md` (`## Decisions`) holds `AD-NNN` entries recorded before Grilling Records existed. Check them as well; they are never written to again.
````

Rules for the table:

- **One row per finished record.** A `draft` record has no row; the row is added when the record becomes `active`, so the Status cell always reads `active`.
- **Columns**, in this order: `File` (a link to the record), `Date` (the day the session started, `YYYY-MM-DD`), `Summary` (one or two sentences saying what was decided, not that a session happened), `Status`, `Binds`, `Areas`, `Specs`. The last four repeat the record's header.
- **Specs** names the feature or features whose spec links the record. A grill that is not about a feature writes `none`. When such a record later turns into a feature, the same row is edited to name the feature.
- **Sorted by Date, then File.** Insert a new row at its place in that order instead of appending at the end, so rows added on two branches rarely touch the same lines.

Rules for the legacy lines:

- When you create `summary.md` (with the first record), check the repository for legacy decision sources and add one line under `## Legacy decision sources` for each one that exists: the root `docs/adr/`, each context's `docs/adr/`, and a `## Decisions` section in `.specs/STATE.md`. Each line names the path and says it is a legacy decision source to check as well.
- Legacy sources are read, never written to and never migrated. When there are none, the section says `none`.
