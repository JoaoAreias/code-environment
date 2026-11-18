---
name: improve-codebase-architecture
description: Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick and write the session down as a Grilling Record.
disable-model-invocation: true
---

# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

This command is _informed_ by the project's domain model and built on a shared design vocabulary:

- Call the Skill tool with "codebase-design" for the architecture vocabulary (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**) and its principles (the deletion test, "the interface is the test surface", "one adapter = hypothetical seam, two = real"). Use these terms exactly in every suggestion, and don't drift into "component," "service," "API," or "boundary."
- The domain language in `CONTEXT.md` gives names to good seams. The project's active Decisions record choices this command should not re-litigate. They live in Grilling Records under `.specs/decisions/`; find the ones that bind the area you look at with the read rule in spec-driven's `references/decisions.md` (`../spec-driven/references/decisions.md` from this skill's directory). That file is the one source of the rule, and it also covers the legacy decision sources of older repositories.

This command proposes and grills. It does not refactor. A deepening the user decides to do is built through spec-driven (step 4).

## Process

### 1. Explore

**Scope before you scan: YAGNI.** Deepening a module pays off by making future changes to it easier, so put extra weight on the parts of the codebase that have recently changed. Decide *where* to look before you look:

- If the user named a direction (a module, a subsystem, a pain point), take it, and skip the inference below.
- Otherwise, walk back a good stretch of the commit history (`git log --oneline`) to find the codebase's hot spots, the files and areas that keep coming up, and let those paths pull your attention first. If the changes are scattered with no clear hot spot, widen the net.

Read the project's domain glossary (`CONTEXT.md`) first. Then run the read rule in `../spec-driven/references/decisions.md`, completely and in order, for the paths you are about to look at: open the `active` Grilling Records that bind the project there, and check the legacy decision sources it lists. An architecture review has no feature, so skip that file's feature test. Note every Decision that governs the area, and in particular every Decision that records an earlier rejected candidate: an earlier review may already have settled what you are about to suggest.

Then spawn a sub-agent to walk the codebase. Don't follow rigid heuristics; explore organically and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow**, with an interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it? A "yes, concentrates" is the signal you want.

### 2. Present candidates as an HTML report

Write a self-contained HTML file to the OS temp directory so nothing lands in the repo. Resolve the temp dir from `$TMPDIR`, falling back to `/tmp` (or `%TEMP%` on Windows), and write to `<tmpdir>/architecture-review-<timestamp>.html` so each run gets a fresh file. Open it for the user (`xdg-open <path>` on Linux, `open <path>` on macOS, `start <path>` on Windows) and tell them the absolute path.

The report uses **Tailwind via CDN** for layout and styling, and **Mermaid via CDN** for diagrams where a graph/flow/sequence reliably communicates the structure. Mix Mermaid with hand-crafted CSS/SVG visuals: use Mermaid when relationships are graph-shaped (call graphs, dependencies, sequences), and hand-built divs/SVG when you want something more editorial (mass diagrams, cross-sections, collapse animations). Each candidate gets a **before/after visualisation**. Be visual.

For each candidate, render a card with:

- **Files**: which files/modules are involved
- **Problem**: why the current architecture is causing friction
- **Solution**: plain English description of what would change
- **Benefits**: explained in terms of locality and leverage, and how tests would improve
- **Before / After diagram**: side-by-side, custom-drawn, illustrating the shallowness and the deepening
- **Recommendation strength**: one of `Strong`, `Worth exploring`, `Speculative`, rendered as a badge

End the report with a **Top recommendation** section: which candidate you'd tackle first and why.

**Use CONTEXT.md vocabulary for the domain, and the `/codebase-design` vocabulary for the architecture.** If `CONTEXT.md` defines "Order," talk about "the Order intake module," not "the FooBarHandler," and not "the Order service."

**Decision conflicts**: if a candidate contradicts an active Decision, only surface it when the friction is real enough to warrant revisiting that Decision. Mark it clearly in the card with the Decision's ID (e.g. a warning callout: _"contradicts D-billing-rules.3, but worth reopening because…"_). Don't list every theoretical refactor a Decision forbids, and never re-suggest a candidate that an active Decision records as rejected unless the reason it gives no longer holds. A legacy decision the read rule found is treated the same way and is named by its file name or entry ID. Only the user changes a Decision: the report raises the conflict, it does not resolve it.

See [HTML-REPORT.md](HTML-REPORT.md) for the full HTML scaffold, diagram patterns, and styling guidance.

Do NOT propose interfaces yet. After the file is written, ask the user: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, call the Skill tool with "grilling" to walk the decision tree with them: constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive.

Side effects happen inline as decisions crystallize; call the Skill tool with "domain-modeling" to keep the domain model and the session's record current as you go:

- **Naming a deepened module after a concept not in `CONTEXT.md`?** Add the term to `CONTEXT.md`. Create the file lazily if it doesn't exist.
- **Sharpening a fuzzy term during the conversation?** Update `CONTEXT.md` right there.
- **Every answer goes into the session's Grilling Record.** The grilling loop is a grilling session, so it writes one Grilling Record in the `domain-modeling` format: create `.specs/decisions/<slug>.md` with `Status: draft` and `Specs: none` at the first answer, append each question with its options, the recommendation and the answer before asking the next one, and at shared understanding complete the Decisions, set `Status: active` and add the row to `.specs/decisions/summary.md` with Specs `none`. Do not ask the user whether to record: the record is always written.
- **User rejects the candidate?** Record the rejection as a Decision in that Grilling Record, without asking first. The Choice says which deepening is not done and names the modules; the Reason is the user's reason in their own terms; the Trade-off is the friction that stays. When the reason will still hold the next time someone reviews this area (a constraint, a dependency, a deliberate design choice), the Decision's Binds is `project` and the record's Areas name the candidate's paths, so the read rule shows it to the next architecture review and the candidate is not suggested again. When the reason is only about timing ("not worth it right now"), the Decision says so and its Binds is `feature`, meaning it matters only to this session, so a later review may raise the candidate again.
- **A decision of this session changes an earlier Decision?** Rewrite that Decision in the record that holds it and add a `Changed` line, as `domain-modeling` describes. Never leave the old choice standing next to a new one.
- **Want to explore alternative interfaces for the deepened module?** Call the Skill tool with "codebase-design" and use its design-it-twice parallel sub-agent pattern.

### 4. Hand the deepening to spec-driven

The session ends at shared understanding, with an `active` Grilling Record. Do not start the refactor. If the user wants the deepening built, it is a feature: load `spec-driven` by name and start its Specify phase from this record. Specify continues the same record instead of starting a new one, sets its Specs from `none` to the feature's name, and writes the Scenarios the deepened module has to satisfy.
