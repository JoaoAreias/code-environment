---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a CONTEXT.md, or writing or changing a Grilling Record.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and the Decisions down the moment they crystallise. (Merely *reading* `CONTEXT.md` for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

Most repos have a single context:

```
/
├── CONTEXT.md
├── .specs/
│   └── decisions/
│       ├── summary.md                ← index: one row per finished Grilling Record
│       ├── billing-retries.md        ← one Grilling Record per grilling session
│       └── csv-export.md
└── src/
```

If a `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each glossary lives:

```
/
├── CONTEXT-MAP.md
├── .specs/
│   └── decisions/                    ← every Grilling Record, whatever context it touches
├── src/
│   ├── ordering/
│   │   └── CONTEXT.md
│   └── billing/
│       └── CONTEXT.md
```

The glossary sits beside the code it describes. Grilling Records always live in the one `.specs/decisions/` folder at the root; a record's `Areas` header says which paths its Decisions govern.

Create files lazily: only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved. If no `.specs/decisions/` exists, create it, with its `summary.md`, when the first Grilling Record is written.

This skill owns three formats: the glossary ([CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md)), and the Grilling Record and `summary.md` ([GRILLING-RECORD-FORMAT.md](./GRILLING-RECORD-FORMAT.md)). How to find and read the Decisions that already bind the code you touch is not defined here: follow the read rule in `../spec-driven/references/decisions.md` before the first question, and treat what it finds as given.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` right there. Don't batch these up: capture them as they happen. Use the format in [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

`CONTEXT.md` should be totally devoid of implementation details. Do not treat `CONTEXT.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Write the Grilling Record as the session goes

Every grilling session writes one Grilling Record, whatever started it: spec-driven's Specify or Design, `/grill-with-docs`, or an architecture review. The record is the complete account of the session, so every decision the session makes goes into it. There is no test a decision must pass to be worth recording, and no shorter kind of decision file exists. A conversation that only sharpens glossary terms and puts no decision to the user writes no record.

Follow [GRILLING-RECORD-FORMAT.md](./GRILLING-RECORD-FORMAT.md) exactly. In short:

- **At the first answer**, create `.specs/decisions/<slug>.md` with `Status: draft`. The slug is 2 to 4 words and must not already exist in the folder; if it does, choose another and leave the existing file alone.
- **After every answer**, append the question, every option offered, the recommendation and the answer to the Session path, and the Decision it settles, before asking the next question. Don't batch these up either.
- **If a `draft` record for this subject already exists**, continue it from its Session path instead of starting a new one.
- **When the user confirms shared understanding**, complete every Decision (choice, reason, trade-off, Binds, Decided by), write Consequences and Related, set `Status: active`, and add the record's row to `.specs/decisions/summary.md` in Date order. When that creates `summary.md`, also add its legacy lines.
- **When a Decision changes later**, rewrite it in the record that holds it and add a `Changed` line. Never leave the old choice standing next to a newer one.

A session that is not about a feature writes `Specs: none`. If it later turns into a feature, spec-driven's Specify continues the same record.
