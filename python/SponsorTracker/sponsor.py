# SponsorTracker: the sponsorship for a charity run.
# Your cousin is running the Great North Run for the local animal rescue, and started this program.
# Each sponsor is a name and an amount in pounds, kept in sponsors.txt, one to a line, like this: Nana,10.00
#
# Run it:          python sponsor.py
# Check your work: python check.py
# The bug reports, and the features your cousin wants next, are in README.md.

TARGET = 200.00
SPONSOR_FILE = "sponsors.txt"


# Reads sponsors.txt into a list of sponsors, each one [name, amount].
def load_sponsors(filename):
    sponsors = []
    with open(filename) as file:
        for line in file.readlines():
            name, amount = line.strip().split(",")
            sponsors.append([name, float(amount)])
    return sponsors


# Adds one sponsor to the end of sponsors.txt.
def save_sponsor(filename, name, amount):
    with open(filename, "a") as file:
        file.write(f"{name},{amount:.2f}\n")


# Asks until the name passes both checks, then gives it back.
def ask_name(prompt):
    while True:
        name = input(prompt).strip()
        if name == "":
            print("You left it blank. Type the sponsor's name.")
        elif "," in name:
            print("Leave out commas: sponsors.txt uses them to split each line.")
        else:
            return name


# Asks for an amount in pounds, and gives it back.
def ask_amount(prompt):
    text = input(prompt).strip()
    return float(text)


# Adds up every sponsor's amount, and gives back the total.
def total_raised(sponsors):
    total = 0
    for name, amount in sponsors:
        total = total + amount
        return total


# The total as a percentage of the target, to the nearest whole number.
def percent_raised(total):
    return round(total / TARGET * 100)


def show_sponsors(sponsors):
    for name, amount in sponsors:
        print(f"{name}: £{amount:.2f}")


def show_progress(sponsors):
    total = total_raised(sponsors)
    percent = percent_raised(total)
    print(f"Raised: £{total:.2f} of £{TARGET:.2f} ({percent}%)")


def main():
    sponsors = load_sponsors(SPONSOR_FILE)
    print("Sponsor tracker")
    while True:
        print()
        print("1 Show the sponsors")
        print("2 Add a sponsor")
        print("3 Show the progress")
        print("0 Quit")
        choice = input("Choose: ").strip()
        if choice == "1":
            show_sponsors(sponsors)
        elif choice == "2":
            name = ask_name("Sponsor's name: ")
            amount = ask_amount("Amount in pounds: ")
            sponsors.append([name, amount])
            save_sponsor(SPONSOR_FILE, name, amount)
            print(f"Thank you, {name}: £{amount:.2f} added.")
        elif choice == "3":
            show_progress(sponsors)
        elif choice == "0":
            print("Bye for now.")
            return
        else:
            print("Type 1, 2, 3 or 0.")


# This line runs main() when you run this file, and not when check.py reads it.
if __name__ == "__main__":
    main()
