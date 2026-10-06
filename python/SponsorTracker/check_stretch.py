# TrainingLog: the checks for the stretch task. Run it in the terminal with:  python check_stretch.py
# It reads training.py, README.md and your repository, and prints PASS, FIX or a dash (not started yet) for each step,
# then a results line to post in the class chat. A step reads PASS once it works, was committed on a branch, is merged
# into main, and main is on GitHub, just like Task 2. It uses check.py, so keep the two together.
# Do not change this file.
import sys

sys.dont_write_bytecode = True
import os
import re

from check import (Part, call, crashed, folder_with, fingerprint, function_source, lines_of, load, number, probe, report,
                   round_and_round, RanOut, TooLong)

LOW_RUN = re.compile(r"(?<![\d.])0?\.5(?!\d)")            # 0.5 (or .5), the shortest run, named in its message
HIGH_RUN = re.compile(r"(?<![\d.])20(?:\.0+)?(?!\d)")     # 20, the longest, but never the 20 in 20.1 or 200

STARTER = {   # each function as the zip gave it, so a step nobody has touched shows a dash rather than a FIX
    "longest_run": "dbe04fa90875",
    "ask_miles": "50a5e96eb517",
    "main": "981e54c28ae1",
}


def as_given(source, name):
    return fingerprint(function_source(source, name)) == STARTER[name]


def training(source):
    return load(source, "training")


def test_longest(source):
    mod, why = training(source)
    if mod is None:
        return False, why
    fn = getattr(mod, "longest_run", None)
    if fn is None:
        return False, "longest_run is missing"
    for runs, want, what in [([3.0, 4.5, 2.5, 6.0, 5.0], 6.0, "the runs in runs.txt"), ([7.0, 1.0], 7.0, "the longest first"),
                             ([1.0, 9.5], 9.5, "the longest last"), ([2.0], 2.0, "one run")]:
        got, printed, e = call(fn, [], list(runs))
        if e:
            return False, crashed(e, what)
        if not number(got) or abs(got - want) > 1e-9:
            if number(got) and abs(got - min(runs)) < 1e-9:
                return False, "it gives back the shortest run: a run takes the place of the longest only when it is longer (>)"
            return False, f"with {what} it gives back {got!r}, and it should give back {want}"
    return True, "it gives back the longest run, wherever it is in the list"


def test_miles(source):
    mod, why = training(source)
    if mod is None:
        return False, why
    fn = getattr(mod, "ask_miles", None)
    if fn is None:
        return False, "ask_miles is missing"
    for typed, want, what in [("3.5", 3.5, "3.5"), ("0.5", 0.5, "0.5, the shortest run"), ("20", 20.0, "20, the longest run"),
                              (" 13.1 ", 13.1, "13.1 with spaces round it")]:
        got, printed, e = call(fn, [typed], "Today's run, in miles: ")
        if isinstance(e, RanOut):
            if typed in ("0.5", "20"):
                return False, f"{typed} is refused, and it is on the edge and allowed (valid extreme): use <="
            return False, f"{what} is refused, and it is a good run"
        if isinstance(e, TooLong):
            return False, round_and_round(source, ("ask_miles",), what)
        if e:
            return False, crashed(e, what)
        if not number(got) or abs(got - want) > 1e-9:
            return False, f"{what} gives back {got!r}, and it should give back {want}"
    said, usual = {}, set(lines_of(call(fn, ["3.5"], "Today's run, in miles: ")[1]))
    for typed, what in [("five", "five"), ("", "a blank"), ("0", "0"), ("0.4", "0.4"), ("20.1", "20.1"), ("-3", "-3")]:
        got, printed, e = call(fn, [typed, "3.5"], "Today's run, in miles: ")
        if isinstance(e, ValueError):
            return False, f"{what} still stops the program with ValueError: put float() inside try, and except ValueError after it"
        if isinstance(e, TooLong):
            return False, round_and_round(source, ("ask_miles",), what)
        if isinstance(e, RanOut):
            return False, f"after {what} it refused 3.5 as well: only a run outside 0.5 to 20, or not a number, is refused"
        if e:
            return False, crashed(e, what)
        if number(got) and abs(got - 3.5) > 1e-9:
            return False, f"{what} gets in: a run is a number of miles from 0.5 to 20"
        if not number(got):                              # it refused, then gave back without asking for 3.5
            return False, (f"after {what} it gives back {got!r} and does not ask again: put the input inside a while True "
                           "loop, so it asks until the run passes")
        shown = [line for line in lines_of(printed) if line not in usual]
        if not shown:
            return False, f"{what} is refused with no message: print what to type, then ask again"
        said[typed] = " ".join(shown)
    # each refusal says the rule it broke: one range message names both ends; a pair of messages names its own end each
    if not LOW_RUN.search(said["0.4"]):
        return False, "the message for 0.4 must say the rule, with the shortest run, 0.5, in it: like Type a run from 0.5 to 20 miles."
    if not HIGH_RUN.search(said["20.1"]):
        return False, "the message for 20.1 must say the rule, with the longest run, 20, in it: like Type a run from 0.5 to 20 miles."
    if said["five"] == said["20.1"]:
        return False, "five and 20.1 get the same message: five is not a number at all, so tell them to type numbers, like 3.5"
    return True, "five, a blank, 0, 0.4, 20.1 and -3 are refused, each with a message; 0.5, 3.5 and 20 get in"


def runs_in(folder):
    with open(os.path.join(folder, "runs.txt"), encoding="utf-8") as f:
        text = f.read()
    try:
        return [float(line) for line in text.split("\n") if line.strip()], text
    except ValueError:
        return None, text


def test_save(source):
    mod, why = training(source)
    if mod is None:
        return False, why
    fn = getattr(mod, "save_run", None)
    if fn is None:
        return False, "there is no save_run yet: write save_run(filename, miles), which adds the run to the end of the file"
    with folder_with({"runs.txt": "3.0\n"}) as folder:
        for miles in (4.5, 2.5):
            got, printed, e = call(fn, [], "runs.txt", miles)
            if e:
                return False, crashed(e, f"saving {miles}")
        runs, text = runs_in(folder)
    if runs is None:
        return False, f"runs.txt now holds {text!r}: put each run on a line of its own (write f\"{{miles}}\\n\")"
    if runs == [2.5]:
        return False, "the runs already in the file were lost: open the file with \"a\" to add to the end, not \"w\""
    if runs != [3.0, 4.5, 2.5]:
        return False, f"after saving 4.5 and 2.5, runs.txt reads {runs}: it should read [3.0, 4.5, 2.5]"
    main = getattr(mod, "main", None)
    with folder_with({"runs.txt": "3.0\n4.5\n"}) as folder:
        got, printed, e = call(main, ["2.5"])
        runs, text = runs_in(folder)
    if e:
        return False, crashed(e, "running main with 2.5")
    if runs != [3.0, 4.5, 2.5]:
        return False, "main does not save today's run: call save_run(RUNS_FILE, miles) after the run is added"
    return True, "each run is added to the end of runs.txt, and main saves today's run"


def test_total(source):
    mod, why = training(source)
    if mod is None:
        return False, why
    fn = getattr(mod, "total_miles", None)
    if fn is None:
        return False, "there is no total_miles yet: write total_miles(runs), which gives back the total to one decimal place"
    for runs, want, what in [([3.0, 4.5, 2.5], 10.0, "3.0, 4.5 and 2.5"), ([0.1, 0.2], 0.3, "0.1 and 0.2"), ([], 0, "no runs")]:
        got, printed, e = call(fn, [], list(runs))
        if e:
            return False, crashed(e, what)
        if got is None:
            return False, f"with {what} it gives back None: return the total; do not print it"
        if not number(got):
            return False, f"with {what} it gives back {got!r}: give back a number"
        if got != want:
            if abs(got - want) < 1e-6:
                return False, f"{what} gives back {got!r}: round it to one decimal place, round(total, 1)"
            return False, f"with {what} it gives back {got!r}, and it should give back {want}"
    main = getattr(mod, "main", None)
    with folder_with({"runs.txt": "3.0\n4.5\n"}):
        got, printed, e = call(main, ["2.5"])
    if e:
        return False, crashed(e, "running main with 2.5")
    if "Total: 10.0 miles" not in printed:
        return False, "main does not show the total: at its end, print it like this: Total: 10.0 miles"
    return True, "total_miles gives back the total to one place, and main shows it"


COMPARE = re.compile(r"^#+\s*compare\b", re.I)


def compare_section(source):
    lines, text, inside = (source or "").split("\n"), [], False
    for line in lines:
        if COMPARE.match(line.strip()):
            inside = True
            continue
        if inside and line.strip().startswith("#"):
            break
        if inside:
            text.append(line)
    return " ".join(text).strip() if inside else None


def test_compare(source):
    text = compare_section(source)
    if text is None:
        return False, "README.md has no heading ## Compare yet"
    words = re.findall(r"[A-Za-z']+", text)
    if len(words) < 40:
        return False, f"the Compare section has {len(words)} words: write at least 40, on the points you compare them on"
    low = text.lower()
    if not re.search(r"\bboth\b|\bsimilarly\b|\balike\b", low):
        return False, "say how the two are alike: Both... or Similarly..."
    if not re.search(r"\bwhereas\b|\bwhile\b|\bbut\b|\bunlike\b|\bhowever\b|\bcompared (with|to)\b", low):
        return False, "say how they differ, both named in one sentence: ... whereas ..."
    if not re.search(r"\bsav(e|es|ed|ing)\b", low):
        return False, "compare the two ways of saving: each run as it is typed, and every run once at the end"
    return True, "the Compare section is there, with how they are alike and how they differ (read by your teacher, not by this check)"


PARTS = [
    Part("1a", "The longest run", "training.py", test_longest, lambda s: as_given(s, "longest_run"), "fix-longest", called="step 1a",
         funcs=("longest_run",)),
    Part("1b", "Check the miles", "training.py", test_miles, lambda s: as_given(s, "ask_miles"), "check-miles", called="step 1b",
         funcs=("ask_miles",)),
    Part("2a", "Save each run", "training.py", test_save, lambda s: "save_run" not in (s or "") and as_given(s, "main"), "save-runs",
         called="step 2a", funcs=("save_run", "main")),
    Part("2b", "The total", "training.py", test_total, lambda s: "total_miles" not in (s or ""), "total-miles", called="step 2b",
         funcs=("total_miles", "main")),
    Part("2c", "Compare, in README.md", "README.md", test_compare, lambda s: compare_section(s) is None, "compare", called="step 2c",
         key=lambda s: compare_section(s) or ""),
]

if __name__ == "__main__":
    if "--probe" in sys.argv:
        probe(PARTS, sys.argv)
    else:
        report(PARTS, prefix="Stretch: ", goes="post it in the class chat")
