# StockCheck: the checks for Task 2. Run it in the terminal with:  python check.py
# It reads your repository and prints PASS, FIX or a dash (not started yet) for each part of Task 2,
# then your RESULTS LINE, which the exit ticket asks you to paste. It never changes anything.
# Do not change this file.
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
START_LEVEL = 5
NEW_LEVEL = 10
FIRST_NAME = "Campus Shop"
ITEMS = ["Milk", "Bread", "Crisps", "Apples"]
FOLDER = "StockCheck"
OWN = {"stock.py", "README.md", "check.py", ".gitignore", ".vscode"}   # what the first commit may hold


def git(*args):
    """Run one git command in this folder. Give back (exit code, what it printed), or (None, "") with no Git."""
    try:
        done = subprocess.run(["git", *args], cwd=HERE, capture_output=True, text=True,
                              encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return None, ""
    return done.returncode, done.stdout.replace("\r\n", "\n")


def commits():
    """Every commit on this branch, oldest first."""
    code, out = git("rev-list", "--reverse", "HEAD")
    return out.split() if code == 0 else []


def subject(sha):
    return git("log", "-1", "--format=%s", sha)[1].strip()


def parent(sha):
    code, out = git("rev-parse", "--verify", "--quiet", f"{sha}^")
    return out.strip() if code == 0 else None


def file_at(sha, name):
    """A file as that commit saved it, or None when the commit does not hold it."""
    if not sha:
        return None
    code, out = git("show", f"{sha}:{name}")
    return out if code == 0 else None


def file_now(name):
    """A file as it is in the folder now, saved or not."""
    try:
        with open(os.path.join(HERE, name), encoding="utf-8") as f:
            return f.read().replace("\r\n", "\n")
    except OSError:
        return None


def level_in(source):
    found = re.search(r"^LOW_STOCK\s*=\s*(\d+)", source or "", re.M)
    return int(found.group(1)) if found else None


def name_in(source):
    found = re.search(r"^SHOP_NAME\s*=\s*[\"'](.*)[\"']", source or "", re.M)
    return found.group(1) if found else None


def follows_rule(source):
    """Run one version of stock.py: LOW must show beside an item exactly when its count is at the warning level or below."""
    level = level_in(source)
    if source is None or level is None:
        return False
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "stock.py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(source)
        run = subprocess.run([sys.executable, path], capture_output=True, text=True,
                             encoding="utf-8", errors="replace")
    seen = {}
    for line in run.stdout.splitlines():
        found = re.match(r"^(\w+): (\d+) left(\s+LOW)?\s*$", line)
        if found:
            seen[found.group(1)] = (int(found.group(2)), bool(found.group(3)))
    if any(item not in seen for item in ITEMS):
        return False
    return all(low == (count <= level) for count, low in seen.values())


def says_what_changed(sha):
    return len(subject(sha).split()) >= 3


def check_2a(history):
    if os.path.basename(os.path.realpath(HERE)).lower() != FOLDER.lower():
        return "FIX", (f"these files are in {HERE}, not in a folder called {FOLDER}: they came out of the zip loose. "
                       "Tell your teacher before you go on")
    name = git("config", "user.name")[1].strip()
    email = git("config", "user.email")[1].strip()
    if not name or not email:
        return "FIX", "Git does not know your name and email yet: do step 2 of Task 2a"
    if not history:
        return "FIX", "no commit yet: git add ., then git commit with a message"
    stray = sorted(n for n in git("ls-tree", "--name-only", history[0])[1].split("\n") if n and n not in OWN)
    if stray:
        return "FIX", f"the first commit holds {stray[0]}, which did not come in the zip: tell your teacher before you go on"
    missing = [f for f in ("stock.py", "README.md") if file_at(history[-1], f) is None]
    if missing:
        return "FIX", f"{' and '.join(missing)} is not in a commit yet: git add {' '.join(missing)}, then git commit"
    return "PASS", "the repository exists and the project is saved in a commit"


def check_2b(history):
    now = level_in(file_now("stock.py"))
    last = level_in(file_at(history[-1], "stock.py"))
    moved = [sha for sha in history[1:] if level_in(file_at(sha, "stock.py")) != level_in(file_at(parent(sha), "stock.py"))]
    if not moved and last == START_LEVEL and now == START_LEVEL:
        return "-", "not started yet"
    if last != NEW_LEVEL:
        if now == NEW_LEVEL:
            return "FIX", "LOW_STOCK is 10 in the file but not committed yet: git add stock.py, then git commit"
        return "FIX", f"LOW_STOCK should be {NEW_LEVEL} in your last commit, and it is {last}"
    raised = [sha for sha in moved if level_in(file_at(sha, "stock.py")) == NEW_LEVEL]
    if not raised:
        return "FIX", "LOW_STOCK was already 10 in your first commit: set it back to 5 and commit, then do Task 2b again"
    if not says_what_changed(raised[-1]):
        return "FIX", f'the message "{subject(raised[-1])}" does not say what changed: use at least three words'
    return "PASS", "LOW_STOCK is 10, and the commit says what changed"


def check_2c(history):
    passes = [follows_rule(file_at(sha, "stock.py")) for sha in history]
    now_ok = follows_rule(file_now("stock.py"))
    untouched = "if count < LOW_STOCK:" in (file_now("stock.py") or "")
    if not passes[-1]:
        if now_ok:
            return "FIX", "the fix is in the file but not committed yet: git add stock.py, then git commit"
        if untouched and not any(passes):
            return "-", "not started yet"
        return "FIX", "an item at the warning level must show LOW too: run python stock.py and compare it with the rule in README.md"
    fixed = [sha for i, sha in enumerate(history) if passes[i] and i > 0 and not passes[i - 1]]
    if not fixed:
        return "FIX", "your first commit already had the fix: change it back and commit, then fix it again in a commit of its own"
    if level_in(file_at(fixed[-1], "stock.py")) != level_in(file_at(parent(fixed[-1]), "stock.py")):
        return "FIX", ("the fix went into the same commit as the new warning level: undo the fix in stock.py and commit, "
                       "then fix it again in a commit of its own")
    if not says_what_changed(fixed[-1]):
        return "FIX", f'the message "{subject(fixed[-1])}" does not say what changed: use at least three words'
    return "PASS", "LOW shows at the warning level, and the fix is a commit of its own"


def check_2d(history):
    renames = [sha for sha in history[1:]
               if name_in(file_at(parent(sha), "stock.py")) == FIRST_NAME and name_in(file_at(sha, "stock.py")) != FIRST_NAME]
    reverts = [sha for sha in history if subject(sha).startswith("Revert ")]
    last = name_in(file_at(history[-1], "stock.py"))
    if not renames and not reverts:
        return "-", "not started yet"
    if not renames:
        return "FIX", "the revert undid a different commit: the one to undo is the shop name commit"
    wanted = {f'Revert "{subject(sha)}"' for sha in renames}
    if not any(subject(sha) in wanted for sha in reverts):
        if reverts:
            return "FIX", "the revert undid a different commit: the one to undo is the shop name commit"
        return "FIX", "undo the shop name commit with: git revert --no-edit HEAD"
    if last != FIRST_NAME:
        return "FIX", f'SHOP_NAME is "{last}" in your last commit: it should be back to "{FIRST_NAME}"'
    return "PASS", "the shop name commit is undone by a revert, and the history shows both"


def check_2e(history):
    saved = file_at(history[-1], "change-log.md")
    if saved is None:
        if file_now("change-log.md") is not None:
            return "FIX", "change-log.md is not committed yet: git add change-log.md, then git commit"
        return "-", "not started yet"
    versions = set()
    for line in saved.splitlines():
        if not line.strip().startswith("|") or re.fullmatch(r"[\s|:-]*", line):
            continue
        dated = re.search(r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b", line)
        filed = re.search(r"\b[\w-]+\.(py|md)\b", line)
        if not (dated and filed):
            continue
        for token in re.findall(r"\b[0-9a-f]{7,40}\b", line):
            if git("cat-file", "-e", f"{token}^{{commit}}")[0] == 0:
                versions.add(git("rev-parse", token)[1].strip())
    if len(versions) < 4:
        return "FIX", (f"{len(versions)} rows name a real version with its date and file: "
                       "write a row for each commit before this one, at least 4")
    return "PASS", f"the change log names {len(versions)} real versions, each with its date and file"


PARTS = [
    ("2a", "Set up and save the first version", check_2a),
    ("2b", "Change the warning level", check_2b),
    ("2c", "Fix the report", check_2c),
    ("2d", "Go back", check_2d),
    ("2e", "Write the change log", check_2e),
]


def main():
    verdicts = []
    if git("--version")[0] is None:
        print("Git was not found on this PC. Tell your teacher, and see the last section of the task sheet.")
        verdicts = ["-"] * len(PARTS)
    elif not os.path.isdir(os.path.join(HERE, ".git")):
        code, top = git("rev-parse", "--show-toplevel")
        verdicts = ["-"] * len(PARTS)
        if code == 0 and top.strip():
            verdicts[0] = "FIX"
            print(f"FIX   2a  {PARTS[0][1]}: the repository was made too high up, in {top.strip()}, not in {FOLDER}: "
                  "tell your teacher before you go on")
        elif os.path.basename(os.path.realpath(HERE)).lower() != FOLDER.lower():
            print(f"These files are not in a folder called {FOLDER}: they came out of the zip loose. "
                  "Tell your teacher before you run git init.")
        else:
            print("There is no repository in this folder yet. Open the StockCheck folder itself in VS Code, then git init.")
    else:
        history = commits()
        for label, name, check in PARTS:
            if label != "2a" and not history:
                verdict, why = "-", "not started yet"
            else:
                verdict, why = check(history)
            verdicts.append(verdict)
            print(f"{verdict:<5} {label}  {name}: {why}")
    print()
    print("Your results line (copy it into the exit ticket, question two):")
    print("  ".join(f"{label} {verdict}" for (label, _, _), verdict in zip(PARTS, verdicts)))


main()
