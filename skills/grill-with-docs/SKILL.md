---
name: grill-with-docs
description: A relentless interview to sharpen a plan, decision or design that is not a feature. It writes a Grilling Record under .specs/decisions/ and keeps the glossary (CONTEXT.md) current as we go. To plan or build a feature, use spec-driven instead.
disable-model-invocation: true
---

# Grill with Docs

A grilling session for something that is **not a feature**: a direction ("should billing move to events?"), a trade-off, a naming question, a design idea that is not yet a request to build. The session leaves two things behind: a **Grilling Record** under `.specs/decisions/` and an up-to-date glossary in `CONTEXT.md`. It builds nothing and writes no spec.

## Features go through spec-driven

If the user wants a feature planned or built, this is the wrong entry point. spec-driven's Specify phase runs the same interview, with the same two skills, and then writes the spec that the reviews and Execute need. Say so in one sentence and start spec-driven's Specify instead of grilling here. Carry on in this skill only when the subject is not a feature, or when the user answers that they want it grilled before deciding whether it becomes one.

## Run the grill

Call the Skill tool twice, for "grilling" and "domain-modeling". If the harness cannot load a skill by name, read `../grilling/SKILL.md`, `../domain-modeling/SKILL.md` and `../domain-modeling/GRILLING-RECORD-FORMAT.md` from this skill's directory.

- `grilling` gives the rules of the interview: one question per turn, concrete options, one recommendation, and the "you decide" and "decide the rest" escapes.
- `domain-modeling` gives what is written down and how: the glossary format, the Grilling Record format and the `summary.md` format. Follow it exactly. Before the first question it also has you find the Decisions that already bind the subject, through the read rule in `../spec-driven/references/decisions.md`.

## What the session writes

**The Grilling Record.** Every session that puts at least one decision to the user writes one record, in full, while the session runs:

1. **At the first answer**, create `.specs/decisions/<slug>.md` with `Status: draft` and `Specs: none` in its header. The slug is 2 to 4 words and must not already exist in the folder. If a `draft` record for this subject already exists, continue it instead of starting a new one.
2. **After every answer**, append the question, every option offered, the recommendation and the answer to the Session path, with the Decision the answer settles, before asking the next question.
3. **When the user confirms shared understanding**, finish the record: complete every Decision (choice, reason, trade-off, Binds, Decided by), write Consequences and Related, and set `Status: active`. Then add the record's row to `.specs/decisions/summary.md`, at its place in Date order. **The Specs cell of that row reads `none`**, because no spec links this record. When this creates `summary.md`, add its legacy lines as the format describes.

So when the session ends, a new Grilling Record exists under `.specs/decisions/`, it is `active`, and its `summary.md` row reads Specs `none`. A session the user leaves before shared understanding keeps its `draft` record, which has no row yet, and the next session on the same subject resumes it.

**The glossary.** When a term is resolved, update `CONTEXT.md` right then, in the `domain-modeling` format. Create the file when the first term is resolved if it does not exist. In a repository with a `CONTEXT-MAP.md`, the term goes into the `CONTEXT.md` of the context it belongs to.

Nothing else is written. A decision that changes an earlier Decision is rewritten in the record that holds it, with a `Changed` line, as `domain-modeling` describes.

## When the grill turns into a feature

The session ends at shared understanding. It does not go on to design, plan or build. If the user then wants what was decided built, point them to spec-driven: Specify continues this same record, sets its Specs from `none` to the feature's name, and writes the spec from it. Do not start a second record for the feature.
