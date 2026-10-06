# Year2-Programming: the checks for the stretch task. Run it in the terminal with:  python check_stretch.py
# It reads your repository and prints PASS, FIX or a dash (not started yet) for each step,
# then one line to post in the class chat. It never changes anything. Do not change this file.
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RECEIPT = "python/Receipt/receipt.py"
KEEP_OUT = ["csharp/TripsManager/bin/Debug/net8.0/TripsManager.dll", "csharp/TripsManager/obj/project.assets.json",
            "csharp/TripsManager/.vs/TripsManager/v17/.suo", "python/StockCheck/__pycache__/stock.cpython-312.pyc"]
TOTAL = "Total: £4.65"


def git(*args):
    try:
        done = subprocess.run(["git", "--no-optional-locks", *args], cwd=HERE, capture_output=True,
                              text=True, encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return None, ""
    return done.returncode, done.stdout.replace("\r\n", "\n")


def exists(ref):
    return git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")[0] == 0


def file_at(ref, name):
    code, out = git("show", f"{ref}:{name}")
    return out if code == 0 else None


def subject(sha):
    return git("log", "-1", "--format=%s", sha)[1].strip()


def parents(sha):
    return git("rev-list", "--parents", "-n", "1", sha)[1].split()[1:]


def is_ancestor(a, b):
    return git("merge-base", "--is-ancestor", a, b)[0] == 0


def file_now(name):
    try:
        with open(os.path.join(HERE, name), encoding="utf-8", errors="replace") as f:
            return f.read().replace("\r\n", "\n")
    except OSError:
        return None


def ignored_by(gitignore, paths):
    """Which of these paths a .gitignore with this text keeps out, tested by Git itself in a scratch folder."""
    if gitignore is None:
        return set()
    tmp = tempfile.mkdtemp()
    try:
        subprocess.run(["git", "init", "-q", tmp], capture_output=True)
        with open(os.path.join(tmp, ".gitignore"), "w", encoding="utf-8") as f:
            f.write(gitignore)
        return {p for p in paths if subprocess.run(["git", "check-ignore", "-q", "--no-index", p], cwd=tmp, capture_output=True).returncode == 0}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


RUNS = {}
PROBE = """
import runpy, io, contextlib
out = io.StringIO()
with contextlib.redirect_stdout(out):
    names = runpy.run_path("receipt.py")
print(out.getvalue(), end="")
fn = names.get("total_of")
if callable(fn):
    quiet = io.StringIO()
    with contextlib.redirect_stdout(quiet):
        got = fn({"Tea": 1.5, "Cake": 2.25})
    print("TOTAL_OF", repr(got), "PRINTED" if quiet.getvalue() else "QUIET")
"""


def run_receipt(source):
    """Run one version of receipt.py in a scratch folder: (what it printed, receipt.txt, what total_of gave back)."""
    if source is None:
        return None, None, None
    if source not in RUNS:
        tmp = tempfile.mkdtemp()
        try:
            with open(os.path.join(tmp, "receipt.py"), "w", encoding="utf-8") as f:
                f.write(source)
            with open(os.path.join(tmp, "probe.py"), "w", encoding="utf-8") as f:
                f.write(PROBE)
            try:
                done = subprocess.run([sys.executable, "probe.py"], cwd=tmp, capture_output=True, text=True, encoding="utf-8",
                                      errors="replace", timeout=10, env=dict(os.environ, PYTHONIOENCODING="utf-8"))
                printed = done.stdout.replace("\r\n", "\n") if done.returncode == 0 else None
            except subprocess.TimeoutExpired:
                printed = None
            path = os.path.join(tmp, "receipt.txt")
            if os.path.exists(path):
                with open(path, encoding="utf-8", errors="replace") as f:
                    written = f.read()
            else:
                written = None
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        fn = None
        if printed and "TOTAL_OF " in printed:
            head, tail = printed.rsplit("TOTAL_OF ", 1)
            printed, fn = head, tail.strip()
        RUNS[source] = (printed, written, fn)
    return RUNS[source]


def journey():
    code, out = git("reflog", "show", "--format=%H%x09%gs", "HEAD")
    if code != 0:
        return []
    steps = [line.split("\t", 1) for line in reversed(out.splitlines()) if "\t" in line]
    moves = [re.match(r"checkout: moving from (\S+) to (\S+)$", w) for _, w in steps]
    renames = [re.match(r"Branch: renamed refs/heads/(\S+) to refs/heads/(\S+)$", w) for _, w in steps]
    first = next(((m or r).group(1) for m, r in zip(moves, renames) if m or r), None)
    if first is None:
        first = git("symbolic-ref", "--short", "HEAD")[1].strip()
    later = {r.group(1): r.group(2) for r in renames if r}

    def final(name):
        seen = set()
        while name in later and name not in seen:
            seen.add(name)
            name = later[name]
        return name

    rows, on = [], first
    for (sha, what), m, r in zip(steps, moves, renames):
        if m:
            on = m.group(2)
        elif r and on == r.group(1):
            on = r.group(2)
        rows.append([sha, what, final(on)])
    return rows


def commits_on(rows, branch):
    return [sha for sha, what, on in rows if on == branch and what.startswith("commit")]


def merged(rows, name):
    return [sha for sha, what, on in rows if on == "main" and what.startswith(f"merge {name}:")]


def tracked(ref):
    return git("ls-tree", "-r", "--name-only", ref)[1].split("\n") if exists(ref) else []


def step_1a(rows):
    made = [sha for sha in commits_on(rows, "receipt") if TOTAL in (run_receipt(file_at(sha, RECEIPT))[0] or "")]
    if made:
        return "PASS", "receipt.py is committed on the receipt branch and prints Total: £4.65"
    if any(file_at(sha, RECEIPT) is not None for sha in commits_on(rows, "main")):
        if file_at("main", RECEIPT) is not None:
            return "FIX", "receipt.py went onto main, not onto a branch: undo it with git revert --no-edit HEAD, then do 1a from the start"
        return "-", "undone: now do 1a from the start, on a branch called receipt"
    if exists("receipt"):
        return "FIX", "receipt has no commit with receipt.py in it yet: make python/Receipt/receipt.py, run it, then commit it"
    return "-", "not started yet"


def step_1b(rows, a):
    if a[0] != "PASS":
        return "-", "not started yet"
    in_commits = [f for ref in ("receipt", "main") for f in tracked(ref) if f.endswith("receipt.txt")]
    if in_commits:
        return "FIX", f"{in_commits[0]} is in a commit: delete it, add the line receipt.txt to .gitignore, then git add . and commit"
    committed = file_at("receipt", ".gitignore")
    kept = ignored_by(committed, ["receipt.txt", "python/Receipt/receipt.txt", RECEIPT] + KEEP_OUT)
    if "receipt.txt" not in kept:
        if "receipt.txt" in ignored_by(file_now(".gitignore"), ["receipt.txt"]):
            return "FIX", "the receipt.txt line is not committed on the receipt branch yet: git add .gitignore, then git commit"
        return "-", "not started yet (next: add the line receipt.txt to .gitignore)"
    if RECEIPT in kept:
        return "FIX", "the .gitignore keeps out receipt.py as well: the line should be receipt.txt"
    if any(p not in kept for p in KEEP_OUT):
        return "FIX", "the .gitignore has lost one of its first four lines: put bin/, obj/, .vs/ and __pycache__/ back"
    return "PASS", "receipt.txt is kept out: the program makes it every time it runs"


def step_1c(rows, b):
    if b[0] != "PASS":
        return "-", "not started yet"
    if merged(rows, "receipt") and file_at("main", RECEIPT) is not None:
        return "PASS", "receipt is merged into main"
    first = next((i for i, (sha, what, on) in enumerate(rows) if on == "receipt" and what.startswith("commit")), len(rows))
    if any(on == "main" for sha, what, on in rows[first:]):
        return "FIX", "receipt is not merged into main yet: git merge receipt, while you are on main"
    return "-", "not started yet (next: git switch main, then git merge receipt)"


def good_function(sha):
    printed, written, fn = run_receipt(file_at(sha, RECEIPT))
    return fn is not None and fn.startswith("3.75 ") and fn.endswith("QUIET") and TOTAL in (printed or "")


def step_2a(rows):
    made = [sha for sha in commits_on(rows, "receipt-function") if good_function(sha)]
    if made:
        return "PASS", "total_of gives back the total, committed on receipt-function"
    tried = commits_on(rows, "receipt-function")
    if tried:
        printed, written, fn = run_receipt(file_at(tried[-1], RECEIPT))
        if fn is None:
            return "FIX", "receipt.py has no function called total_of yet: def total_of(prices):"
        if fn.endswith("PRINTED"):
            return "FIX", "total_of prints the total: it should give it back with return, and the receipt prints it"
        if TOTAL not in (printed or ""):
            return "FIX", "the receipt should still end on Total: £4.65: print the total total_of gives back"
        return "FIX", "total_of should give back the sum of the prices it is given"
    if exists("receipt-function"):
        return "FIX", "receipt-function has no commit of its own yet: write total_of, run it, then commit it"
    return "-", "not started yet"


def changed(base, tip, name):
    return file_at(base, name) != file_at(tip, name)


def step_2b(rows, a):
    if a[0] != "PASS":
        return "-", "not started yet"
    made = next((i for i, (sha, what, on) in enumerate(rows) if on == "receipt-function"), len(rows))
    if not any(on == "main" for sha, what, on in rows[made:]):
        return "-", "not started yet (next: git switch main, then the README line)"
    for sha in git("rev-list", "--merges", "main")[1].split():
        ps = parents(sha)
        if len(ps) != 2:
            continue
        base = git("merge-base", ps[0], ps[1])[1].strip()
        fn = [changed(base, p, RECEIPT) and good_function(p) for p in ps]
        readme = [changed(base, p, "README.md") for p in ps]
        if (fn[0] and readme[1]) or (fn[1] and readme[0]):
            return "PASS", "a merge commit joins receipt-function and main, with the README line"
    if any(re.match(r"merge receipt-function: Fast-forward", what) for sha, what, on in rows if on == "main"):
        return "FIX", "that merge was a fast-forward: commit the README line on main before you merge"
    return "FIX", "commit a line about Receipt in README.md on main, then git merge --no-edit receipt-function"


def step_2c(rows, b):
    if b[0] != "PASS":
        return "-", "not started yet"
    joined = next((i for i, (sha, what, on) in enumerate(rows) if on == "main" and what.startswith("merge receipt-function")), len(rows))
    later = [sha for sha, what, on in rows[joined + 1:] if on == "main" and (what.startswith("commit") or what.startswith("revert"))]
    if not any(changed(sha + "^", sha, RECEIPT) for sha in later):
        return "-", "not started yet (next: the Flapjack at 1.10, committed on main)"
    for sha in git("rev-list", "--first-parent", "main")[1].split():
        if not subject(sha).startswith('Revert "'):
            continue
        undone = git("rev-list", "--parents", "-n", "1", sha)[1].split()[1:]
        target = re.search(r"This reverts commit ([0-9a-f]{7,40})", git("log", "-1", "--format=%b", sha)[1])
        if target and changed(target.group(1) + "^", target.group(1), RECEIPT):
            if TOTAL in (run_receipt(file_at("main", RECEIPT))[0] or ""):
                return "PASS", "the price change is undone by a revert, and the receipt is back to Total: £4.65"
            return "FIX", "the receipt should be back to Total: £4.65 after the revert"
    return "FIX", "commit the new Flapjack price on main, then undo it with git revert --no-edit HEAD" \
        if TOTAL in (run_receipt(file_at("main", RECEIPT))[0] or "") else \
        "the price change is committed: undo it with git revert --no-edit HEAD"


def main():
    labels = ["1a", "1b", "1c", "2a", "2b", "2c"]
    if git("--version")[0] is None or git("rev-parse", "--git-dir")[0] != 0:
        print("No repository here yet: do Task 2 first.")
        got = {k: ("-", "") for k in labels}
    else:
        rows = journey()
        got = {}
        got["1a"] = step_1a(rows)
        got["1b"] = step_1b(rows, got["1a"])
        got["1c"] = step_1c(rows, got["1b"])
        got["2a"] = step_2a(rows) if got["1c"][0] == "PASS" else ("-", "not started yet (Project 1 first)")
        got["2b"] = step_2b(rows, got["2a"])
        got["2c"] = step_2c(rows, got["2b"])
        for k in labels:
            print(f"{got[k][0]:<5} {k}  {got[k][1]}")
    print()
    print("Post this line in the class chat:")
    print("Stretch: " + "  ".join(f"{k} {got[k][0]}" for k in labels))


main()
