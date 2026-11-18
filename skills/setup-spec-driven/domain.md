# Domain Docs

How skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root, or
- **`CONTEXT-MAP.md`** at the repo root if it exists: it points at one `CONTEXT.md` per context. Read each one relevant to the topic.
- **`.specs/decisions/summary.md`**: the index of this repo's Grilling Records. Follow the read rule in the spec-driven skill's `references/decisions.md`: it says which records to open for the paths you are about to touch, what to do when the index is broken, and which older decision sources to check as well.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The `domain-modeling` skill (reached through spec-driven's Specify, `/grill-with-docs` and `/improve-codebase-architecture`) creates them lazily when terms or Decisions actually get resolved.

## File structure

Single-context repo (most repos):

```
/
├── CONTEXT.md
├── .specs/decisions/
│   ├── summary.md
│   ├── event-sourced-orders.md
│   └── postgres-write-model.md
└── src/
```

Multi-context repo (presence of `CONTEXT-MAP.md` at the root):

```
/
├── CONTEXT-MAP.md
├── .specs/decisions/                  ← every Grilling Record, whatever context it touches
└── src/
    ├── ordering/
    │   └── CONTEXT.md
    └── billing/
        └── CONTEXT.md
```

## Use the glossary's vocabulary

When your output names a domain concept (in a Ticket title, a refactor proposal, a hypothesis, a test name), use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal: either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `domain-modeling`).

## Flag Decision conflicts

If your output contradicts an active Decision, surface it explicitly by its ID rather than silently overriding:

> _Contradicts D-event-sourced-orders.2 (orders are event-sourced), but worth reopening because…_
