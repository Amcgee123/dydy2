# Task 2b: your test plan for ask_count("How many arrived? ", 1, 50) in delivery.py.
# For each thing the manager might type, fill in both gaps:
#   accepted or rejected: what ask_count does with it
#   the kind of test data: valid, valid extreme, invalid, invalid extreme or erroneous
# The first row is done for you. Predict every row first, then run python try_count.py and type each one in.
# Then run python check.py.

TESTS = [
    # (what is typed, accepted or rejected, kind of test data)
    ("12", "accepted", "valid"),
    ("50", "", ""),
    ("51", "", ""),
    ("1", "", ""),
    ("0", "", ""),
    ("200", "", ""),
    ("ten", "", ""),
]
