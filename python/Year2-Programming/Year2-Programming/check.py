# Year2-Programming: the checks for Task 2. Run it in the terminal with:  python check.py
# It reads your repository and prints PASS, FIX or a dash (not started yet) for each part of Task 2,
# then your RESULTS LINE, which the exit ticket asks you to paste. It never changes anything.
# Do not change this file.
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
STOCK = "python/StockCheck/stock.py"
KEEP = ["README.md", "check.py", "check_stretch.py", STOCK,
        "csharp/TripsManager/Program.cs", "csharp/TripsManager/TripsManager.csproj"]
KEEP_OUT = {  # what a build or a run makes, and a path each line of the .gitignore has to keep out
    "bin/": "csharp/TripsManager/bin/Debug/net8.0/TripsManager.dll",
    "obj/": "csharp/TripsManager/obj/project.assets.json",
    ".vs/": "csharp/TripsManager/.vs/TripsManager/v17/.suo",
    "__pycache__/": "python/StockCheck/__pycache__/stock.cpython-312.pyc",
}
BUILT = {"bin", "obj", ".vs", "__pycache__"}
ORDERS = {"Milk": 10, "Bread": 16, "Apples": 15}   # 20 take away each LOW count; Crisps is not LOW
TOTAL = re.compile(r"^Items\b.*\b41\s*$", re.M)     # Items in stock: 41
FOLDER = "Year2-Programming"
TOP = {"python", "csharp", "README.md", "check.py", "check_stretch.py", ".gitignore",   # what the repository's top holds,
       ".vscode"}                                                                         # and VS Code's own settings folder


def git(*args):
    """Run one git command in this folder. Give back (exit code, what it printed), or (None, "") with no Git."""
    try:
        done = subprocess.run(["git", "--no-optional-locks", *args], cwd=HERE, capture_output=True,
                              text=True, encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return None, ""
    return done.returncode, done.stdout.replace("\r\n", "\n")


def exists(ref):
    return git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")[0] == 0


def file_at(ref, name):
    """A file as that commit saved it, or None when the commit does not hold it."""
    code, out = git("show", f"{ref}:{name}")
    return out if code == 0 else None


def file_now(name):
    """A file as it is in the folder now, saved or not."""
    try:
        with open(os.path.join(HERE, name), encoding="utf-8", errors="replace") as f:
            return f.read().replace("\r\n", "\n")
    except OSError:
        return None


def subject(sha):
    return git("log", "-1", "--format=%s", sha)[1].strip()


def says_what_changed(sha):
    return len(subject(sha).split()) >= 3


def parents(sha):
    return git("rev-list", "--parents", "-n", "1", sha)[1].split()[1:]


def is_ancestor(a, b):
    return git("merge-base", "--is-ancestor", a, b)[0] == 0


def ignored_by(gitignore, paths):
    """Which of these paths a .gitignore with this text keeps out, tested by Git itself in a scratch folder."""
    if gitignore is None:
        return set()
    tmp = tempfile.mkdtemp()
    try:
        subprocess.run(["git", "init", "-q", tmp], capture_output=True)
        with open(os.path.join(tmp, ".gitignore"), "w", encoding="utf-8") as f:
            f.write(gitignore)
        out = set()
        for path in paths:
            done = subprocess.run(["git", "check-ignore", "-q", "--no-index", path], cwd=tmp, capture_output=True)
            if done.returncode == 0:
                out.add(path)
        return out
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


RUNS = {}


def run_report(source):
    """Run one version of stock.py. Give back what it printed, or None when it stops with an error."""
    if source is None:
        return None
    if source not in RUNS:
        tmp = tempfile.mkdtemp()
        try:
            path = os.path.join(tmp, "stock.py")
            with open(path, "w", encoding="utf-8") as f:
                f.write(source)
            done = subprocess.run([sys.executable, path], cwd=tmp, capture_output=True, text=True, encoding="utf-8",
                                  errors="replace", timeout=10, env=dict(os.environ, PYTHONIOENCODING="utf-8"))
            RUNS[source] = done.stdout.replace("\r\n", "\n") if done.returncode == 0 else None
        except subprocess.TimeoutExpired:
            RUNS[source] = None
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    return RUNS[source]


def order_problem(printed):
    """None when every LOW item has its order line with the right number and Crisps has none; else what is wrong."""
    if printed is None:
        return "stock.py stops with an error: run python python/StockCheck/stock.py and read its last line"
    blocks, current = {}, None
    for line in printed.splitlines():
        item = re.match(r"^(\w+): \d+ left", line)
        if item:
            current = item.group(1)
            blocks[current] = line
        elif current:
            blocks[current] += "\n" + line
    for item, want in ORDERS.items():
        text = blocks.get(item)
        if text is None:
            return f"{item} is missing from the report: put its line back in the stock dictionary"
        if "order" not in text.lower():
            return f"{item} is LOW and has no order line under it"
        if not re.search(rf"\b{want}\b", text.split("\n", 1)[-1] if "\n" in text else text.split("LOW", 1)[-1]):
            return f"{item} should order {want}: 20 take away its count"
    if "order" in blocks.get("Crisps", "").lower():
        return "Crisps is not LOW, so it needs no order line: the new line goes inside the if, under the LOW line"
    return None


def trips_readme_at(ref):
    """The TripsManager README as that commit saved it, README.md or readme.md (Windows does not mind which), or None."""
    code, out = git("ls-tree", "--name-only", ref, "csharp/TripsManager/")
    names = [n for n in out.split("\n") if n.rsplit("/", 1)[-1].lower() == "readme.md"] if code == 0 else []
    return file_at(ref, names[0]) if names else None


def trips_readme_now():
    try:
        names = [n for n in os.listdir(os.path.join(HERE, "csharp", "TripsManager")) if n.lower() == "readme.md"]
    except OSError:
        return None
    return file_now("csharp/TripsManager/" + names[0]) if names else None


def has_orders(ref):
    printed = run_report(file_at(ref, STOCK))
    return bool(printed and "order" in printed.lower())


def total_problem(printed):
    """None when the report ends on the total line and prints it once; else what is wrong. (After Enter, VS Code
    indents a new line to match the one above, so a total typed there prints inside the loop.)"""
    lines = [l for l in (printed or "").split("\n") if l.strip()]
    hits = [i for i, l in enumerate(lines) if TOTAL.match(l)]
    if len(hits) == 1 and hits[0] == len(lines) - 1:
        return None
    where = f"prints {len(hits)} times" if len(hits) > 1 else "prints before the end of the report"
    return (f"the total {where}, because its line is inside the loop: take its indent away (Shift+Tab), "
            "so it starts at the left edge and runs once, after the loop")


def journey():
    """HEAD's reflog, oldest first: [commit, what happened, the branch HEAD was on]. It is how Git remembers
    which branch each commit and each merge was made on, even after a fast-forward has made two branches alike."""
    code, out = git("reflog", "show", "--format=%H%x09%gs", "HEAD")
    if code != 0:
        return []
    steps = [line.split("\t", 1) for line in reversed(out.splitlines()) if "\t" in line]
    moves = [re.match(r"checkout: moving from (\S+) to (\S+)$", w) for _, w in steps]
    renames = [re.match(r"Branch: renamed refs/heads/(\S+) to refs/heads/(\S+)$", w) for _, w in steps]
    first = next(((m or r).group(1) for m, r in zip(moves, renames) if m or r), None)
    if first is None:
        first = git("symbolic-ref", "--short", "HEAD")[1].strip()
    later = {}                      # a branch renamed later counts under its new name (master, then main)
    for r in renames:
        if r:
            later[r.group(1)] = r.group(2)

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


def merges_on(rows, branch, name):
    return [sha for sha, what, on in rows if on == branch and (what.startswith(f"merge {name}:")
                                                             or what.startswith(f"merge {name}-"))]


def check_2a(rows):
    top = git("rev-parse", "--show-toplevel")[1].strip()
    if top and os.path.normcase(os.path.realpath(top)) != os.path.normcase(os.path.realpath(HERE)):
        return "FIX", f"the repository was made too high up, in {top}, not in {FOLDER}: tell your teacher before you go on"
    if os.path.basename(os.path.realpath(HERE)).lower() != FOLDER.lower():
        return "FIX", (f"these files are in {HERE}, not in a folder called {FOLDER}: they came out of the zip loose. "
                       "Tell your teacher before you go on")
    name = git("config", "user.name")[1].strip()
    email = git("config", "user.email")[1].strip()
    if not name or not email:
        return "FIX", "Git does not know your name and email yet: do step 2 of Task 2a"
    if not exists("main"):
        if exists("master"):
            return "FIX", "your first branch is called master: type git branch -m master main"
        return "FIX", "no commit yet: git add ., then git commit with a message"
    for first in git("rev-list", "--max-parents=0", "main")[1].split():
        stray = sorted(n for n in git("ls-tree", "--name-only", first)[1].split("\n")
                       if n and n not in TOP and "gitignore" not in n.lower())
        if stray:
            return "FIX", (f"the first commit holds {stray[0]}, which did not come in the zip: "
                           "tell your teacher before you go on")
    saved = git("ls-tree", "-r", "--name-only", "main")[1].split("\n")
    missing = [f for f in KEEP if f not in saved]
    if missing:
        return "FIX", f"{missing[0]} is not in a commit on main: git add ., then git commit"
    if ".gitignore" not in saved:
        near = [n for n in os.listdir(HERE) if "gitignore" in n.lower() and n != ".gitignore"]
        if near:
            return "FIX", f'your file is called "{near[0]}": rename it .gitignore, with the dot and nothing after'
        if file_now(".gitignore") is not None:
            return "FIX", ".gitignore is not committed yet: git add .gitignore, then git commit"
        return "FIX", "there is no .gitignore yet: step 3 of Task 2a"
    text = file_at("main", ".gitignore")
    kept_out = ignored_by(text, list(KEEP_OUT.values()) + KEEP + [".gitignore"])
    for line, path in KEEP_OUT.items():
        if path not in kept_out:
            anchored = any(l.strip().startswith("/") for l in text.splitlines())
            extra = ", with no / in front of it" if anchored else ""
            return "FIX", f"the .gitignore does not keep out {line}: give it the line {line}{extra}"
    for path in KEEP + [".gitignore"]:
        if path in kept_out:
            return "FIX", f"the .gitignore keeps out {path} as well, which is your own work: take out the line that matches it"
    built = [f for f in saved if BUILT & set(f.split("/")[:-1])]
    if built:
        folder = "/".join(built[0].split("/")[:[i for i, p in enumerate(built[0].split("/")) if p in BUILT][0] + 1])
        return "FIX", f"{folder} is in a commit: delete that folder in VS Code, then git add . and git commit"
    return "PASS", "one repository on main, both languages committed, and a .gitignore that keeps out what builds make"


def check_2b(rows):
    made = commits_on(rows, "restock")
    good = [sha for sha in made if order_problem(run_report(file_at(sha, STOCK))) is None]
    if good:
        if not says_what_changed(good[0]):
            return "FIX", f'the message "{subject(good[0])}" does not say what changed: use at least three words'
        return "PASS", "the order lines are committed on restock"
    if any(order_problem(run_report(file_at(sha, STOCK))) is None for sha in commits_on(rows, "main")):
        if has_orders("main"):
            return "FIX", ("the order lines are in a commit on main, not on a branch: undo it with git revert --no-edit HEAD, "
                           "then do Task 2b from step 1")
        return "-", "undone: now do Task 2b from step 1"
    ready = order_problem(run_report(file_now(STOCK))) is None
    if not exists("restock"):
        if ready:
            return "FIX", "the order lines are not on a branch yet: git switch -c restock (the change comes with you), then commit"
        return "-", "not started yet"
    if made:
        return "FIX", order_problem(run_report(file_at(made[-1], STOCK)))
    if ready:
        return "FIX", "the order lines are not committed yet: git add python/StockCheck/stock.py, then git commit"
    return "FIX", "restock has no commit of its own yet: do steps 2 to 4 of Task 2b"


def check_2c(rows, b):
    if b[0] != "PASS":
        return "-", "not started yet (Task 2b first)"
    good = [sha for sha in commits_on(rows, "restock") if order_problem(run_report(file_at(sha, STOCK))) is None]
    if merges_on(rows, "main", "restock") and any(is_ancestor(sha, "main") for sha in good):
        problem = order_problem(run_report(file_at("main", STOCK)))
        if problem:
            return "FIX", f"main does not show the order lines any more: {problem}"
        return "PASS", "restock is merged into main, and main shows the order lines"
    first = next(i for i, row in enumerate(rows) if row[0] in good)
    if any(on == "main" for sha, what, on in rows[first:]):
        return "FIX", "restock is not merged into main yet: git merge restock, while you are on main"
    return "-", "not started yet (next: git switch main, then git merge restock)"


def check_2d(rows):
    made = [sha for sha in commits_on(rows, "trips-readme") if trips_readme_at(sha) is not None]
    if not made:
        on_main = [sha for sha in commits_on(rows, "main") if trips_readme_at(sha) is not None]
        if on_main:
            if trips_readme_at("main") is not None:
                return "FIX", ("the README went onto main, not onto a branch: undo it with git revert --no-edit HEAD, "
                               "then do Task 2d from step 1")
            return "-", "undone: now do Task 2d from step 1"
        others = sorted({on for sha, what, on in rows if what.startswith("commit") and on not in ("main", "restock")
                         and trips_readme_at(sha) is not None})
        if others:
            return "FIX", f"the README is on a branch called {others[0]}: rename it with git branch -m {others[0]} trips-readme"
        if trips_readme_now() is not None:
            if not exists("trips-readme"):
                return "FIX", "the README is not on a branch yet: git switch -c trips-readme (it comes with you), then commit it"
            return "FIX", "the README is not committed yet: git add, then git commit"
        return "-", "not started yet"
    words = len((trips_readme_at(made[-1]) or "").split())
    if words < 12:
        return "FIX", f"the README has {words} words: write at least two sentences, what TripsManager is for and how to run it"
    if not says_what_changed(made[0]):
        return "FIX", f'the message "{subject(made[0])}" does not say what changed: use at least three words'
    if not merges_on(rows, "main", "trips-readme") or not is_ancestor(made[-1], "main"):
        return "FIX", "trips-readme is not merged into main yet: git switch main, then git merge trips-readme"
    return "PASS", "the README is committed on trips-readme and merged into main"


def changed(base, tip, name):
    return file_at(base, name) != file_at(tip, name)


def has_total(ref=None, source=None):
    printed = run_report(source if ref is None else file_at(ref, STOCK))
    return bool(printed and TOTAL.search(printed))


def check_2e(rows):
    branch_side = [sha for sha, what, on in rows if on.startswith("stock-total") and what.startswith("commit") and has_total(sha)]
    joins = []
    for sha in git("rev-list", "--merges", "main")[1].split():
        ps = parents(sha)
        if len(ps) != 2:
            continue
        base = git("merge-base", ps[0], ps[1])[1].strip()
        total = [changed(base, p, STOCK) and has_total(p) for p in ps]
        readme = [changed(base, p, "README.md") for p in ps]
        if (total[0] and readme[1]) or (total[1] and readme[0]):
            joins.append(sha)
    if joins and has_total("main"):
        problem = total_problem(run_report(file_at("main", STOCK)))
        if problem:
            return "FIX", problem
        if branch_side and not says_what_changed(branch_side[0]):
            return "FIX", f'the message "{subject(branch_side[0])}" does not say what changed: use at least three words'
        return "PASS", "a merge commit joins stock-total and main, and main has both changes"
    if not branch_side:
        if any(has_total(sha) for sha in commits_on(rows, "main") if len(parents(sha)) == 1):
            if has_total("main"):
                return "FIX", ("the total went straight onto main, not onto a branch: undo it with git revert --no-edit HEAD, "
                               "then do Task 2e from step 1")
            return "-", "undone: now do Task 2e from step 1"
        if has_total(source=file_now(STOCK)):
            if not exists("stock-total"):
                return "FIX", "the total line is not on a branch yet: git switch -c stock-total (it comes with you), then commit it"
            return "FIX", "the total line is not committed yet: git add python/StockCheck/stock.py, then git commit"
        return "-", "not started yet"
    problem = total_problem(run_report(file_at(branch_side[-1], STOCK)))
    if problem:
        return "FIX", problem
    if any(re.match(r"merge stock-total\S*: Fast-forward", what) for sha, what, on in rows if on == "main"):
        return "FIX", "that merge was a fast-forward, because main had not moved on: see Fast-forward under If something goes wrong"
    if any(what.startswith("merge main") for sha, what, on in rows if on.startswith("stock-total")):
        return "FIX", "you merged main into stock-total, which is the wrong way round: git switch main, then git merge --no-edit stock-total"
    made_at = next((i for i, (sha, what, on) in enumerate(rows) if on.startswith("stock-total")), len(rows))
    moved = [sha for sha, what, on in rows[made_at:] if on == "main" and what.startswith("commit")
             and len(parents(sha)) == 1 and changed(parents(sha)[0], sha, "README.md")]
    if not moved:
        return "FIX", "main has no commit of its own since you made stock-total: step 4 commits a line in README.md on main"
    return "FIX", "stock-total is not merged into main yet: git switch main, then git merge --no-edit stock-total"


def main():
    labels = [("2a", "Set up the repository for the year"), ("2b", "Make a branch and commit on it"),
              ("2c", "Switch back and merge"), ("2d", "A branch of your own"), ("2e", "Two lines of work at once")]
    verdicts = []
    if git("--version")[0] is None:
        print("Git was not found on this PC. Tell your teacher, and see the last section of the task sheet.")
        verdicts = ["-"] * len(labels)
    elif git("rev-parse", "--git-dir")[0] != 0:
        said = subprocess.run(["git", "status"], cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
        if "dubious ownership" in said:
            print("Git says detected dubious ownership: the folder is on a network drive. Move it into OneDrive, then open it again.")
        elif os.path.basename(os.path.realpath(HERE)).lower() != FOLDER.lower():
            print(f"These files are not in a folder called {FOLDER}: they came out of the zip loose. "
                  "Tell your teacher before you run git init.")
        else:
            print("There is no repository here yet. Open the Year2-Programming folder itself in VS Code, then git init -b main.")
        verdicts = ["-"] * len(labels)
    else:
        rows = journey()
        results = {}
        results["2a"] = check_2a(rows) if rows else ("FIX", "no commit yet: git add ., then git commit with a message")
        started = bool(rows)
        results["2b"] = check_2b(rows) if started else ("-", "not started yet")
        results["2c"] = check_2c(rows, results["2b"]) if started else ("-", "not started yet")
        results["2d"] = check_2d(rows) if started else ("-", "not started yet")
        results["2e"] = check_2e(rows) if started else ("-", "not started yet")
        for label, name in labels:
            verdict, why = results[label]
            verdicts.append(verdict)
            print(f"{verdict:<5} {label}  {name}: {why}")
    print()
    print("Your results line (copy it into the exit ticket, question two):")
    print("  ".join(f"{label} {verdict}" for (label, _), verdict in zip(labels, verdicts)))


main()
