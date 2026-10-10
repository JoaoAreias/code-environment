"""
scenarios_lib.py - shared parsing for Acceptance Criteria, Scenarios and test claims.

Imported by validate_spec.py, validate_tasks.py, validate_scenarios.py and
prep_review.py (same directory). Pure standard library.

Spec format (inside `**Acceptance Criteria**` lists and `## Edge Cases`):

    1. **PAY-01**: WHEN ... THEN the system SHALL ...

       ```gherkin
       Scenario: PAY-01.S1 optional title
         Given ...
         When ...
         Then ...
       ```

Test format: a comment or docstring inside (or directly above) the test carries
`Scenario: PAY-01.S1` followed by the same Given/When/Then/And/But lines.
"""

import os
import re
import subprocess

REQ_ID = r"[A-Z][A-Z0-9]*-\d+"
REQ_ID_RE = re.compile(r"^" + REQ_ID + r"$")
SCEN_ID_RE = re.compile(r"\b(" + REQ_ID + r")\.S(\d+)\b")
SCEN_LINE_RE = re.compile(r"Scenario(?: Outline)?:\s*(" + REQ_ID + r"\.S\d+)\b(.*)$")
AC_ITEM_RE = re.compile(r"^\s*\d+\.\s+(?:\*\*)?(\[?[A-Z][A-Z0-9\]]*-\d+)(?:\*\*)?\s*[:—-]\s*(.*)$")
NUMBERED_RE = re.compile(r"^\s*\d+\.\s+(.*)$")
STEP_RE = re.compile(r"^(Given|When|Then|And|But)\b\s*(.*)$", re.IGNORECASE)
COMMENT_PREFIX_RE = re.compile(r'^\s*(?:#+|//+|/\*+|\*+|--|;+|"""|\'\'\'|"|\')?\s*')
COMMENT_SUFFIX_RE = re.compile(r'\s*(?:\*/|"""|\'\'\')\s*$')

TEST_PATH_RE = re.compile(
    r"(^|/)(tests?|__tests__|specs?|e2e|integration[-_]tests?)/"
    r"|(^|/)test_[^/]+\.py$|_test\.(py|go|rb|exs?)$|_spec\.rb$"
    r"|\.(test|spec|e2e-spec|e2e)\.[cm]?[jt]sx?$"
    r"|(Test|Tests|Spec|IT)\.(java|kt|cs|scala|swift)$|Test\.php$"
)
CODE_EXT_RE = re.compile(r"\.(py|[cm]?[jt]sx?|go|rb|exs?|java|kt|cs|scala|swift|php|rs)$")

# Test definition heuristics, one per family. Group "name" is the test name.
TEST_DEF_RES = [
    re.compile(r"^\s*(?:async\s+)?def\s+(?P<name>test\w*)\s*\("),  # python
    re.compile(r"^\s*(?:it|test|specify)(?:\.\w+)*\s*\(\s*(['\"`])(?P<name>.+?)\1"),  # js/ts
    re.compile(r"^\s*func\s+(?P<name>Test\w+)\s*\("),  # go
    re.compile(r"^\s*(?:it|scenario|specify|test)\s+(['\"])(?P<name>.+?)\1"),  # ruby/elixir
    re.compile(r"^\s*public\s+function\s+(?P<name>test\w+)\s*\("),  # php
]
ANNOTATION_RE = re.compile(r"^\s*(@Test\b|@ParameterizedTest\b|\[(Fact|Theory|Test|TestMethod)\]|#\[(tokio::)?test\])")
ANNOTATED_FN_RE = re.compile(r"^\s*(?:[\w<>\[\],]+\s+)*?(?:fn|fun|void|Task|def)\s+(?P<name>\w+)\s*[(<]")
HEADER_LINE_RE = re.compile(r'^\s*(@|#\[|\[(Fact|Theory|Test|TestMethod)|#|//|/\*|\*)')


def norm_step(text):
    t = re.sub(r"\s+", " ", text.strip())
    m = STEP_RE.match(t)
    if m:
        return m.group(1).capitalize() + " " + m.group(2).strip()
    return t


def strip_comment(line):
    t = COMMENT_PREFIX_RE.sub("", line, count=1)
    return COMMENT_SUFFIX_RE.sub("", t).strip()


def is_test_path(path):
    p = path.replace(os.sep, "/")
    return bool(CODE_EXT_RE.search(p)) and bool(TEST_PATH_RE.search(p))


def is_placeholder(text):
    return bool(re.match(r"^\s*\[[^\]]*\]\s*$", text))


# ----------------------------- spec parsing -----------------------------

def spec_scope(text):
    m = re.search(r"^\*{0,2}Scope\*{0,2}\s*:\s*\**\s*(Small|Medium|Large|Complex)", text, re.IGNORECASE | re.MULTILINE)
    return m.group(1).capitalize() if m else None


def parse_spec(text):
    """Parse ACs and Scenarios. Returns dict with acs, scenarios, problems.

    acs:       list of {id, line, text}
    scenarios: dict id -> {ac, line, title, steps}
    problems:  list of (line, message) structural errors
    """
    lines = text.splitlines()
    acs, scenarios, problems = [], {}, []
    in_list = False      # inside an Acceptance Criteria / Edge Cases list
    current_ac = None
    in_fence = False
    current_scen = None

    for idx, raw in enumerate(lines, start=1):
        s = raw.strip()
        if s.startswith("```"):
            in_fence = not in_fence
            current_scen = None
            continue
        if in_fence:
            if not in_list:
                continue
            m = SCEN_LINE_RE.search(s)
            if m:
                sid = m.group(1)
                if current_ac is None:
                    problems.append((idx, f"Scenario {sid} is not under an Acceptance Criterion"))
                elif not sid.startswith(current_ac["id"] + "."):
                    problems.append((idx, f"Scenario {sid} sits under {current_ac['id']}; its ID must start with {current_ac['id']}.S"))
                if sid in scenarios:
                    problems.append((idx, f"duplicate Scenario ID {sid}"))
                current_scen = {"ac": current_ac["id"] if current_ac else None, "line": idx,
                                "title": m.group(2).strip(" -:—"), "steps": []}
                scenarios[sid] = current_scen
                continue
            if current_scen is not None and STEP_RE.match(s):
                current_scen["steps"].append(norm_step(s))
            continue

        if re.match(r"^\*{0,2}Acceptance Criteria\*{0,2}", s) or re.match(r"^#{1,4}\s+(Acceptance Criteria|Edge Cases)\b", s):
            in_list, current_ac = True, None
            continue
        if re.match(r"^#{1,4}\s", s):
            in_list, current_ac = False, None
            continue
        if not in_list:
            continue
        m = AC_ITEM_RE.match(raw)
        if m:
            aid, body = m.group(1), m.group(2).strip()
            if aid.startswith("["):
                current_ac = {"id": aid, "line": idx, "text": body, "placeholder": True}
                continue
            current_ac = {"id": aid, "line": idx, "text": body, "placeholder": False}
            acs.append(current_ac)
            continue
        n = NUMBERED_RE.match(raw)
        if n and not raw.startswith((" ", "\t")):
            item = n.group(1).strip()
            if not is_placeholder(item):
                problems.append((idx, f"acceptance criterion has no requirement ID (expected '1. **FEAT-01**: ...'): {item[:60]}"))
            current_ac = None

    for sid, sc in scenarios.items():
        kinds = {st.split(" ", 1)[0] for st in sc["steps"]}
        missing = [k for k in ("Given", "When", "Then") if k not in kinds]
        if missing:
            problems.append((sc["line"], f"Scenario {sid} lacks {'/'.join(missing)} step(s)"))
    for ac in acs:
        if not any(sc["ac"] == ac["id"] for sc in scenarios.values()):
            problems.append((ac["line"], f"{ac['id']} has no Scenario (every Acceptance Criterion needs at least one)"))
    seen = {}
    for ac in acs:
        if ac["id"] in seen:
            problems.append((ac["line"], f"duplicate requirement ID {ac['id']} (first at L{seen[ac['id']]})"))
        seen.setdefault(ac["id"], ac["line"])
    return {"acs": acs, "scenarios": scenarios, "problems": problems}


def load_all_specs(root):
    """Return {scenario_id: (feature, scenario)} across every feature spec."""
    index = {}
    base = os.path.join(root, ".specs", "features")
    if not os.path.isdir(base):
        return index
    for feat in sorted(os.listdir(base)):
        path = os.path.join(base, feat, "spec.md")
        if not os.path.isfile(path):
            continue
        parsed = parse_spec(open(path, encoding="utf-8", errors="replace").read())
        for sid, sc in parsed["scenarios"].items():
            index.setdefault(sid, (feat, sc))
    return index


# ----------------------------- test parsing -----------------------------

def parse_test_file(text):
    """Return list of tests: {name, line, start, end, claims: {sid: [steps]}}."""
    lines = text.splitlines()
    defs = []
    pending_annotation = False
    for i, raw in enumerate(lines):
        name = None
        for rx in TEST_DEF_RES:
            m = rx.match(raw)
            if m:
                name = m.group("name")
                break
        if name is None and pending_annotation:
            m = ANNOTATED_FN_RE.match(raw)
            if m:
                name = m.group("name")
        if ANNOTATION_RE.match(raw):
            pending_annotation = True
        elif name is not None or (raw.strip() and not HEADER_LINE_RE.match(raw)):
            pending_annotation = False
        if name is not None:
            start = i
            while start > 0 and lines[start - 1].strip() and HEADER_LINE_RE.match(lines[start - 1]):
                start -= 1
            defs.append({"name": name, "line": i + 1, "start": start + 1})
    for k, d in enumerate(defs):
        d["end"] = defs[k + 1]["start"] - 1 if k + 1 < len(defs) else len(lines)
        d["claims"] = {}
        current = None
        for j in range(d["start"] - 1, d["end"]):
            body = strip_comment(lines[j])
            m = SCEN_LINE_RE.search(body)
            if m:
                current = m.group(1)
                d["claims"].setdefault(current, [])
                continue
            if current and STEP_RE.match(body):
                d["claims"][current].append(norm_step(body))
            elif current and body and d["claims"][current]:
                current = None
    return defs


# ----------------------------- git helpers -----------------------------

def git(root, *args):
    r = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def tracked_and_untracked(root):
    files = []
    for args in (("ls-files",), ("ls-files", "--others", "--exclude-standard")):
        rc, out, _ = git(root, *args)
        if rc == 0:
            files += [f for f in out.splitlines() if f]
    return sorted(set(files))


def changed_lines(root, since, files=None):
    """Map file -> set of changed (new-side) line numbers between `since` and the working tree.

    Untracked files count as fully changed. A pure deletion marks the line it follows.
    """
    result = {}
    args = ["diff", "-U0", "--no-color", "--no-prefix", "--no-ext-diff", since, "--"]
    if files:
        args += list(files)
    rc, out, _ = git(root, *args)
    current = None
    for ln in out.splitlines():
        if ln.startswith("+++ "):
            path = ln[4:]
            current = None if path == "/dev/null" else path.split("\t")[0]
            if current:
                result.setdefault(current, set())
            continue
        m = re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", ln)
        if m and current:
            start, count = int(m.group(1)), int(m.group(2) if m.group(2) is not None else 1)
            if count == 0:
                result[current].add(max(start, 1))
            else:
                result[current].update(range(start, start + count))
    rc, out, _ = git(root, "ls-files", "--others", "--exclude-standard")
    for f in out.splitlines():
        if f and (files is None or f in files):
            try:
                n = sum(1 for _ in open(os.path.join(root, f), encoding="utf-8", errors="replace"))
            except OSError:
                continue
            result[f] = set(range(1, n + 1))
    return result
