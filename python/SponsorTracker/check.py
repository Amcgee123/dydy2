# SponsorTracker: the checks for Task 2. Run it in the terminal, in the SponsorTracker folder, with:  python check.py
# It reads your code and your repository, and prints PASS, FIX or a dash (not started yet) for each part of Task 2,
# then your RESULTS LINE, which starts SponsorTracker: and which the exit ticket asks you to paste. A change reads PASS
# once it works, was committed on a branch, is merged into main, and main is on GitHub. It never changes your files or
# your repository. Do not change this file.
import ast
import builtins
import contextlib
import copy
import glob
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = "SponsorTracker"
YEAR = "Year2-Programming"
REAL_INPUT = builtins.input


# ------------------------------------------------------------------ Git
def find_git():
    """Git on this PC: the one on the PATH, or the copy inside GitHub Desktop or Visual Studio."""
    found = shutil.which("git")
    if found:
        return found
    places = []
    local = os.environ.get("LOCALAPPDATA", "")
    if local:
        places += glob.glob(os.path.join(local, "GitHubDesktop", "app-*", "resources", "app", "git", "cmd", "git.exe"))
        places += glob.glob(os.path.join(local, "GitHubDesktop", "app-*", "resources", "app", "git", "mingw64", "bin", "git.exe"))
    for base in (os.environ.get("ProgramFiles", ""), os.environ.get("ProgramFiles(x86)", "")):
        if base:
            places += glob.glob(os.path.join(base, "Git", "cmd", "git.exe"))
            places += glob.glob(os.path.join(base, "Microsoft Visual Studio", "*", "*", "Common7", "IDE", "CommonExtensions",
                                             "Microsoft", "TeamFoundation", "Team Explorer", "Git", "cmd", "git.exe"))
    places = [p for p in places if os.path.isfile(p)]
    return sorted(places)[-1] if places else None


GIT = find_git()


def git_in(folder, *args, stdin=None, err=False):
    """Run one git command in folder, reading only. Give back (exit code, what it printed), or (None, "") with no Git."""
    if not GIT:
        return (None, "", "") if err else (None, "")
    try:
        done = subprocess.run([GIT, "--no-optional-locks", *args], cwd=folder, input=stdin, capture_output=True,
                              text=True, encoding="utf-8", errors="replace")
    except OSError:
        return (None, "", "") if err else (None, "")
    out = done.stdout.replace("\r\n", "\n")
    return (done.returncode, out, done.stderr) if err else (done.returncode, out)


def git(*args, stdin=None):
    return git_in(HERE, *args, stdin=stdin)


def exists(ref):
    return git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")[0] == 0


def sha_of(ref):
    code, out = git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
    return out.strip() if code == 0 else None


def is_ancestor(a, b):
    return git("merge-base", "--is-ancestor", a, b)[0] == 0


def current_branch():
    code, out = git("symbolic-ref", "--short", "-q", "HEAD")
    return out.strip() if code == 0 else None


def same(a, b):
    return os.path.normcase(os.path.realpath(a)) == os.path.normcase(os.path.realpath(b))


# ------------------------------------------------------------------ where this folder is
def where():
    """(the problem, or None; and what check needs to read the repository). The folder has to be called SponsorTracker
    and be in a repository: your Year2-Programming one, or (if you have none) a repository of its own."""
    name = os.path.basename(os.path.realpath(HERE))
    if name.lower() != PROJECT.lower():
        return (f"these files are in a folder called {name}, not {PROJECT}: rename the folder {PROJECT} (right-click it "
                "in File Explorer, Rename), then open it again in VS Code"), None
    if GIT is None:
        return "Git was not found on this PC: tell your teacher", None
    code, top, said = git_in(HERE, "rev-parse", "--show-toplevel", err=True)
    if code != 0:
        if "dubious ownership" in said:
            return "Git says detected dubious ownership: the folder is on a network drive. Move it into OneDrive, then open it again", None
        return (f"{PROJECT} is not in your {YEAR} repository: extract the zip again, and Browse to the python folder "
                f"inside {YEAR} (Task 2a, step 1)"), None
    top = os.path.normpath(top.strip())
    if same(top, HERE):
        above = git_in(os.path.dirname(HERE), "rev-parse", "--show-toplevel")
        if above[0] == 0:
            return (f"{PROJECT} has become a repository of its own inside {os.path.basename(os.path.normpath(above[1].strip()))}: "
                    "tell your teacher before you go on"), None
    elif os.path.basename(top).lower() != YEAR.lower():
        return f"the repository here is {top}, not your {YEAR} folder: tell your teacher before you go on", None
    rel = git("rev-parse", "--show-prefix")[1].strip()
    main = "main" if exists("refs/heads/main") or not exists("refs/heads/master") else "master"
    remotes = git("remote")[1].split()
    return None, {"top": top, "rel": rel, "main": main, "origin": "origin" in remotes,
                  "origin_main": sha_of(f"refs/remotes/origin/{main}"), "main_sha": sha_of(f"refs/heads/{main}")}


def journey():
    """HEAD's reflog, oldest first: [commit, what happened, the branch HEAD was on]. It is how Git remembers which branch
    each commit was made on, even after a merge has made two branches alike."""
    code, out = git("reflog", "show", "--format=%H%x09%gs", "HEAD")
    if code != 0:
        return []
    steps = [line.split("\t", 1) for line in reversed(out.splitlines()) if "\t" in line]
    moves = [re.match(r"checkout: moving from (\S+) to (\S+)$", w) for _, w in steps]
    renames = [re.match(r"Branch: renamed refs/heads/(\S+) to refs/heads/(\S+)$", w) for _, w in steps]
    first = next(((m or r).group(1) for m, r in zip(moves, renames) if m or r), None)
    if first is None:
        first = current_branch() or ""
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


# ------------------------------------------------------------------ running your code
class RanOut(BaseException):
    """It asked for another answer after the last one: it refused something it should have given back."""


class TooLong(BaseException):
    """A loop that never stops."""


def no_input(prompt=""):
    raise RanOut()


def load(source, name):
    """Read one version of a file as Python. Give back (the module, None) or (None, why not)."""
    folder = tempfile.mkdtemp(prefix="checked-")
    try:
        path = os.path.join(folder, f"{name}.py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(source)
        spec = importlib.util.spec_from_file_location(f"{name}_checked", path)
        module = importlib.util.module_from_spec(spec)
        try:
            compile(source, path, "exec")
        except SyntaxError as e:
            return None, (f"{name}.py has a line Python cannot read (line {e.lineno}): run python {name}.py to see it, "
                          "then finish that line, or put # in front of the lines you have not finished")
        result, printed, e = call(spec.loader.exec_module, [], module)
        if isinstance(e, RanOut):
            return None, f"{name}.py asks a question as soon as it is read: keep main() under if __name__ == \"__main__\":"
        if isinstance(e, TooLong):
            return None, f"{name}.py runs a loop as soon as it is read, and it never stops: keep main() under if __name__ == \"__main__\":"
        if e:
            return None, f"{name}.py stops with {type(e).__name__} before the checks can reach it: {e}"
        return module, None
    finally:
        shutil.rmtree(folder, ignore_errors=True)


def call(fn, answers, *args):
    """Run fn(*args) with the answers typed in, one each time it asks. Give back (what it gave back, what it printed,
    the error or None). A loop that never stops is stopped, and says so."""
    todo = list(answers)

    def typed(prompt=""):
        if not todo:
            raise RanOut()
        return todo.pop(0)

    steps = [0]

    def tracer(frame, event, arg):
        if event == "line":
            steps[0] += 1
            if steps[0] > 200000:
                raise TooLong()
        return tracer

    out = Capped()
    builtins.input = typed
    sys.settrace(tracer)
    try:
        with contextlib.redirect_stdout(out):
            result = fn(*args)
        return result, out.getvalue(), None
    except BaseException as e:
        if isinstance(e, KeyboardInterrupt):
            raise
        return None, out.getvalue(), e
    finally:
        sys.settrace(None)
        builtins.input = REAL_INPUT


@contextlib.contextmanager
def folder_with(files):
    """A folder of its own holding these files ({name: text}), as the current folder while the code runs."""
    folder, back = tempfile.mkdtemp(prefix="checked-run-"), os.getcwd()
    try:
        for name, text in files.items():
            with open(os.path.join(folder, name), "w", encoding="utf-8") as f:
                f.write(text)
        os.chdir(folder)
        yield folder
    finally:
        os.chdir(back)
        shutil.rmtree(folder, ignore_errors=True)


def lines_of(printed):
    return [line.strip() for line in printed.split("\n") if line.strip()]


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def crashed(e, what):
    if isinstance(e, TooLong):
        return f"after {what} it goes round and round and never stops: each loop must ask again, or end"
    if isinstance(e, RanOut):
        return f"after {what} it asked for another answer: it refused an answer it should have given back"
    return f"{what} makes it stop with {type(e).__name__}: {e}"


def function_source(source, name):
    """One function's lines as the file has them, tidied, or "" when there is no such function (None: unreadable)."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            text = ast.get_source_segment(source, node) or ""
            return "\n".join(line.rstrip() for line in text.split("\n")).strip()
    return ""


def fingerprint(text):
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()[:12]


def functions_in(source, names):
    """The top-level functions with these names, as the file has them (none when it cannot be read)."""
    try:
        tree = ast.parse(source or "")
    except SyntaxError:
        return []
    return [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names]


def bare_except(source, names):
    """The first of these functions with a bare except: (or except BaseException:), which catches the checks' own
    signals as well as the error it was written for; None when there is none."""
    for node in functions_in(source, names):
        for h in ast.walk(node):
            if isinstance(h, ast.ExceptHandler) and (h.type is None or (isinstance(h.type, ast.Name) and h.type.id == "BaseException")):
                return node.name
    return None


def round_and_round(source, names, what):
    """The FIX for a loop that goes round and round after `what`. A bare except: is named first: it swallows the
    checks' own signals, so the slip behind it cannot be seen until it is gone."""
    name = bare_except(source, names)
    if name:
        return (f"after {what} it goes round and round: {name} has a bare except:, which catches everything, even the "
                "check's own signals. Write except ValueError:, so only the error you expect is caught, then check again")
    return f"after {what} it goes round and round without asking again: read the answer inside the loop"


def resets_in_loop(source, name):
    """True when the function sets a name back to a number inside one of its loops (total = 0 on every pass)."""
    for node in functions_in(source, (name,)):
        for loop in ast.walk(node):
            if isinstance(loop, (ast.For, ast.While)):
                for inner in loop.body:
                    for n in ast.walk(inner):
                        if isinstance(n, ast.Assign) and isinstance(n.value, ast.Constant) and number(n.value.value):
                            return True
    return False


# ------------------------------------------------------------------ a part: its change, and where the change has got to
class Part:
    """One part of the task: the file it changes, the test its change must pass, how to tell it is not started, the branch
    the sheet names for it, and the step to go back to."""

    def __init__(self, label, name, file, test, untouched, branch, called=None, funcs=(), key=None):
        self.label, self.name, self.file, self.test, self.untouched, self.branch = label, name, file, test, untouched, branch
        self.called = called or f"Task {label}"          # how the sheet names it: Task 2b, or the stretch's step 1a
        self.script = None                               # the check script that runs this part's test: report() sets it
        self.funcs = tuple(funcs)                        # the functions the change is made in
        self._key = key                                  # or, for a file that is not Python, what the change is

    def passes(self, source):
        return results(self.file, source)[self.label]

    def key(self, source):
        """The part's own change, as text: a squash merge is matched to its branch's commit on it."""
        if self._key:
            return self._key(source or "") or ""
        return "\n".join(function_source(source or "", f) or "" for f in self.funcs).strip()


# Your code runs in a Python of its own with a time limit, one version of a file at a time, every part's test on it in
# turn, each verdict printed the moment it is known: a loop that never stops (a bare except: can swallow the checks' own
# signals) is stopped by the limit, the part still running then is the one named, and only the parts after it are run
# again, so each such version costs one limit, not one per part. Every other version and part is still checked.
REGISTRY, RESULTS, LIMIT = {}, {}, 8
RUNAWAY = "it goes round and round and never stops, whatever is typed: each loop must ask again, or end"


def runaway(part, source):
    """The FIX for a part whose test never finished: a bare except: in its functions is named, because it is the usual cause."""
    name = bare_except(source, part.funcs)
    if name:
        return (f"it goes round and round and never stops: {name} has a bare except:, which catches everything, even the "
                "check's own stop. Write except ValueError:, so only the error you expect is caught, then check again")
    return RUNAWAY


def run_tests(labels, source, script):
    """Run the tests named in labels on source in a Python of its own, in that order. Give back ({label: (ok, why)} for
    every test that finished, and the label of the one still running when the time ran out, or None)."""
    folder = tempfile.mkdtemp(prefix="checked-src-")
    path = os.path.join(folder, "source.txt")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(source)
        try:
            done = subprocess.run([sys.executable, "-B", script, "--probe", ",".join(labels), path], cwd=HERE,
                                  capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=LIMIT)
            out, said, late = done.stdout, done.stderr, False
        except subprocess.TimeoutExpired as stopped:     # what it printed before the limit comes with it
            out, said, late = stopped.stdout or "", "", True
            if isinstance(out, bytes):
                out = out.decode("utf-8", "replace")
        got = {}
        for line in out.splitlines():
            if line.startswith("PROBE "):
                try:
                    label, verdict = json.loads(line[len("PROBE "):])
                    got[label] = (bool(verdict[0]), str(verdict[1]))
                except (ValueError, TypeError, IndexError):
                    pass
        missing = [label for label in labels if label not in got]
        if late:
            return got, (missing[0] if missing else None)
        if missing:
            said = (said.strip().splitlines() or ["no answer"])[-1]
            got.update({label: (False, f"the check could not run: {said}") for label in missing})
        return got, None
    finally:
        shutil.rmtree(folder, ignore_errors=True)


def results(file, source):
    """Every part's verdict on this version of this file, worked out once."""
    key = (file, fingerprint(source))
    if key not in RESULTS:
        parts = [p for p in REGISTRY.values() if p.file == file]
        got, todo = {}, [p.label for p in parts]
        while todo:
            done, late = run_tests(todo, source or "", parts[0].script)
            got.update(done)
            if late is None:
                break
            got[late] = (False, runaway(REGISTRY[late], source or ""))   # the part that never stopped
            todo = todo[todo.index(late) + 1:]                              # and only the parts after it run again
        RESULTS[key] = got
    return RESULTS[key]


class Capped(io.StringIO):
    """What a program prints, up to a limit: a loop that prints for ever stops here rather than filling the memory."""

    def write(self, text):
        if self.tell() > 200000:
            raise TooLong()
        return super().write(text)


def probe(parts, argv):
    """In the Python of its own: run each named part's test on the file given, in the order named, and print each
    verdict on a line of its own the moment it is known, so the parts that finished are known if the time runs out."""
    labels, path = argv[argv.index("--probe") + 1].split(","), argv[argv.index("--probe") + 2]
    with open(path, encoding="utf-8") as f:
        source = f.read()
    by_label = {part.label: part for part in parts}
    for label in labels:
        part = by_label.get(label)
        if part is None:
            continue
        try:
            ok, why = part.test(source)
        except BaseException as e:                       # a check that cannot run says so rather than stopping the others
            ok, why = False, (runaway(part, source) if isinstance(e, TooLong) else f"the check could not run: {type(e).__name__}: {e}")
        sys.__stdout__.write("PROBE " + json.dumps([label, [bool(ok), why]]) + "\n")
        sys.__stdout__.flush()


def working(file):
    try:
        with open(os.path.join(HERE, file), encoding="utf-8", errors="replace") as f:
            return f.read().replace("\r\n", "\n")
    except OSError:
        return None


class Repo:
    """What the repository holds, read once: the reflog, which branch each commit was made on, and each commit's copy of
    a file, fetched in one go and only when a part needs it."""

    def __init__(self, info):
        self.info, self.rows = info, journey()
        main = info["main"]
        made = [(sha, on) for sha, what, on in self.rows if what.startswith("commit")]
        shas = list(dict.fromkeys(sha for sha, on in made))
        if shas:                                         # only the commits still in the repository (an amended one may have gone)
            found = git("cat-file", "--batch-check", stdin="".join(f"{sha}\n" for sha in shas))[1].split("\n")
            shas = [sha for k, sha in enumerate(shas) if k < len(found) and found[k].split()[1:2] == ["commit"]]
        self.parents = {}
        if shas:
            code, out = git("rev-list", "--no-walk=unsorted", "--parents", *shas)
            for row in (out.split("\n") if code == 0 else []):
                if row.strip():
                    first, *rest = row.split()
                    self.parents[first] = rest
        # oldest first: (commit, branch) made off main, and the single-parent commits made on main
        self.branch_made = [(sha, on) for sha, on in made if on != main]
        self.main_made = [sha for sha, on in made if on == main and len(self.parents.get(sha, [])) == 1]
        self.blobs, self.texts = {}, {}

    def fetch(self, shas, file):
        """Look up this file in every commit given, with one git command."""
        todo = [sha for sha in dict.fromkeys(shas) if sha and (sha, file) not in self.blobs]
        if not todo:
            return
        code, out = git("cat-file", "--batch-check", stdin="".join(f"{sha}:{self.info['rel']}{file}\n" for sha in todo))
        answers = out.split("\n")
        for k, sha in enumerate(todo):
            words = answers[k].split() if k < len(answers) else []
            self.blobs[(sha, file)] = words[0] if len(words) >= 2 and words[1] == "blob" else None

    def source(self, sha, file):
        if not sha:
            return None
        self.fetch([sha], file)
        blob = self.blobs[(sha, file)]
        if blob is None:
            return None
        if blob not in self.texts:
            self.texts[blob] = git("cat-file", "blob", blob)[1]
        return self.texts[blob]


def verdict(part, repo, info, problem):
    """(PASS, FIX or -, why) for one part: first where its change has got to, then what the code in the folder does."""
    here = working(part.file)
    code_ok, code_why = part.passes(here) if here is not None else (False, f"{part.file} is not in this folder")
    if problem:
        if here is None or (not code_ok and part.untouched(here)):
            return "-", "not started yet"
        if code_ok:
            return "FIX", "it works: now put SponsorTracker right (Task 2a), so the change can go on a branch"
        return "FIX", code_why
    main, O, M = info["main"], info["origin_main"], info["main_sha"]
    redo = f"then do {part.called} again from its first step, starting with the branch"
    repo.fetch([sha for sha, on in repo.branch_made] + repo.main_made + [O, M] +
               [repo.parents[sha][0] for sha in repo.main_made], part.file)

    def good(sha):
        return part.passes(repo.source(sha, part.file) or "")[0]

    good_branch = [(sha, on) for sha, on in repo.branch_made if good(sha)]
    # a commit made on main that made the part work; not the commit that brought the project in, which is the starting point
    good_main = [sha for sha in repo.main_made if good(sha) and repo.source(repo.parents[sha][0], part.file) is not None]
    # a squash merge (GitHub Desktop's Squash and merge) is one new commit on main holding the branch's change, with no
    # link back to the branch: matched to a branch commit on the part's own change, it counts as merged from that branch
    keys = {sha: part.key(repo.source(sha, part.file)) for sha, on in good_branch}
    squashed = {}
    for msha in good_main:
        mine = part.key(repo.source(msha, part.file))
        twin = next(((sha, on) for sha, on in good_branch if mine and keys[sha] == mine), None)
        if twin:
            squashed[msha] = twin
    straight = (f"that change went straight onto {main}, not onto a branch: in GitHub Desktop, History, right-click it, "
                f"Revert changes in commit, then Push origin; {redo}")
    for tip, kind in ((O, "github"), (M, "main")):
        if not tip or not good(tip):
            continue
        reached = [(sha, on) for sha, on in good_branch if is_ancestor(sha, tip)]
        reached += [twin for msha, twin in squashed.items() if is_ancestor(msha, tip)]
        if not reached and any(is_ancestor(sha, tip) for sha in good_main):
            return "FIX", straight
        if kind == "github":
            return "PASS", (f"done on {reached[0][1]}, merged into {main}, and on GitHub" if reached else f"on {main}, and on GitHub")
        if not info["origin"]:
            return "FIX", f"merged into {main}, and your repository is not on GitHub yet: Publish repository (Task 2a)"
        return "FIX", f"merged into {main}, not on GitHub yet: click Push origin"
    if good_branch:
        landed = {twin[0] for msha, twin in squashed.items() if M and is_ancestor(msha, M)}
        waiting = [(sha, on) for sha, on in good_branch if not (M and is_ancestor(sha, M)) and sha not in landed]
        if waiting:
            branch = waiting[-1][1]
            return "FIX", (f"done and committed on {branch}, not merged into {main} yet: Current branch, {main}, then Branch, "
                           f"Merge into current branch, choose {branch}; then Push origin")
        why = part.passes(repo.source(M, part.file) or "")[1]
        return "FIX", (f"{main} had the change from {good_branch[0][1]}, and a later commit undid it (History in GitHub Desktop "
                       f"shows which). Now: {why}")
    if here is None:
        return "FIX", f"{part.file} is not in this folder: take it from the zip again"
    if code_ok:
        now = current_branch()
        if now in (None, main):
            return "FIX", (f"it works, and it is not committed yet: make its branch first (Current branch, New branch, "
                           f"{part.branch}, and bring your changes), then Commit to {part.branch}")
        return "FIX", f"it works, and it is not committed yet: in GitHub Desktop, type a summary, then Commit to {now}"
    if part.untouched(here):
        if good_main:
            return "-", f"undone: now do {part.called} again from its first step, starting with the branch"
        return "-", "not started yet"
    return "FIX", code_why


# ------------------------------------------------------------------ the tests: what each change has to do
STARTER = {   # each function as the zip gave it, so a part nobody has touched shows a dash rather than a FIX
    "total_raised": "d2632169507e",
    "ask_amount": "c42df4b7c9c8",
    "show_progress": "f615ad7b9a30",
    "main": "dd68d5acded8",
}


def as_given(source, name):
    return fingerprint(function_source(source, name)) == STARTER[name]


def sponsor_module(source):
    return load(source, "sponsor")


def test_total(source):
    mod, why = sponsor_module(source)
    if mod is None:
        return False, why
    fn = getattr(mod, "total_raised", None)
    if fn is None:
        return False, "total_raised is missing: the progress needs it to add up the sponsors"
    for sponsors, want, what in [([["A", 20.0], ["B", 10.0], ["C", 5.5]], 35.5, "three sponsors, £20.00, £10.00 and £5.50"),
                                 ([], 0, "no sponsors at all"), ([["A", 12.5]], 12.5, "one sponsor")]:
        got, printed, e = call(fn, [], copy.deepcopy(sponsors))
        if e:
            return False, crashed(e, what)
        if got is None:
            return False, f"with {what} it gives back None: return total once, after the loop has finished"
        if not number(got):
            return False, f"with {what} it gives back {got!r}: give back the total, a number"
        if abs(got - want) > 1e-9:
            if want == 35.5 and abs(got - 20.0) < 1e-9:
                return False, ("only the first sponsor is added: the return is inside the for loop, so it gives back "
                               "after one pass. Move it out, level with for")
            if want == 35.5 and abs(got - 5.5) < 1e-9:
                if resets_in_loop(source, "total_raised"):
                    return False, ("only the last sponsor counts: the total goes back to 0 on every pass of the loop. "
                                   "Set total = 0 once, before the loop")
                return False, "only the last sponsor counts: add each amount to the total (total = total + amount)"
            if want == 35.5 and abs(got - 15.5) < 1e-9:
                return False, "the first sponsor is missed: the loop must add every sponsor, the first one too"
            return False, f"with {what} it gives back {got!r}, and it should give back {want}"
    return True, "the total counts every sponsor"


LOW_AMOUNT = re.compile(r"(?<![\d.])1(?:\.0+)?(?!\d)")       # 1, or 1.00, but never the 1 in 10 or in 0.1
HIGH_AMOUNT = re.compile(r"(?<![\d.])500(?:\.0+)?(?!\d)")


def test_amount(source):
    mod, why = sponsor_module(source)
    if mod is None:
        return False, why
    fn = getattr(mod, "ask_amount", None)
    if fn is None:
        return False, "ask_amount is missing: adding a sponsor needs it"
    for typed, want, what in [("10", 10.0, "10"), ("7.50", 7.5, "7.50"), ("  12  ", 12.0, "12 with spaces round it"),
                              ("1", 1.0, "1, the lowest amount"), ("500", 500.0, "500, the highest amount")]:
        got, printed, e = call(fn, [typed], "Amount in pounds: ")
        if isinstance(e, RanOut):
            if typed in ("1", "500"):
                return False, (f"{typed} is refused, and it is on the edge and allowed (valid extreme): the range is from "
                               "1 to 500, both included, so use <=")
            if typed == "7.50":
                return False, "7.50 is refused: read the amount with float(), which reads pence"
            return False, f"{what} is refused, and it is a good amount"
        if isinstance(e, TooLong):
            return False, round_and_round(source, ("ask_amount",), what)
        if e:
            return False, crashed(e, what)
        if isinstance(got, str):
            return False, f"{what} comes back as text, {got!r}: give back the number, float(text)"
        if not number(got) or abs(got - want) > 1e-9:
            return False, f"{what} gives back {got!r}, and it should give back {want}"
    said, usual = {}, set(lines_of(call(fn, ["10"], "Amount in pounds: ")[1]))   # what it prints for a good answer
    for typed, what in [("£10", "£10"), ("ten", "ten"), ("", "a blank"), ("-5", "-5"), ("0", "0"), ("0.99", "0.99"),
                        ("500.01", "500.01"), ("501", "501")]:
        got, printed, e = call(fn, [typed, "10"], "Amount in pounds: ")
        if isinstance(e, ValueError):
            return False, (f"{what} still stops the program with ValueError: put float() inside try, and except ValueError "
                           "after it, with a message that says what to type")
        if isinstance(e, TooLong):
            return False, round_and_round(source, ("ask_amount",), what)
        if isinstance(e, RanOut):
            return False, f"after {what} it refused 10 as well: only an answer outside 1 to 500, or not a number, is refused"
        if e:
            return False, crashed(e, what)
        if number(got) and abs(got - 10.0) > 1e-9:
            if typed in ("-5", "0", "0.99", "500.01", "501"):
                return False, f"{what} gets in: check the range where the amount comes in, from 1 to 500"
            return False, f"{what} gets in: it is not an amount"
        if not number(got):                              # it refused, then gave back without asking for 10
            return False, (f"after {what} it gives back {got!r} and does not ask again: put the input inside a while True "
                           "loop, so it asks until the amount passes")
        shown = [line for line in lines_of(printed) if line not in usual]
        if not shown:
            return False, f"{what} is refused with no message: print what to type, then ask again"
        said[typed] = " ".join(shown)
    # each refusal says the rule it broke: a single range message (Type 1 to 500.) names both ends; a pair names its own
    if not LOW_AMOUNT.search(said["-5"]):
        return False, "the message for -5 must say the rule, with the lowest amount, 1, in it: like Type 1 to 500."
    if not HIGH_AMOUNT.search(said["501"]):
        return False, "the message for 501 must say the rule, with the highest amount, 500, in it: like Type 1 to 500."
    if said["£10"] == said["-5"]:
        return False, "£10 and -5 get the same message: £10 is not a number at all, so tell them to type numbers, like 10 or 7.50"
    return True, "£10, ten, a blank, -5, 0 and 501 are refused, each with a message; 1, 7.50 and 500 get in"


def test_still(source):
    mod, why = sponsor_module(source)
    if mod is None:
        return False, why
    fn = getattr(mod, "show_progress", None)
    if fn is None:
        return False, "show_progress is missing: choosing 3 needs it"

    mod.total_raised = lambda sponsors: sum(amount for name, amount in sponsors)   # Bug 1's fix is 2b's, not this part's

    def shown(total, target=None):
        if target is not None:
            mod.TARGET = target
        got, printed, e = call(fn, [], [["Test", total]])
        mod.TARGET = 200.00
        return printed, e

    printed, e = shown(82.5)
    if e:
        return False, crashed(e, "£82.50 raised")
    if not re.search(r"Raised: £82\.50 of £200\.00", printed):
        return False, "keep the Raised line, Raised: £82.50 of £200.00 (41%), above the new line"
    if "Still to raise: £117.50" not in printed:
        if "117.5" in printed:
            return False, "show it in pounds to two places, like this: Still to raise: £117.50"
        return False, "with £82.50 raised it does not say Still to raise: £117.50 under the Raised line"
    for total, what in [(200.0, "exactly £200.00"), (250.0, "£250.00")]:
        printed, e = shown(total)
        if e:
            return False, crashed(e, f"{what} raised")
        if "Still to raise" in printed and "target reached" in printed.lower():
            return False, (f"with {what} raised it prints Target reached! and Still to raise together: put the Still to "
                           "raise line under else, so only one of the two lines prints")
        if "Still to raise" in printed:
            if total == 200.0:
                return False, "exactly £200.00 is the target reached: the check is total >= TARGET"
            return False, "over the target it still shows Still to raise: once the total is the target or more, say Target reached!"
        if "target reached" not in printed.lower():
            return False, f"with {what} raised it should say Target reached!"
    printed, e = shown(82.5, target=100.0)
    if "Still to raise: £17.50" not in printed:
        return False, "it still works it out from 200 when TARGET changes: use TARGET, not 200, so the target is typed once"
    printed, e = shown(150.0, target=100.0)              # over a changed target: the comparison must use TARGET too
    if e:
        return False, crashed(e, "£150.00 raised")
    if "target reached" not in printed.lower() or "Still to raise" in printed:
        return False, ("with TARGET changed to 100, £150.00 should say Target reached!: compare the total with TARGET, "
                       "not 200, so the target is typed once")
    return True, "Still to raise under the Raised line, and Target reached! from £200.00"


MENU_FILE = "A,5.00\nB,25.00\nC,25.00\nD,1.00\n"


def test_top(source):
    mod, why = sponsor_module(source)
    if mod is None:
        return False, why
    fn = getattr(mod, "top_sponsor", None)
    if fn is None:
        return False, "there is no top_sponsor yet: write top_sponsor(sponsors), which gives back the sponsor who gave the most"
    for sponsors, want, what in [([["A", 5.0], ["B", 25.0], ["C", 25.0], ["D", 1.0]], ["B", 25.0], "B and C both £25.00"),
                                 ([["A", 9.0], ["B", 2.0]], ["A", 9.0], "the biggest first"),
                                 ([["A", 1.0], ["B", 2.0]], ["B", 2.0], "the biggest last"),
                                 ([["A", 3.0]], ["A", 3.0], "one sponsor")]:
        got, printed, e = call(fn, [], copy.deepcopy(sponsors))
        if e:
            return False, crashed(e, what)
        if isinstance(got, tuple):
            got = list(got)
        if got != want:
            if what.startswith("B and C") and got == ["C", 25.0]:
                return False, "on a tie it gives back the last: keep the first of two equal amounts (use >, not >=)"
            if got == ["D", 1.0] or got == ["A", 1.0]:
                return False, "it gives back the smallest amount: a sponsor takes the top place only with a bigger amount (>)"
            if got in ("B", "A") or got in (25.0, 9.0, 2.0, 3.0):
                return False, f"it gives back {got!r}: give back the whole sponsor, [name, amount], so the menu can show both"
            return False, f"with {what} it gives back {got!r}, and it should give back {want!r}"
    main = getattr(mod, "main", None)
    if main is None:
        return False, "main is missing"
    with folder_with({"sponsors.txt": MENU_FILE}):
        got, printed, e = call(main, ["4", "0"])
    if isinstance(e, RanOut):
        return False, "choosing 4 asks for more than the menu choice: option 4 shows the top sponsor, then the menu comes back"
    if e:
        return False, crashed(e, "choosing 4")
    if not any(re.match(r"4\b", line) for line in lines_of(printed)):
        return False, "the menu does not show option 4: add print(\"4 Show the top sponsor\") to the menu"
    if "Top sponsor: B, £25.00" not in printed:
        return False, "choosing 4 should print the top sponsor like this: Top sponsor: B, £25.00 (their name, then the amount to two places)"
    with folder_with({"sponsors.txt": ""}):
        got, printed, e = call(main, ["4", "0"])
    if e:
        return False, "with no sponsors yet, choosing 4 " + (crashed(e, "choosing 4") if isinstance(e, RanOut) else f"stops with {type(e).__name__}") + ": say No sponsors yet."
    if "no sponsors yet" not in printed.lower():
        return False, "with no sponsors yet, choosing 4 should say No sponsors yet."
    return True, "top_sponsor gives back the first of the biggest; option 4 shows it, or No sponsors yet"


def top_untouched(source):
    return "top_sponsor" not in (source or "") and as_given(source, "main")


PARTS = [
    Part("2b", "Bug 1: the total", "sponsor.py", test_total, lambda s: as_given(s, "total_raised"), "fix-total",
         funcs=("total_raised",)),
    Part("2c", "Bug 2: check the amount", "sponsor.py", test_amount, lambda s: as_given(s, "ask_amount"), "check-amount",
         funcs=("ask_amount",)),
    Part("2d", "Feature 1: still to raise", "sponsor.py", test_still, lambda s: as_given(s, "show_progress"), "still-to-raise",
         funcs=("show_progress",)),
    Part("2e", "Feature 2: the top sponsor", "sponsor.py", test_top, top_untouched, "top-sponsor", funcs=("top_sponsor", "main")),
]
FILES = ["sponsor.py", "sponsors.txt", "check.py", "README.md"]


def check_2a(problem, info):
    if problem:
        return "FIX", problem
    main, rel = info["main"], info["rel"]

    def holds(ref):
        names = set(git("ls-tree", "-r", "--full-name", "--name-only", ref, "--", ".")[1].split("\n"))
        return all(f"{rel}{f}" in names for f in FILES)

    if not exists(f"refs/heads/{main}") or not holds(main):
        others = [b for b in git("for-each-ref", "--format=%(refname:short)", "refs/heads")[1].split() if b != main]
        elsewhere = next((b for b in others if holds(b)), None)
        if elsewhere:
            return "FIX", (f"SponsorTracker is committed on {elsewhere}, not on {main}: Current branch, {main}, then Branch, "
                           f"Merge into current branch, choose {elsewhere}")
        kept = []                                        # a .gitignore line (*.txt, say) that keeps a project file out of every commit
        for f in FILES:
            code, out = git("check-ignore", "-v", f)
            bits = out.split("\t")[0].split(":", 2) if code == 0 else []   # .gitignore:2:*.txt, then a tab and the file
            if len(bits) == 3:
                kept.append((f, bits[0], bits[2]))
        if kept:
            names = " and ".join(f for f, where, pattern in kept)
            where, pattern = kept[0][1], kept[0][2]
            place = where if "/" in where else f"{os.path.basename(info['top'])}'s {where}"
            return "FIX", (f"{names} {'is' if len(kept) == 1 else 'are'} kept out of every commit by the line {pattern} in "
                           f"{place}: change that line so it names only the file it was for (like receipt.txt), save it, "
                           f"then commit on {main}")
        return "FIX", (f"SponsorTracker is not in a commit on {main} yet: in GitHub Desktop, Current branch {main}, then type "
                       f"the summary Add the sponsor tracker as it came, and click Commit to {main}")
    if not info["origin"]:
        return "FIX", ("committed, and your repository is not on GitHub yet: click Publish repository, keep Keep this code "
                       "private ticked, then Publish repository")
    if not info["origin_main"] or not holds(f"refs/remotes/origin/{main}"):
        return "FIX", f"committed on {main}, not on GitHub yet: click Push origin"
    return "PASS", f"SponsorTracker is committed on {main}, and {main} is on GitHub"


def report(parts, first=None, prefix="", goes="copy it into the exit ticket, question two"):
    """Print each part's line and the results line. first: a part of its own (2a here) put in front of the others."""
    for part in parts:
        part.script = os.path.abspath(sys.argv[0])
        REGISTRY[part.label] = part
    print("Checking your code and your repository...", flush=True)
    problem, info = where()
    repo = Repo(info) if info else None
    results = []
    if first:
        results.append((first[0], first[1], *first[2](problem, info)))
    for part in parts:
        results.append((part.label, part.name, *verdict(part, repo, info, problem)))
    for label, name, result, why in results:
        print(f"{result:<5} {label}  {name}: {why}")
    print()
    print(f"Your results line ({goes}):")
    print(prefix + "  ".join(f"{label} {result}" for label, name, result, why in results))


if __name__ == "__main__":
    if "--probe" in sys.argv:
        probe(PARTS, sys.argv)
    else:
        report(PARTS, first=("2a", "Put the project on GitHub", check_2a), prefix="SponsorTracker: ")
