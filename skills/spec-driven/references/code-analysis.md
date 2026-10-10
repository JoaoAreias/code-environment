# Code Analysis Tools

Use graceful degradation for code search and structural analysis.

## Tool Priority

1. **graphify** - Relationships and existing concepts: who calls what, what a change touches, whether an equivalent already exists. `graphify update .` (incremental), `graphify query "<question>"`, `graphify explain "<symbol>"`, `graphify path "A" "B"`, and `python3 <skill-dir>/scripts/graph_queries.py` (`symbols --match`, `callers`, `new-symbols`, `dup-candidates`, `test-only`). `graphify-out/` stays out of git via `.git/info/exclude`.
2. **ast-grep** (`sg`) - Structural pattern-based search
3. **ripgrep** (`rg`) - Fast context-aware text search, including what the graph cannot see (string keys, config, SQL)
4. **grep** - Standard text search (always available)

graphify has no embeddings: it finds candidates by structure and names. Search by concept words and synonyms, then read the code before calling two things equivalent.

## Detection

Check tool availability before use:

```bash
# Check for ast-grep
if command -v sg >/dev/null 2>&1; then
  # Use ast-grep for structural search
elif command -v rg >/dev/null 2>&1; then
  # Fall back to ripgrep
else
  # Use standard grep as final fallback
fi
```

## Usage Examples

**Finding function definitions:**

```bash
# ast-grep (best - structural)
sg -p 'function $NAME($$$) { $$$ }'

# ripgrep (fallback - fast text)
rg '^function\s+\w+\(' --type-add 'source:*.[extension]' -t source

# grep (last resort - basic)
grep -r '^function ' --include="*.[extension]"
```

**Finding imports/requires:**

```bash
# ast-grep
sg -p 'import { $$$ } from "$MODULE"'

# ripgrep
rg '^import .* from' --type-add 'source:*.[extension]' -t source

# grep
grep -r '^import ' --include="*.[extension]"
```

**Finding class/component definitions:**

```bash
# ast-grep
sg -p 'class $NAME { $$$ }'

# ripgrep
rg '^(class|export class)\s+\w+' --type-add 'source:*.[extension]' -t source

# grep
grep -r '^class ' --include="*.[extension]"
```

## Search Scope

**Best practices:**

- Limit to source file extensions relevant to project
- Exclude directories: `node_modules`, `vendor`, `dist`, `build`, `.git`
- Focus on source directories: `src`, `lib`, `app`
- Use file type filters when available

**Performance tips:**

- Use specific patterns over broad searches
- Limit directory depth with `--max-depth` (ripgrep/grep)
- Cache results for repeated queries

## Fallback Notice

If graphify is unavailable, stop and tell the user before any search-before-adding step: without the graph, duplicate detection has no evidence. It installs with `uv tool install graphifyy`.

If ast-grep unavailable, display once per session:

```
⚠️ ast-grep not detected. Install for more precise structural code analysis.
   https://ast-grep.github.io/guide/quick-start.html
```

## When to Use

- Finding usage patterns across codebase
- Identifying code structure and organization
- Locating function/class/component definitions
- Analyzing import/dependency patterns
- Refactoring impact analysis
- Code navigation in unfamiliar codebases
