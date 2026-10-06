# SponsorTracker

Your cousin is running the Great North Run for the local animal rescue, and started this program to keep track of the sponsors. It runs, and it nearly works.

Run it: python sponsor.py
Check your work: python check.py
The stretch task's program: python training.py, checked by python check_stretch.py

## Bug reports

Bug 1: the total stops at the first sponsor.
Run it and choose 3, Show the progress. It says Raised: £20.00 of £200.00 (10%).
The six sponsors in sponsors.txt add up to £82.50, so it should say Raised: £82.50 of £200.00 (41%).

Bug 2: the amount is not checked where it comes in.
Choose 2 and add a sponsor. Type £10 for the amount, and the program stops with ValueError.
Type -5, and it is taken: sponsors.txt gains a line for -5.00.
An amount must be a number of pounds from 1 to 500, pence allowed (like 7.50). Anything else is refused with a message that says what to type, and the program asks again.

## Wanted

Feature 1: how much is still to raise.
Under the Raised line, show Still to raise: £117.50, or Target reached! once the total is £200.00 or more.

Feature 2: the top sponsor.
A new menu option, 4 Show the top sponsor, that shows the sponsor who gave the most, like this: Top sponsor: The chippy, £25.00
If two gave the same, show the first of them. With no sponsors yet, it says No sponsors yet.
