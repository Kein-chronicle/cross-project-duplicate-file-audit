#!/usr/bin/env python3
"""fleet_audit: cheap mechanical probes over a fleet of sibling projects/outputs.
  dupes   : byte-identical files that exist in >= N projects (a copy-pasted template bug is present in all of them)
  charsplit: text where a string was joined character by character ("i; P; h; o; n; e")
  overlap : near-duplicate long text between siblings (n-gram overlap)
usage: fleet_audit.py dupes ROOT [--min-projects 3] [--ext .swift,.ts,.py] | charsplit FILE... | overlap FILE_A FILE_B [--n 5]
exit 0 nothing found | 1 findings | 2 bad input"""
import argparse, collections, hashlib, os, re, sys

def dupes(root, min_projects, exts):
    if not os.path.isdir(root): print("bad root"); return 2
    projects = [d for d in sorted(os.listdir(root)) if os.path.isdir(os.path.join(root, d)) and not d.startswith(".")]
    if len(projects) < 2: print("need >= 2 projects: nothing to compare"); return 2
    seen = collections.defaultdict(set)
    for p in projects:
        for d, ds, fs in os.walk(os.path.join(root, p)):
            ds[:] = [x for x in ds if x not in (".git", "node_modules", "build", "dist", "DerivedData")]
            for f in fs:
                if exts and not f.endswith(tuple(exts)): continue
                path = os.path.join(d, f)
                try: data = open(path, "rb").read()
                except OSError: continue
                if len(data) < 200: continue                       # tiny files are boilerplate by nature
                seen[(f, hashlib.md5(data).hexdigest())].add(p)
    hits = {k: v for k, v in seen.items() if len(v) >= min_projects}
    for (f, h), ps in sorted(hits.items(), key=lambda kv: -len(kv[1])):
        print(f"{f}  md5={h[:8]}  identical in {len(ps)}/{len(projects)} projects: {', '.join(sorted(ps))[:100]}")
    print("review each: one shared file means one shared bug (or a missing abstraction)" if hits else "no byte-identical files shared widely")
    return 1 if hits else 0

CHARSPLIT = re.compile(r"(?:^|[\s:,])(?:\S\s?[;|,]\s){6,}\S(?:$|\s)")
def charsplit(files):
    bad = 0
    for f in files:
        try: t = open(f, encoding="utf-8", errors="ignore").read()
        except OSError: print(f"cannot read {f}"); return 2
        for i, line in enumerate(t.splitlines(), 1):
            if CHARSPLIT.search(line): print(f"{f}:{i}: looks character-split: {line.strip()[:70]!r}"); bad += 1
    print("none" if not bad else f"{bad} suspicious line(s)")
    return 1 if bad else 0

def grams(t, n):
    w = re.findall(r"\w+", t.lower()); return {" ".join(w[i:i+n]) for i in range(len(w) - n + 1)}
def overlap(a, b, n):
    try: ta, tb = open(a, encoding="utf-8").read(), open(b, encoding="utf-8").read()
    except OSError as e: print(e); return 2
    ga, gb = grams(ta, n), grams(tb, n)
    if not ga or not gb: print("text too short to compare"); return 2
    r = len(ga & gb) / min(len(ga), len(gb))
    print(f"{n}-gram overlap: {len(ga & gb)} shared ({r:.0%} of the smaller text)")
    return 1 if r > 0.25 else 0

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["dupes", "charsplit", "overlap"]); ap.add_argument("args", nargs="+")
    ap.add_argument("--min-projects", type=int, default=3); ap.add_argument("--ext", default=""); ap.add_argument("--n", type=int, default=5)
    a = ap.parse_args()
    if a.cmd == "dupes": sys.exit(dupes(a.args[0], a.min_projects, [e for e in a.ext.split(",") if e]))
    if a.cmd == "charsplit": sys.exit(charsplit(a.args))
    if len(a.args) != 2: print("overlap needs two files"); sys.exit(2)
    sys.exit(overlap(a.args[0], a.args[1], a.n))
