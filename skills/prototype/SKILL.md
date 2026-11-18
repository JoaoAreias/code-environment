---
name: prototype
description: Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like.
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

## Pick a branch

Identify which question is being answered, using the user's prompt, the surrounding code, or by asking if the user is around:

- **"Does this logic / state model feel right?"** → [LOGIC.md](LOGIC.md). Build a single shareable HTML file (free-play buttons plus tabbed guided walkthroughs) that pushes the state machine through cases that are hard to reason about on paper, and that a non-developer can drive.
- **"What should this look like?"** → [UI.md](UI.md). Generate several radically different UI variations on a single route, switchable via a URL search param and a floating bottom bar.

The two branches produce very different artifacts, so getting this wrong wastes the whole prototype. If the question is genuinely ambiguous and the user isn't reachable, default to whichever branch better matches the surrounding code (a backend module → logic; a page or component → UI) and state the assumption at the top of the prototype.

## Rules that apply to both

1. **Throwaway from day one, and clearly marked as such.** Locate the prototype code close to where it will actually be used (next to the module or page it's prototyping for) so context is obvious, but name it so a casual reader can see it's a prototype, not production. For throwaway UI routes, obey whatever routing convention the project already uses; don't invent a new top-level structure.
2. **Trivial to run.** A UI prototype starts from one command in the project's task runner: `pnpm <name>`, `python <path>`, `bun <path>`, etc. A logic demo is a single HTML file the user double-clicks. Either way, no thinking required to start it.
3. **No persistence by default.** State lives in memory. Persistence is the thing the prototype is _checking_, not something it should depend on. If the question explicitly involves a database, hit a scratch DB or a local file with a clear "PROTOTYPE, wipe me" name.
4. **Skip the polish.** No tests, no error handling beyond what makes the prototype _runnable_, no abstractions. The point is to learn something fast.
5. **Surface the state.** After every action (logic) or on every variant switch (UI), print or render the full relevant state so the user can see what changed.
6. **When the question is settled, keep the prototype on a throwaway branch and hand the verdict to Specify.** A prototype never becomes production code, and this skill never edits production code. When the user says the question is settled, do these steps in order:
   1. **Write the verdict and the question it settled**, one sentence each. For example: question "does the order state machine cover a payment that is under review?", verdict "orders need a held state".
   2. **Commit the prototype to a throwaway branch.** Create a branch whose name says what it is (for example `prototype/order-held-state`), commit the prototype files there, and put the question and the verdict in the commit message. The branch is the **primary source**: evidence of how the verdict was reached. It is never merged.
   3. **Leave the main branch as it was.** Switch back and check `git status`: the prototype files are not on the main branch, and no file outside the prototype has changed there. If you touched a real file to wire the prototype in (a route, an import, a task-runner entry), that edit belongs to the prototype: it is committed on the throwaway branch only and is absent from the main branch.
   4. **Start Specify with the verdict as input.** Load `spec-driven` by name with your harness's skill tool (the Skill tool in Claude Code, the `skill` tool in opencode), or read `../spec-driven/SKILL.md` from this skill's directory when the harness cannot load a skill by name. Start its Specify phase and give it the verdict, the question it settled and the name of the throwaway branch. Specify takes the verdict as given, cites the branch in the Context of its Grilling Record, and writes the Scenarios the real code has to satisfy.

   Do not copy prototype code or the validated behavior onto the main branch yourself, however small the change looks. The real code is written in spec-driven's Execute, after a human-run `/spec-review` and Execution Approval, and it is written from the spec, not from the prototype.

   This rule holds for both branches and comes before anything [LOGIC.md](LOGIC.md) or [UI.md](UI.md) says about what happens after the prototype. Where they speak of folding a winning variant in, promoting a route or lifting the logic module out, that is work for spec-driven's Execute. In this skill the winner is only named in the verdict.
