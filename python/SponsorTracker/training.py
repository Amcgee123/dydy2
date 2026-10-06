# TrainingLog: your cousin's training runs for the Great North Run, in miles.
# Each run is kept in runs.txt, one to a line, like this: 3.5
#
# Run it:          python training.py
# Check your work: python check_stretch.py
# The stretch task sheet has its two bug reports and what to add.

RUNS_FILE = "runs.txt"


# Reads runs.txt into a list of runs, in miles.
def load_runs(filename):
    runs = []
    with open(filename) as file:
        for line in file.readlines():
            runs.append(float(line.strip()))
    return runs


# Asks for today's run, in miles, and gives it back.
def ask_miles(prompt):
    text = input(prompt).strip()
    return float(text)


# Gives back the longest run so far.
def longest_run(runs):
    longest = runs[0]
    for miles in runs:
        if miles < longest:
            longest = miles
    return longest


def main():
    runs = load_runs(RUNS_FILE)
    print(f"Runs so far: {len(runs)}")
    print(f"Longest run: {longest_run(runs)} miles")
    miles = ask_miles("Today's run, in miles: ")
    runs.append(miles)
    print(f"Runs so far: {len(runs)}")
    print(f"Longest run: {longest_run(runs)} miles")


# This line runs main() when you run this file, and not when check_stretch.py reads it.
if __name__ == "__main__":
    main()
