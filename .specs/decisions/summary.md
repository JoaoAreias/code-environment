# Decisions

One row per Grilling Record. Read this first, then open the records whose Status is `active` or `partly superseded` and that either bind the project with Areas overlapping the paths you touch (or Areas `*`) or name your feature in Specs.

| File | Summary | Status | Binds | Areas | Specs |
| --- | --- | --- | --- | --- | --- |
| [0001-integrate-grill-into-spec-driven.md](0001-integrate-grill-into-spec-driven.md) | spec-driven Specify becomes the grill and every grill writes a Grilling Record under `.specs/decisions/`; ADRs and `STATE.md` Decisions are retired. Tickets, mandatory Tasks and Design at Medium, and a single implementation path through spec-driven. | active | project | `skills/`, `agents/`, `install.sh`, `render-adapters.js`, `README.md`, `CONTEXT.md`, `.specs/` | `integrate-skills` |

## Legacy decision paths

- `docs/adr/` holds decisions recorded before Grilling Records existed (0001–0003). Check them as well; they are never written to again.
