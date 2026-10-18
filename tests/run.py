import os, subprocess, sys, tempfile
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "fleet_audit.py"); ok = True
def run(*a): return subprocess.run([sys.executable, S, *a], capture_output=True, text=True)
def expect(n, c, v=""):
    global ok; ok &= bool(c); print(("ok   " if c else "FAIL ") + n + ("" if c else f"\n     {v}"))
root = tempfile.mkdtemp(); buggy = "func grant() { timer(0.5) { granted = false } }\n" * 12
for i in range(4):
    p = os.path.join(root, f"app{i}"); os.makedirs(p); open(os.path.join(p, "RewardedAd.swift"), "w").write(buggy)
    open(os.path.join(p, "Unique.swift"), "w").write(f"// unique {i}\n" + "let x = %d\n" % i * 40)
r = run("dupes", root, "--min-projects", "3", "--ext", ".swift")
expect("the same buggy file in 4/4 apps is found", r.returncode == 1 and "RewardedAd.swift" in r.stdout and "4/4" in r.stdout, r.stdout)
expect("unique files are not reported", "Unique.swift" not in r.stdout, r.stdout)
r = run("dupes", root, "--min-projects", "5", "--ext", ".swift"); expect("threshold respected", r.returncode == 0, r.stdout)
one = tempfile.mkdtemp(); r = run("dupes", one); expect("fewer than two projects => cannot compare (exit 2)", r.returncode == 2, r.stdout)
f = os.path.join(root, "notes.txt"); open(f, "w").write("1. Review notes\n2. i; P; h; o; n; e; ; S; E; 1; 5\n3. fine line, with; some punctuation\n")
r = run("charsplit", f); expect("character-joined review note is caught, normal punctuation is not", r.returncode == 1 and ":2:" in r.stdout and ":3:" not in r.stdout, r.stdout)
a = os.path.join(root, "a.txt"); b = os.path.join(root, "b.txt"); c = os.path.join(root, "c.txt")
text = " ".join(f"word{i}" for i in range(60)); open(a, "w").write(text); open(b, "w").write(text + " extra tail words here now"); open(c, "w").write(" ".join(f"other{i}" for i in range(60)))
expect("near-duplicate descriptions are flagged", run("overlap", a, b).returncode == 1)
expect("unrelated descriptions pass", run("overlap", a, c).returncode == 0)
sys.exit(0 if ok else 1)
