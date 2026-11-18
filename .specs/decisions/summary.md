# Decisions

One row per finished Grilling Record, sorted by Date, then File. Read this first, then open the `active` records that either bind the project with Areas overlapping the paths you touch (or Areas `*`) or name your feature in Specs. Each record's header is the source of truth; if a row looks wrong, read the headers in this folder instead.

| File | Date | Summary | Status | Binds | Areas | Specs |
| --- | --- | --- | --- | --- | --- | --- |
| [grill-in-spec-driven.md](grill-in-spec-driven.md) | 2026-10-11 | spec-driven Specify becomes the grill and every grill writes a Grilling Record under `.specs/decisions/`; ADRs and `STATE.md` Decisions are retired. Tickets, mandatory Tasks and Design at Medium, `inspect` proofs, tolerance for legacy and foreign plans, and a single implementation path through spec-driven. | active | project | `skills/`, `agents/`, `install.sh`, `render-adapters.js`, `README.md`, `CONTEXT.md`, `.specs/` | `integrate-skills` |

## Legacy decision sources

- `docs/adr/` holds decisions recorded before Grilling Records existed (0001–0003). Check them as well; they are never written to again.
