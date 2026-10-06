// TripsManager: stage 05, 05 - Iteration P2. Rung: 1 · Copy the model.
// WHAT CHANGED SINCE LAST TIME:
//   The first state. The Coach Trip from lesson 03's stretch has become a trips desk: one trip, its cost per head, its capacity, and a menu.
//   Every lesson from now on opens the project as the last lesson left it; this file's top comment says what changed each time.

// TRIPS MANAGER: the college trips and visits manager.
// One program, grown one lesson at a time from lesson 05 to lesson 18. Your starter is always the project as the
// last lesson left it, so you never need your own copy of last lesson's work.
//
// HOW TO WORK. Run it first. The top of every run is the CHECK HARNESS: each part of today's task prints PASS, FIX or
// a dash (not started yet), then your RESULTS LINE, which the exit ticket asks you to paste. After the checks, the
// trips desk runs for real. Today's parts are the methods marked YOUR TURN; each sits under the finished method it
// copies. Under each YOUR TURN heading is a "My prediction:" line: before you write the method, type what its check
// will want from it, then write, run and compare. Nothing else in the file is yours to change today.

const string TRIP = "Edinburgh: the Royal Mile and the Castle";
const decimal COST_PER_HEAD = 48.50m;
const int CAPACITY = 12;     // a minibus, small on purpose, so the desk fills up while you test it

// ---------------------------------------------------------------- the check harness. Do not change this part.
// It runs each of today's methods with fixed input, catches what they print or return, and compares.
string Capture(Action run, string typed)
{
    TextReader oldIn = Console.In; TextWriter oldOut = Console.Out;
    StringWriter caught = new StringWriter();
    Console.SetIn(new StringReader(typed + string.Concat(Enumerable.Repeat("done\n", 20))));
    Console.SetOut(caught);
    try { run(); } finally { Console.SetIn(oldIn); Console.SetOut(oldOut); }
    return caught.ToString().Replace("\r\n", "\n");
}
int pass = 0, fail = 0;
string Check(string part, string what, string got, string want, bool started)
{
    if (!started) { Console.WriteLine($"-     {part}  {what}: not started yet"); return "-"; }
    bool ok = got == want;
    if (ok) pass++; else fail++;
    Console.WriteLine($"{(ok ? "PASS" : "FIX ")}  {part}  {what}   got {Show(got)}   want {Show(want)}");
    return ok ? "PASS" : "FIX";
}
string Show(string s) => s.Replace("\n", " / ").TrimEnd(' ', '/');
string Overall(params string[] verdicts) => verdicts.All(v => v == "-") ? "-" : (verdicts.All(v => v == "PASS") ? "PASS" : "FIX");

Console.WriteLine("CHECKS");
// Task 2a: the price list, three party sizes at 48.50 a head
string priceList = Capture(() => PriceList(3, 48.50m), "");
string v2a = Check("2a", "price list for 3 seats", priceList, "Party of 1: £48.50\nParty of 2: £97.00\nParty of 3: £145.50\n", priceList.Length > 0);
// Task 2b: bookings stop at done, and stop at capacity
int bookedA = -1, bookedB = -1;
Capture(() => { bookedA = TakeBookings(12); }, "L2043\nL2044\nL2045\ndone\n");
Capture(() => { bookedB = TakeBookings(2); }, "L2043\nL2044\nL2045\nL2046\n");
string v2b = Overall(
    Check("2b", "three references then done", bookedA.ToString(), "3", bookedA != -1),
    Check("2b", "a minibus of 2 fills up", bookedB.ToString(), "2", bookedB != -1));
// Task 2c: capital letters in a reference
int uA = CountUpper("L2043"), uB = CountUpper("l2043"), uC = CountUpper("LEEDS");
string v2c = Overall(
    Check("2c", "capitals in L2043", uA.ToString(), "1", uA != -1),
    Check("2c", "capitals in l2043", uB.ToString(), "0", uB != -1),
    Check("2c", "capitals in LEEDS", uC.ToString(), "5", uC != -1));
Console.WriteLine($"{pass} of {pass + fail} checks PASS");
Console.WriteLine();
Console.WriteLine("Your results line (copy it into the exit ticket, question two):");
Console.WriteLine($"2a {v2a}  2b {v2b}  2c {v2c}");
Console.WriteLine();

// ---------------------------------------------------------------- the trips desk (given: not yours to change today)
// A do...while loop: the menu shows at least once, then again while the choice is not 0. Python has no do...while.
Console.WriteLine($"TRIPS DESK  {TRIP}  £{COST_PER_HEAD:F2} a head, {CAPACITY} seats");
string choice;
do
{
    Console.WriteLine();
    Console.WriteLine("1 Seat plan   2 Price list   3 Deposits   4 Take bookings   5 Check a reference   0 Quit");
    Console.Write("Choose: ");
    choice = Console.ReadLine();
    switch (choice)
    {
        case "1":
            SeatPlan(CAPACITY);
            break;
        case "2":
            PriceList(CAPACITY, COST_PER_HEAD);
            break;
        case "3":
            decimal banked = CollectDeposits(COST_PER_HEAD * CAPACITY);
            Console.WriteLine($"Banked £{banked:F2} of £{COST_PER_HEAD * CAPACITY:F2}.");
            break;
        case "4":
            int booked = TakeBookings(CAPACITY);
            Console.WriteLine($"{booked} booked, {CAPACITY - booked} seats left.");
            break;
        case "5":
            Console.Write("Reference: ");
            string reference = Console.ReadLine();
            bool accepted = reference.Length == 5 && CountDigits(reference) == 4 && CountUpper(reference) == 1;
            Console.WriteLine(accepted ? "Accepted." : "Rejected: a reference is one capital letter and four digits, like L2043.");
            break;
        case "0":
            Console.WriteLine("Desk closed.");
            break;
        default:
            Console.WriteLine("Not on the menu.");
            break;
    }
} while (choice != "0");

// ================================================================ Task 2a: a count-controlled loop, twice
// THE MODEL, finished: the seat plan, one line per seat from 1 to the capacity.
// A for loop: start; keep going while; step. seat <= capacity is inclusive, Python's range(1, capacity + 1).
static void SeatPlan(int capacity)
{
    for (int seat = 1; seat <= capacity; seat++)
    {
        Console.WriteLine($"Seat {seat}: free");
    }
}

// YOUR TURN, Task 2a: the price list, one line per party size from 1 to the capacity, each line
// "Party of 3: £145.50" (the size times the cost per head, two decimal places).
// The same shape as SeatPlan, one thing changed: what each line prints.
// My prediction:
static void PriceList(int capacity, decimal costPerHead)
{
    // Task 2a: your for loop goes here. Look up at SeatPlan: same start, same test, same step.
    // Until you write it, this method prints nothing, and the check shows a dash.
}

// ================================================================ Task 2b: a condition-controlled loop, twice
// THE MODEL, finished: the desk takes deposits until the target is reached, or until it types done.
// A while loop: the condition is tested BEFORE each go, and the body must change what the condition tests
// (total grows, or entry becomes done), or the loop never ends.
static decimal CollectDeposits(decimal target)
{
    decimal total = 0m;
    string entry = "";
    while (total < target && entry != "done")
    {
        Console.Write("Deposit (or done): ");
        entry = Console.ReadLine();
        if (decimal.TryParse(entry, out decimal amount))
        {
            total = total + amount;
        }
    }
    return total;
}

// YOUR TURN, Task 2b: the desk takes learner references until the minibus is full, or until it types done,
// and gives back how many it booked. The prompt is "Learner reference (or done): ".
// The same shape as CollectDeposits, one thing changed: it counts bookings instead of adding up money.
// My prediction:
static int TakeBookings(int capacity)
{
    // Task 2b: your while loop goes here. Look up at CollectDeposits: the condition is tested before each go,
    // and the body must change what the condition tests. Count the references; stop at capacity or at done.
    return -1;   // -1 means not started yet: replace it with the count you built
}

// ================================================================ Task 2c: a loop over every character, twice
// THE MODEL, finished: how many digits a learner reference has. A foreach loop walks every character of the
// string in order, one at a time, and you cannot change the string inside it. Python's for letter in text.
// char.IsDigit(c) is true for 0 to 9.
static int CountDigits(string text)
{
    int digits = 0;
    foreach (char c in text)
    {
        if (char.IsDigit(c))
        {
            digits = digits + 1;
        }
    }
    return digits;
}

// YOUR TURN, Task 2c: how many capital letters a reference has, so the desk can tell L2043 from l2043 and LEEDS.
// The same shape as CountDigits, one thing changed: the test inside the if (char.IsUpper(c) is true for A to Z).
// My prediction:
static int CountUpper(string text)
{
    // Task 2c: your foreach loop goes here. Look up at CountDigits: the same walk over every character,
    // one thing changed inside the if.
    return -1;   // -1 means not started yet: replace it with the count you built
}
