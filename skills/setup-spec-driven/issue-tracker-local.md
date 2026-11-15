# Issue tracker: Local Markdown

Issues for this repo live as markdown files in `.scratch/`.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`
- Issues are one file each at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`, never a single combined file
- An issue's ID is its file path from the repo root
- The Spec is not copied here: it stays at `.specs/features/<feature>/spec.md`, and each issue file links to it
- An issue's state is recorded as a `Status:` line near the top of its file (`open` or `closed`)
- A `Blocked by:` line near the top lists the IDs of the issues that block it
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

## When a skill says "publish to the issue tracker"

Create a new file under `.scratch/<feature-slug>/issues/` (creating the directories if needed).

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the issue number directly.
