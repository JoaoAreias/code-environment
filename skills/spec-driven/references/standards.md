# Standards

One rule list, read by everyone who writes or judges code: Specify, Design, Execute, the Verifier, the Spec Reviewer and the Change Reviewer. The author applies it while building; the reviewers check the same list.

`<skill-dir>` below is the `spec-driven` skill directory.

---

## 1. Repo Standards: discover, record, obey

A **Repo Standard** is a rule the codebase documents about how its code must be written. Look in:

- Agent rule files: `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`, `.claude/rules/`, `.github/copilot-instructions.md`
- Contributor docs: `CONTRIBUTING.md`, `CODING_STANDARDS.md`, `STYLEGUIDE.md`, `docs/` pages on standards, style, conventions or guidelines
- Tool config: linter, formatter and type-checker settings (`eslint`, `biome`, `ruff`/`pyproject.toml`, `golangci`, `rubocop`, `tsconfig.json` strictness, `.editorconfig`)
- Active `AD-NNN` entries in `.specs/STATE.md` that set a convention

Rules a tool already enforces are not re-checked by hand. Flag only code that switches a rule off (`eslint-disable`, `# noqa`, `# type: ignore`, `@ts-ignore`, `//nolint`) without a stated reason.

**Record** them in the Spec's `## Standards` section: each source file, then one line per rule that touches this feature. `none found - Smell Baseline only` is a valid entry.

**Precedence:** a Repo Standard always beats the Smell Baseline. When a Repo Standard endorses a pattern the baseline would flag, the smell is suppressed.

---

## 2. Smell Baseline

Design smells checked in every codebase (Fowler, *Refactoring*, ch. 3, plus two agent-specific ones). Each is a **judgment call**: write "possible Feature Envy", say why, never call it a violation. Each entry reads *what it is* → *how to fix*.

- **Mysterious Name**: a name that does not reveal what the thing does or holds. → Rename; if no honest name comes, the design is murky.
- **Duplicated Code**: the same logic shape in more than one place in the change. → Extract the shared shape and call it from both.
- **Feature Envy**: a function that works on another object's data more than its own. → Move it to the data it envies.
- **Data Clumps**: the same few fields or parameters keep travelling together. → Bundle them into one type.
- **Primitive Obsession**: a primitive or string standing in for a domain concept. → Give the concept its own small type.
- **Repeated Switches**: the same `switch`/`if` cascade on the same type recurs. → Polymorphism, or one map both sites share.
- **Shotgun Surgery**: one logical change forces scattered edits across many files. → Gather what changes together into one module.
- **Divergent Change**: one module is edited for several unrelated reasons. → Split it so each module changes for one reason.
- **Speculative Generality**: abstractions, parameters or hooks for needs the Spec does not have. → Delete them; inline until a real need shows.
- **Message Chains**: long `a.b().c().d()` navigation the caller should not depend on. → Hide the walk behind one method.
- **Middle Man**: a class or function that mostly delegates onward. → Cut it; call the real target.
- **Refused Bequest**: a subclass that ignores or overrides most of what it inherits. → Drop the inheritance; use composition.
- **Legacy Path**: an older implementation kept beside its replacement only because a test still exercises it. → Delete the old path; claim or drop the test (section 3).
- **Semantic Duplicate**: new code that re-implements behavior existing code already provides, under different names. → Reuse or extend the existing code (section 4).

---

## 3. Tests

**Scenarios are the contract; tests are disposable proofs of them.** Every test proves exactly one Scenario and carries the Scenario's ID and its Given/When/Then text, copied verbatim from the Spec, in a docstring or comment:

```python
def test_rejects_expired_card():
    """
    Scenario: PAY-01.S2
      Given a card that expired last month
      When the customer pays
      Then the payment is declined with "card_expired"
    """
```

`python3 <skill-dir>/scripts/validate_scenarios.py <feature>` enforces the mechanics: unknown IDs, drifted text, missing proofs, tests that claim more than one Scenario, and (with `--since <base>`) Unclaimed Tests the Change touched.

### Behavior Test or Implementation-Coupled Test

A **Behavior Test** exercises the public interface, asserts the outcome the Scenario names, and survives any refactor that keeps that outcome. Two questions decide it:

1. Would the test still pass under a plausible *wrong* implementation? Then it is shallow.
2. Would the test fail under a refactor that changes no behavior? Then it is **Implementation-Coupled**.

A useful test fails in case 1 and passes in case 2.

Red flags for Implementation-Coupled Tests:

- Mocks internal collaborators, or asserts call counts or call order on them. Mocks belong at system boundaries: network, clock, randomness, third-party APIs.
- Calls private methods or reads private state.
- Verifies through a side door (a raw DB query, a log line) when the public interface can show the outcome.
- Its name or Scenario describes *how* ("calls paymentService.process"), not *what* ("payment is declined").
- Asserts on structure (snapshot of internals, exact SQL text) rather than on the result.

Shallow-test red flags: no assertion, tautologies, "does not throw" as the only check (unless not throwing is the behavior), happy path only when the Spec lists failure modes.

### Scenario quality (proposed tests, judged at planning)

A Scenario is a good proposed test when it uses concrete values, names one observable outcome reachable through the public interface, and describes behavior a user or caller cares about. Where the Spec's implicit-requirement dimensions apply (partial failure, rollback, retries and idempotency, concurrency, external-dependency failure), at least one Scenario covers the failure mode.

### Touch it, claim it or drop it

Tests written before Scenarios existed are **Grandfathered** while no Change touches them. When a Change modifies or breaks one, it must either:

- be claimed by a Scenario back-filled into the Spec (it becomes contract), or
- be rewritten or removed as an **Unclaimed Test**.

Never keep old production code alive to satisfy an unclaimed test. Record each removal as a Claim in the commit body: `Removed test: <file>::<name> - unclaimed; asserted <what it checked>`.

---

## 4. Search before you add

Before adding a capability (Specify), a component (Design), or any new exported function, class or module (Execute), look for an existing equivalent:

1. `graphify update .` (incremental; cheap after the first build). If `graphify` is missing, stop and tell the user: duplicate detection has no evidence without it.
2. `python3 <skill-dir>/scripts/graph_queries.py symbols --match <concept words and synonyms>`. Search by concept ("money,amount,cents,parse,decimal"), not only by the name you planned.
3. `graphify query "<question>"` and `graphify explain "<candidate>"` to see how a candidate is used.
4. `rg` for literal domain terms the graph cannot see (string keys, config names, SQL).
5. Read the candidates. Reuse or extend an equivalent; build new only when none fits.

Record what you searched:

- Specify: `## Existing Capabilities` (queries, findings, and why this is not a Redundant Feature)
- Design: the reuse table in `design.md`
- Execute: one line in the commit body, `Searched: <terms> -> reused <symbol>` or `Searched: <terms> -> none equivalent`

Reviewers treat these records as Claims and re-check them.
