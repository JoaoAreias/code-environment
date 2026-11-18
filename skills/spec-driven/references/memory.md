# Memory Layer

**File:** `.specs/STATE.md`

The file holds one thing this skill writes: the `## Handoff` snapshot, so paused work can resume. Writes are always targeted at that section - never whole-file overwrites.

**Decisions do not live here.** Every Decision is written into a Grilling Record under `.specs/decisions/` and found through the read rule in [decisions.md](decisions.md). This file never gains a new decision entry.

An older `STATE.md` may still hold a `## Decisions` section with numbered entries. That section is a legacy decision source: [decisions.md](decisions.md) section 3 says when to read it. Never add to it, edit it, reorder it or remove it.

---

## Sections

### `## Handoff` - pause snapshot (~500 tokens, overwritten each pause)

Captures mid-task / in-flight state so work can resume without re-reading the full task history. It complements `tasks.md` and git evidence: on resume, the Handoff is a starting hypothesis that must be reconciled against the real branch, commits, and working tree (see Resume below).

**Format:**

```markdown
## Handoff

- **Feature**: [feature name / .specs path]
- **Phase / Task**: [e.g., Phase 2 / T4 - implement repository layer]
- **Completed**: [comma-separated task IDs or "none"]
- **In-progress** (file:line): [e.g., `src/billing/subscription.service.ts:88` - mid-write]
- **Next step**: [one sentence - exactly what to do next]
- **Blockers**: [none | description]
- **Uncommitted files**: [list or "none"]
- **Branch**: [git branch name]
```

---

## File shape

```markdown
# STATE

## Handoff

[latest snapshot…]
```

If the file does not yet exist, create it with the `## Handoff` header and an empty body. Do not add a `## Decisions` header to a new file.

---

## Read / Write Triggers

| Trigger | Section | Operation |
| ------- | ------- | --------- |
| Pause work / end of session | `## Handoff` | **Replace** - overwrite Handoff section only |
| Resume work / start of session | `## Handoff` | **Read** - load snapshot, then reconcile with git before acting |
| Any phase that reads Decisions | Grilling Records, not this file | **Read** through [decisions.md](decisions.md); an old `## Decisions` section here is read only as a legacy decision source |

---

## Section-scoped write rule (critical)

A pause **replaces** `## Handoff` and touches nothing else. Locate the `## Handoff` header and replace only the content between it and the next `##` header (or end of file). Never overwrite the full file.

An older file may hold a legacy `## Decisions` section above the Handoff. A whole-file overwrite would silently destroy it, and those entries exist nowhere else. The section-scoped write rule is the single correctness invariant of this memory layer.

---

## Pause / Resume Procedure

### Pause

1. Locate the `## Handoff` section in `.specs/STATE.md`.
2. Replace its body (everything between `## Handoff` and the next `##` or EOF) with the current snapshot.
3. Do NOT modify anything above or before `## Handoff`.
4. Commit or stash outstanding changes as appropriate.

### Resume

1. Read the `## Handoff` section of `.specs/STATE.md`.
2. Re-run the read rule in [decisions.md](decisions.md) for the paths the work touches - a Decision may have been added or rewritten since the last session.
3. Read `## Handoff` - treat it as a **hypothesis** for feature, phase/task, next step, blockers, uncommitted files, branch - not as ground truth by itself.
4. **Reconcile with git before editing anything:**
   - Current branch vs Handoff `Branch`
   - `git status --porcelain` (uncommitted / unexpected paths)
   - Recent commits on the branch (messages and touched files)
   - `tasks.md` completion marks and, when present, gate evidence / commit references
5. **Resolve conflicts with evidence, not narrative:**
   - A task with a green gate and an atomic commit already on the branch → do **not** redo it; mark it complete in `tasks.md` if the file still shows it open, then continue from the next incomplete task
   - Partial unverified work in the working tree → preserve it, re-run the relevant gate, then finish the status+commit cycle
   - Stale or missing Handoff → rebuild next-step from git + `tasks.md`, then propose that to the user
   - Unexplained local changes you cannot map to the current task → STOP and ask; do not discard them
6. Propose the reconciled next step to the user before writing any code.
