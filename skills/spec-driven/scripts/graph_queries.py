#!/usr/bin/env python3
"""
graph_queries.py - questions the graphify CLI does not answer directly.

Reads graphify-out/graph.json (built by `graphify update .`). Pure standard library.
graphify has no embeddings, so these queries only produce *candidates*; the agent
reads the code before calling anything a duplicate or a Legacy Path.

Commands:
  symbols --match a,b,c      Callables/classes whose qualified name or file path
                             contains any term (ranked by matches). Use concept
                             words and synonyms, not just the new symbol's name.
  callers NAME               Who calls NAME, split into production and test callers.
  new-symbols --since REF    Symbols defined on lines added since REF.
  dup-candidates --since REF For each new symbol, existing symbols that share name
                             tokens, file path tokens, community, or callees.
  test-only [--since REF]    Production symbols whose only callers are tests
                             (Legacy Path candidates). With --since, only those the
                             Change touched or whose test callers it touched.

Common options: --root DIR (default .), --graph PATH (default <root>/graphify-out/graph.json),
--limit N, --include-tests (symbols/dup-candidates).

Exit codes: 0 ok, 2 usage error (missing graph, unknown symbol).
"""

import argparse
import json
import os
import re
import sys

from scenarios_lib import changed_lines, is_test_path

STOP = {"get", "set", "is", "has", "do", "make", "to", "from", "the", "a", "an", "of", "for",
        "with", "by", "on", "in", "init", "new", "create", "handle", "process", "run", "main",
        "self", "cls", "test", "tests", "src", "lib", "app", "index", "py", "ts", "js", "tsx",
        "jsx", "go", "rb", "java", "kt", "util", "utils", "helper", "helpers"}


def tokens(text):
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    return {t for t in re.split(r"[^A-Za-z0-9]+", text.lower()) if len(t) > 1 and t not in STOP}


class Graph:
    def __init__(self, path):
        data = json.load(open(path, encoding="utf-8"))
        self.nodes = {n["id"]: n for n in data["nodes"]}
        links = data.get("links", data.get("edges", []))
        self.calls_in, self.calls_out, parent = {}, {}, {}
        for e in links:
            rel = e.get("relation")
            src, dst = e["source"], e["target"]
            if rel == "calls":
                # Undirected graphs may store either orientation; the call site file wins.
                site = e.get("source_file")
                if site and self.file(dst) == site and self.file(src) != site:
                    src, dst = dst, src
                self.calls_out.setdefault(src, set()).add(dst)
                self.calls_in.setdefault(dst, set()).add(src)
            elif rel == "method":
                parent[dst] = src
        self.qual = {}
        for nid, n in self.nodes.items():
            label = n.get("label", nid).strip("()").lstrip(".")
            p = parent.get(nid)
            self.qual[nid] = f"{self.nodes[p].get('label', p)}.{label}" if p in self.nodes else label

    def file(self, nid):
        return self.nodes.get(nid, {}).get("source_file", "")

    def line(self, nid):
        m = re.match(r"L(\d+)", self.nodes.get(nid, {}).get("source_location", "") or "")
        return int(m.group(1)) if m else 0

    def symbols(self):
        for nid, n in self.nodes.items():
            if n.get("_callable") or n.get("_callable_class"):
                yield nid

    def is_test(self, nid):
        return is_test_path(self.file(nid))

    def show(self, nid):
        n = self.nodes[nid]
        return f"{self.qual[nid]}  {self.file(nid)}:{self.line(nid)}  [community: {n.get('community_name', n.get('community', '-'))}]"


def find(g, name):
    want = name.strip("()").lstrip(".").lower()
    hits = [nid for nid in g.symbols() if g.qual[nid].lower() == want or g.qual[nid].lower().endswith("." + want)]
    return hits


def new_symbols(g, root, since):
    touched = changed_lines(root, since)
    return [nid for nid in g.symbols() if g.line(nid) in touched.get(g.file(nid), set())]


def cmd_symbols(g, args):
    terms = [t.strip().lower() for t in args.match.split(",") if t.strip()]
    scored = []
    for nid in g.symbols():
        if g.is_test(nid) and not args.include_tests:
            continue
        hay = g.qual[nid].lower() + " " + g.file(nid).lower()
        score = sum(1 for t in terms if t in hay)
        if score:
            scored.append((-score, g.qual[nid], nid))
    for _, _, nid in sorted(scored)[: args.limit]:
        print(g.show(nid))
    if not scored:
        print("(no symbol matches; try synonyms or `graphify query`)")
    return 0


def cmd_callers(g, args):
    hits = find(g, args.name)
    if not hits:
        print(f"no symbol named {args.name}", file=sys.stderr)
        return 2
    for nid in hits:
        callers = g.calls_in.get(nid, set())
        prod = sorted(c for c in callers if not g.is_test(c))
        test = sorted(c for c in callers if g.is_test(c))
        print(g.show(nid))
        print(f"  production callers ({len(prod)}):")
        for c in prod:
            print(f"    {g.show(c)}")
        print(f"  test callers ({len(test)}):")
        for c in test:
            print(f"    {g.show(c)}")
    return 0


def cmd_new_symbols(g, args):
    found = [nid for nid in new_symbols(g, args.root, args.since) if args.include_tests or not g.is_test(nid)]
    for nid in sorted(found, key=lambda n: (g.file(n), g.line(n))):
        print(g.show(nid))
    if not found:
        print(f"(no new symbols since {args.since})")
    return 0


def cmd_dup_candidates(g, args):
    fresh = [nid for nid in new_symbols(g, args.root, args.since) if not g.is_test(nid)]
    fresh_set = set(fresh)
    pool = [nid for nid in g.symbols() if nid not in fresh_set and (args.include_tests or not g.is_test(nid))]
    if not fresh:
        print(f"(no new production symbols since {args.since})")
    for nid in sorted(fresh, key=lambda n: (g.file(n), g.line(n))):
        nt = tokens(g.qual[nid])
        ft = tokens(os.path.splitext(g.file(nid))[0])
        comm = g.nodes[nid].get("community")
        callees = g.calls_out.get(nid, set())
        scored = []
        for other in pool:
            reasons = []
            shared = nt & tokens(g.qual[other])
            if shared:
                reasons.append("name:" + "+".join(sorted(shared)))
            pshared = (ft & tokens(os.path.splitext(g.file(other))[0])) - nt
            if pshared:
                reasons.append("path:" + "+".join(sorted(pshared)))
            if comm is not None and g.nodes[other].get("community") == comm:
                reasons.append("same community")
            common = callees & g.calls_out.get(other, set())
            if common:
                reasons.append(f"{len(common)} shared callee(s)")
            score = 3 * len(shared) + len(pshared) + (1 if "same community" in reasons else 0) + 2 * len(common)
            if score:
                scored.append((-score, g.qual[other], other, reasons))
        print(f"NEW {g.show(nid)}")
        for _, _, other, reasons in sorted(scored)[: args.limit]:
            print(f"    {g.show(other)}  <- {', '.join(reasons)}")
        if not scored:
            print("    (no structural candidates; search by concept with `symbols --match`)")
    return 0


def cmd_test_only(g, args):
    touched = changed_lines(args.root, args.since) if args.since else None
    rows = []
    for nid in g.symbols():
        if g.is_test(nid):
            continue
        callers = g.calls_in.get(nid, set())
        if not callers or any(not g.is_test(c) for c in callers):
            continue
        if touched is not None:
            mine = g.file(nid) in touched
            theirs = any(g.file(c) in touched for c in callers)
            if not (mine or theirs):
                continue
        rows.append((g.file(nid), g.line(nid), nid, callers))
    for _, _, nid, callers in sorted(rows):
        print(g.show(nid))
        for c in sorted(callers):
            print(f"    called only by test {g.show(c)}")
    if not rows:
        print("(no production symbol is called only by tests" + (f" within the Change since {args.since})" if args.since else ")"))
    print("\nNote: entry points (routes, CLI commands, handlers wired by a framework) have no static callers; "
          "check how a symbol is reached before calling it a Legacy Path.")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="graph_queries.py", description="Candidate queries over graphify's graph.json.")
    p.add_argument("--root", default=".")
    p.add_argument("--graph", default=None)
    p.add_argument("--limit", type=int, default=8)
    p.add_argument("--include-tests", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("symbols")
    sp.add_argument("--match", required=True)
    sp.set_defaults(fn=cmd_symbols)
    sp = sub.add_parser("callers")
    sp.add_argument("name")
    sp.set_defaults(fn=cmd_callers)
    sp = sub.add_parser("new-symbols")
    sp.add_argument("--since", required=True)
    sp.set_defaults(fn=cmd_new_symbols)
    sp = sub.add_parser("dup-candidates")
    sp.add_argument("--since", required=True)
    sp.set_defaults(fn=cmd_dup_candidates)
    sp = sub.add_parser("test-only")
    sp.add_argument("--since", default=None)
    sp.set_defaults(fn=cmd_test_only)
    args = p.parse_args(argv)
    args.root = os.path.abspath(args.root)
    path = args.graph or os.path.join(args.root, "graphify-out", "graph.json")
    if not os.path.isfile(path):
        print(f"graph_queries: {path} not found; run `graphify update .` first", file=sys.stderr)
        return 2
    return args.fn(Graph(path), args)


if __name__ == "__main__":
    raise SystemExit(main())
