// TripsManager: stage 07b, 01 - Methods P2. Rung: 2 · Fill the gap.
// WHAT CHANGED SINCE LAST TIME:
//   Moved: PartyCost and PaymentStatus, finished, into the Program class near the bottom of the file, so each can have a second version with the same name.
//   New: a second PaymentStatus and a second PartyCost under them for you to finish; the desk shows each seat's status and what the booked seats pay.

// TRIPS MANAGER: the college trips and visits manager.
// One program, grown one lesson at a time from lesson 05 to lesson 18. Your starter is the project as the last lesson
// left it, with the changes since then named at the top of this file, so you never need your own copy of last
// lesson's work.
//
// HOW TO WORK. Run it with Ctrl+F5 (Start Without Debugging), first and after every change: the checks are built to
// run without the debugger. The top of every run is the CHECK HARNESS: each part of today's task prints PASS, FIX or a
// dash (not started yet), then your RESULTS LINE, which the exit ticket asks you to paste. After the checks, the trips
// desk runs for real, and it uses each of today's methods once its checks read PASS.
// Today's parts are the two methods marked YOUR TURN, in the Program class near the bottom of the file: press Ctrl+F
// and search for YOUR TURN. Each has the same name as the finished method just above it, with different parameters.
// Its header, its comment, the place the desk calls it and its check are written for you: you write the body, between
// its braces. Under each YOUR TURN heading is a "My prediction:" line: before you write the body, type what its check
// will want from it, then write, run and compare. Nothing else in the file is yours to change today.

const int CAPACITY = 12;     // the college minibus: every trip goes in it, so every trip has twelve seats

// ---------------------------------------------------------------- the check harness. Do not change this part.
// It runs each of today's methods with fixed values, catches what they print or give back, and compares. A method
// that stops with an error, waits for typing, prints without end or is still running after two seconds is stopped
// there, and its check says so instead of hanging. Each of today's methods is read before it runs (Reading, at the
// bottom of the file): one that calls itself with the same arguments would never stop, so it is named and not run.
bool runaway = false;
string Capture(Action run)
{
    TextReader oldIn = Console.In; TextWriter oldOut = Console.Out;
    Typing typing = new Typing("");
    Capped caught = new Capped();
    string stopped = "";
    Console.SetIn(typing);
    Console.SetOut(caught);
    Thread worker = new Thread(() =>
    {
        try { run(); }
        catch (RanOutOfTyping) { stopped = "[stopped: it waited for typing. Today's methods get everything they need as parameters]"; }
        catch (TooMuchPrinted) { stopped = "[stopped: it printed far too much. Does the loop ever stop?]"; }
        catch (Exception e) { stopped = $"[stopped with {e.GetType().Name}]"; }
    });
    worker.IsBackground = true;
    worker.Start();
    if (!worker.Join(2000))
    {
        stopped = "[stopped: still running after two seconds. Does the loop ever stop?]";
        runaway = true;
    }
    Console.SetIn(oldIn); Console.SetOut(oldOut);
    return stopped != "" ? stopped : caught.ToString().Replace("\r\n", "\n");
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
string Show(string s) => s == "" ? "\"\"" : s.Replace("\n", " / ").TrimEnd(' ', '/');
string Overall(params string[] verdicts) => verdicts.All(v => v == "-") ? "-" : (verdicts.All(v => v == "PASS") ? "PASS" : "FIX");
string Stopped(string printed) => printed.Contains("[stopped") ? printed.Substring(printed.IndexOf("[stopped")) : "";
// What a method gave back, and anything it printed as well: a method that gives back must not print instead.
string Given(string printed, string value) => Stopped(printed) != "" ? Stopped(printed) : (printed != "" ? $"{Show(value)}, and it printed {Show(printed)}" : value);
// A method that calls itself with the same arguments is named, never run: it would call itself for ever.
string CallsItself(string part, string call, string instead)
{
    fail++;
    Console.WriteLine($"FIX   {part}  it calls itself: {call} runs this same method again, and again, so the check did not run it. {instead}");
    return "FIX";
}

Console.WriteLine("CHECKS");
// Task 2a: a second PaymentStatus, from a learner's reference, passing its work to the first
string bodyA = Reading.BodyOf("static string PaymentStatus(Dictionary<string, decimal> paid, string reference, decimal costPerHead)");
List<string[]> callsA = Reading.CallsTo("PaymentStatus", bodyA);
bool selfA = callsA.Any(c => c.Length == 3);     // three arguments fit only this PaymentStatus: it would call itself
bool onA = callsA.Any(c => c.Length == 2);       // two fit the first PaymentStatus, just above it
// Two trips' costs, so a method that passes £48.50 instead of the cost per head it was given is caught.
Dictionary<string, decimal> paidA = new Dictionary<string, decimal>();
paidA["L2043"] = 15.75m;
paidA["L2051"] = 20.00m;
string a1 = "", a2 = "", a3 = "", pa1 = "", pa2 = "", pa3 = "";
if (!selfA)
{
    pa1 = Capture(() => { a1 = PaymentStatus(paidA, "L2051", 48.50m); });
    pa2 = Capture(() => { a2 = PaymentStatus(paidA, "L2043", 15.75m); });
    pa3 = Capture(() => { a3 = PaymentStatus(paidA, "L2060", 48.50m); });
}
bool startedA = selfA || onA || a1 + a2 + a3 != "" || pa1 + pa2 + pa3 != "";
string v2a = selfA
    ? CallsItself("2a", "PaymentStatus(paid, reference, costPerHead)", "Give the first PaymentStatus two arguments: what they have paid, and the cost per head.")
    : Overall(new[] {
        Check("2a", "L2051 has paid £20.00 of £48.50", Given(pa1, a1), "part paid", startedA),
        Check("2a", "L2043 has paid £15.75 of £15.75", Given(pa2, a2), "paid in full", startedA),
        Check("2a", "L2060 has paid nothing yet", Given(pa3, a3), "not paid", startedA) }
        .Concat(bodyA == "" ? new string[0] : new[] {
        Check("2a", "passes its work to the first PaymentStatus", onA ? "a call to it" : "no call to it", "a call to it", startedA) }).ToArray());
// Task 2b: a second PartyCost, from the seats, counting who is booked and passing its work to the first
string bodyB = Reading.BodyOf("static decimal PartyCost(string[] seats, decimal costPerHead)");
List<string[]> callsB = Reading.CallsTo("PartyCost", bodyB);
// The seats again, however they are passed, is this same PartyCost: seats itself, an array the body declares
// (string[] booked = seats;), or an array a call makes (...ToArray(), new string[] ...). A number of people is the first.
List<string> arraysB = Reading.ArraysIn(bodyB);
arraysB.Add("seats");
bool SeatsAgain(string arg)
{
    string a = arg.Replace(" ", "");
    return arraysB.Contains(a) || a.EndsWith("ToArray()") || a.StartsWith("newstring[") || a.StartsWith("new[]");
}
bool selfB = callsB.Any(c => c.Length == 2 && SeatsAgain(c[0]));   // the seats again: this same PartyCost
bool onB = callsB.Any(c => c.Length == 2 && !SeatsAgain(c[0]));     // a number of people: the first PartyCost
string selfCallB = callsB.Any(c => c.Length == 2 && c[0] == "seats") ? "PartyCost(seats, costPerHead)" : "PartyCost given an array of the seats";
string[] twelve = new string[CAPACITY];
for (int i = 0; i < twelve.Length; i++)
{
    twelve[i] = $"L{2043 + i}";
}
decimal b1 = -1m, b2 = -1m, b3 = -1m;
string pb1 = "", pb2 = "", pb3 = "";
if (!selfB)
{
    pb1 = Capture(() => { b1 = PartyCost(new string[] { "L2043", "L2051", "", "L2060" }, 48.50m); });
    pb2 = Capture(() => { b2 = PartyCost(new string[] { "", "", "" }, 48.50m); });
    pb3 = Capture(() => { b3 = PartyCost(twelve, 15.75m); });
}
bool startedB = selfB || onB || b1 != -1m || b2 != -1m || b3 != -1m || pb1 + pb2 + pb3 != "";
string v2b = selfB
    ? CallsItself("2b", selfCallB, "Give the first PartyCost the number of people you counted, and the cost per head.")
    : Overall(new[] {
        Check("2b", "L2043, L2051, a free seat and L2060 at £48.50", Given(pb1, $"£{b1:F2}"), "£145.50", startedB),
        Check("2b", "three free seats at £48.50", Given(pb2, $"£{b2:F2}"), "£0.00", startedB),
        Check("2b", "twelve booked at £15.75", Given(pb3, $"£{b3:F2}"), "£189.00", startedB) }
        .Concat(bodyB == "" ? new string[0] : new[] {
        Check("2b", "passes its work to the first PartyCost", onB ? "a call to it" : "no call to it", "a call to it", startedB) }).ToArray());
Console.WriteLine($"{pass} of {pass + fail} checks PASS");
Console.WriteLine();
Console.WriteLine("Your results line (copy it into the exit ticket, question two):");
Console.WriteLine($"2a {v2a}  2b {v2b}");
Console.WriteLine();
if (runaway)
{
    Console.WriteLine("A method was still running when its check stopped it, so the desk does not open this run.");
    Console.WriteLine("Find the loop whose condition never becomes false, fix it, and run again.");
    return;
}

// ---------------------------------------------------------------- the trips desk (given: not yours to change today)
// The desk's data. The trips on offer: a Dictionary, each trip's name the key and its cost per head the value.
// The minibus: an array of seats, "" for a free one, twelve and never more. The waiting list: a List, which grows.
// What each learner has paid so far: a Dictionary, the learner reference the key and the amount the value.
// The desk uses each of today's methods only once its checks read PASS, so a method with a slip never runs here.
string NotYet(bool started) => started ? "does not pass its checks yet" : "gives back nothing yet";
Dictionary<string, decimal> trips = new Dictionary<string, decimal>();
trips["Edinburgh"] = 48.50m;
trips["York"] = 22.00m;
trips["Whitby"] = 15.75m;
string trip = "Edinburgh";
decimal costPerHead = trips[trip];
string[] seats = new string[CAPACITY];
for (int i = 0; i < seats.Length; i++)
{
    seats[i] = "";
}
List<string> waiting = new List<string>();
Dictionary<string, decimal> paid = new Dictionary<string, decimal>();

// A do...while loop: the menu shows at least once, then again while the choice is not 0.
string choice;
do
{
    Console.WriteLine();
    // Task 2b's call: what the seats booked so far pay, on the desk's top line once 2b's checks read PASS.
    string bookedCost = v2b == "PASS" ? $"; the seats booked pay £{PartyCost(seats, costPerHead):F2}" : "";
    Console.WriteLine($"TRIPS DESK  {trip}  £{costPerHead:F2} a head (£{PartyCost(CAPACITY, costPerHead):F2} for a full minibus{bookedCost})  {CAPACITY} seats  {waiting.Count} waiting");
    Console.WriteLine("1 Trips on offer   2 Choose a trip   3 Price list   4 Take bookings   5 Seat plan");
    Console.WriteLine("6 Record a payment   7 Payments   8 Waiting list   9 Receipt   0 Quit");
    Console.Write("Choose: ");
    choice = Console.ReadLine();
    switch (choice)
    {
        case "1":
            foreach (KeyValuePair<string, decimal> offer in trips)
            {
                Console.WriteLine($"{offer.Key}: £{offer.Value:F2} a head");
            }
            break;
        case "2":
            Console.Write("Which trip? ");
            string name = Console.ReadLine();
            decimal price = PriceOf(trips, name);
            if (price < 0)
            {
                Console.WriteLine($"{name} is not on offer: option 1 lists the trips.");
            }
            else
            {
                trip = name;
                costPerHead = price;
                for (int i = 0; i < seats.Length; i++)
                {
                    seats[i] = "";
                }
                waiting.Clear();
                paid.Clear();
                Console.WriteLine($"Now booking {trip}: an empty minibus, nobody waiting, no payments yet.");
            }
            break;
        case "3":
            PriceList(CAPACITY, costPerHead);
            break;
        case "4":
            foreach (string reference in TakeBookingList(CAPACITY))
            {
                bool looksRight = reference.Length == 5 && CountDigits(reference) == 4 && CountUpper(reference) == 1;
                int already = SeatOf(seats, reference);
                if (!looksRight)
                {
                    Console.WriteLine($"{reference}: rejected, a reference is one capital letter and four digits, like L2043.");
                }
                else if (already > 0)
                {
                    Console.WriteLine($"{reference}: already booked, in seat {already}.");
                }
                else
                {
                    int free = FirstFreeSeat(seats);
                    if (free == 0)
                    {
                        waiting.Add(reference);
                        Console.WriteLine($"{reference}: the minibus is full, so number {waiting.Count} on the waiting list.");
                    }
                    else
                    {
                        seats[free - 1] = reference;
                        Console.WriteLine($"{reference}: seat {free}.");
                    }
                }
            }
            break;
        case "5":
            for (int i = 0; i < seats.Length; i++)
            {
                Console.WriteLine($"Seat {i + 1}: {(seats[i] == "" ? "free" : seats[i])}");
            }
            // Task 2b's call again, under the seat plan.
            Console.WriteLine(v2b == "PASS" ? $"The seats booked pay £{PartyCost(seats, costPerHead):F2}." : $"What the seats booked pay: Task 2b {NotYet(startedB)}.");
            break;
        case "6":
            Console.Write("Learner reference: ");
            string who = Console.ReadLine();
            if (SeatOf(seats, who) == 0)
            {
                Console.WriteLine($"{who} is not booked on this trip: nothing recorded.");
                break;
            }
            Console.Write("Amount: £");
            if (decimal.TryParse(Console.ReadLine(), out decimal amount) && amount > 0)
            {
                if (paid.ContainsKey(who))
                {
                    paid[who] = paid[who] + amount;
                }
                else
                {
                    paid[who] = amount;
                }
                Console.WriteLine($"{who} has paid £{paid[who]:F2} of £{costPerHead:F2}.");
            }
            else
            {
                Console.WriteLine("That is not an amount: nothing recorded.");
            }
            break;
        case "7":
            List<string> inFull = PaidInFull(paid, costPerHead);
            Console.WriteLine($"Paid in full: {(inFull.Count == 0 ? "nobody yet" : string.Join(" ", inFull))}");
            List<string> partPaid = PartPaid(paid, costPerHead);
            Console.WriteLine($"Part paid: {(partPaid.Count == 0 ? "nobody" : string.Join(" ", partPaid))}");
            for (int i = 0; i < seats.Length; i++)
            {
                if (seats[i] != "")
                {
                    decimal owes = Balance(paid, seats[i], costPerHead);
                    // Task 2a's call: each seat's status from its reference, once 2a's checks read PASS.
                    string status = v2a == "PASS" ? $": {PaymentStatus(paid, seats[i], costPerHead)}" : "";
                    Console.WriteLine(owes < 0 ? $"Seat {i + 1}  {seats[i]} is £{-owes:F2} in credit{status}" : $"Seat {i + 1}  {seats[i]} owes £{owes:F2}{status}");
                }
            }
            if (v2a != "PASS")
            {
                Console.WriteLine($"Each seat's status: Task 2a {NotYet(startedA)}.");
            }
            Console.WriteLine($"Still to collect: £{StillToCollect(seats, paid, costPerHead):F2}");
            break;
        case "8":
            Console.WriteLine("References for the waiting list, then done.");
            foreach (string joiner in ReadReferences())
            {
                waiting.Add(joiner);
            }
            if (waiting.Count == 0)
            {
                Console.WriteLine("Nobody is waiting.");
            }
            else
            {
                Console.WriteLine($"{waiting.Count} waiting: first {waiting[0]}, last {waiting[^1]}.");
            }
            break;
        case "9":
            Console.Write("Learner reference: ");
            string whose = Console.ReadLine();
            if (SeatOf(seats, whose) == 0)
            {
                Console.WriteLine($"{whose} is not booked on this trip: no receipt.");
                break;
            }
            paid.TryGetValue(whose, out decimal sofar);
            PrintReceipt(whose, sofar, costPerHead);
            break;
        case "0":
            Console.WriteLine("Desk closed.");
            break;
        default:
            Console.WriteLine("Not on the menu.");
            break;
    }
} while (choice != "0");

// ================================================================ finished in lesson 07: methods

// One learner's receipt, on two lines: a void method, its status from PaymentStatus.
static void PrintReceipt(string reference, decimal paid, decimal costPerHead)
{
    string status = PaymentStatus(paid, costPerHead);
    Console.WriteLine($"Receipt for {reference}");
    Console.WriteLine($"Paid £{paid:F2} of £{costPerHead:F2}: {status}");
}

// How much is still to collect: Balance for every seated learner, added up, a credit counted as nothing.
static decimal StillToCollect(string[] seats, Dictionary<string, decimal> paid, decimal costPerHead)
{
    decimal total = 0m;
    foreach (string reference in seats)
    {
        decimal owes = Balance(paid, reference, costPerHead);
        if (reference != "" && owes > 0) { total = total + owes; }
    }
    return total;
}

// ================================================================ finished in lesson 06: the desk's collections
// Which seat a reference sits in, from 1 to the number of seats, or 0 when it is not on the minibus: an array.
static int SeatOf(string[] seats, string reference)
{
    for (int i = 0; i < seats.Length; i++)
    {
        if (seats[i] == reference)
        {
            return i + 1;
        }
    }
    return 0;
}

// The first free seat, from 1 to the number of seats, or 0 when the minibus is full: an array.
static int FirstFreeSeat(string[] seats)
{
    for (int i = 0; i < seats.Length; i++)
    {
        if (seats[i] == "")
        {
            return i + 1;
        }
    }
    return 0;
}

// Learner references typed until done, kept in a List in the order they were typed: a while loop and Add.
static List<string> ReadReferences()
{
    List<string> typed = new List<string>();
    string entry = "";
    while (entry != "done")
    {
        Console.Write("Learner reference (or done): ");
        entry = Console.ReadLine();
        if (entry != "done")
        {
            typed.Add(entry);
        }
    }
    return typed;
}

// The bookings for one trip in a List: references until done, or until the List holds a minibus-full.
static List<string> TakeBookingList(int capacity)
{
    List<string> booked = new List<string>();
    string entry = "";
    while (booked.Count < capacity && entry != "done")
    {
        Console.Write("Learner reference (or done): ");
        entry = Console.ReadLine();
        if (entry != "done")
        {
            booked.Add(entry);
        }
    }
    return booked;
}

// The learners who have paid the whole cost per head or more: a foreach over a Dictionary, each Key kept in a List.
static List<string> PaidInFull(Dictionary<string, decimal> paid, decimal costPerHead)
{
    List<string> done = new List<string>();
    foreach (KeyValuePair<string, decimal> pair in paid)
    {
        if (pair.Value >= costPerHead)
        {
            done.Add(pair.Key);
        }
    }
    return done;
}

// The learners who have paid something but not the whole cost per head: a foreach over a Dictionary.
static List<string> PartPaid(Dictionary<string, decimal> paid, decimal costPerHead)
{
    List<string> part = new List<string>();
    foreach (KeyValuePair<string, decimal> pair in paid)
    {
        if (pair.Value < costPerHead)
        {
            part.Add(pair.Key);
        }
    }
    return part;
}

// The cost per head of a trip, looked up by its name, or -1 when it is not on offer: TryGetValue.
static decimal PriceOf(Dictionary<string, decimal> trips, string name)
{
    if (trips.TryGetValue(name, out decimal price))
    {
        return price;
    }
    return -1m;
}

// What a learner still owes, and the whole cost per head when they have paid nothing yet: TryGetValue.
static decimal Balance(Dictionary<string, decimal> paid, string reference, decimal costPerHead)
{
    if (paid.TryGetValue(reference, out decimal sofar))
    {
        return costPerHead - sofar;
    }
    return costPerHead;
}

// ================================================================ finished in lesson 05: the desk's loops
// The price list, one line per party size from 1 to the capacity, the size times the cost per head: a for loop.
static void PriceList(int capacity, decimal costPerHead)
{
    for (int size = 1; size <= capacity; size++)
    {
        Console.WriteLine($"Party of {size}: £{size * costPerHead:F2}");
    }
}

// How many digits a reference has: a foreach over its characters, char.IsDigit(c) true for 0 to 9.
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

// How many capital letters a reference has: a foreach over its characters, char.IsUpper(c) true for A to Z.
static int CountUpper(string text)
{
    int capitals = 0;
    foreach (char c in text)
    {
        if (char.IsUpper(c))
        {
            capitals = capitals + 1;
        }
    }
    return capitals;
}

// ================================================================ today: two methods may share a name
// C# builds a class called Program round the code at the top of this file, and "partial class Program" adds these
// methods to it. A method written straight in the file, as every method above is, cannot share its name with another;
// inside a class two methods can, as long as their parameters differ. Today's two methods share their names with the
// finished methods above them, moved here from lesson 07 so that they could.
// A method in the class cannot call the methods written straight in the file (PriceOf, Balance and the rest): C#
// refuses it with CS8801. Today's two need only the finished method of the same name, just above each.
partial class Program
{
    // ================================================================ Task 2a: the same name, different parameters
    // THE MODEL, finished in lesson 07 and moved here: one learner's status from what they have paid and the cost per
    // head. Task 2a, under it, is a second PaymentStatus that starts from a learner's reference instead.
    static string PaymentStatus(decimal paid, decimal costPerHead)
    {
        if (paid >= costPerHead)
        {
            return "paid in full";
        }
        else if (paid > 0)
        {
            return "part paid";
        }
        return "not paid";
    }

    // YOUR TURN, Task 2a: a second PaymentStatus, for when the desk has a learner's reference and not an amount. Look
    // up what this learner has paid (TryGetValue: a learner who has paid nothing is not in the Dictionary, and that is
    // 0), then give back what the first PaymentStatus, just above, gives for that amount. Call it: do not copy its if.
    // The desk calls this one beside every seat under option 7.
    // My prediction:
    static string PaymentStatus(Dictionary<string, decimal> paid, string reference, decimal costPerHead)
    {
        // Task 2a: two lines go here: TryGetValue for what this learner has paid, then return what the first
        // PaymentStatus gives back for that amount.
        return "";   // "" means not started yet: replace it with what the first PaymentStatus gives back
    }

    // ================================================================ Task 2b: the same name, a different type
    // THE MODEL, finished in lesson 07 and moved here: what a party pays, the number of people times the cost per head.
    // Task 2b, under it, is a second PartyCost that starts from the seats instead of a number of people.
    static decimal PartyCost(int people, decimal costPerHead)
    {
        return people * costPerHead;
    }

    // YOUR TURN, Task 2b: a second PartyCost, for what the seats booked so far pay. Count the seats that are not free (a
    // free seat is ""), then give back what the first PartyCost, just above, gives for that many people. Call it: do not
    // multiply here. The desk shows it on its top line and under its seat plan.
    // My prediction:
    static decimal PartyCost(string[] seats, decimal costPerHead)
    {
        // Task 2b: your loop goes here: count the seats that are not "", then return what the first PartyCost
        // gives back for that many people.
        return -1m;   // -1 means not started yet: replace it with what the first PartyCost gives back
    }
}

// ---------------------------------------------------------------- the check harness's typing and printing. Do not change this part.
// The checks type into your methods from a list. If a method asks for more than the list holds, or prints without
// end, the check stops it and says so, instead of waiting for ever. The debugger is told these two classes are not
// your code, so it never stops inside them.
[System.Diagnostics.DebuggerNonUserCode]
class Typing : StringReader
{
    public Typing(string typed) : base(typed) { }
    public int Reads { get; private set; }
    public override string ReadLine() { Reads++; return base.ReadLine() ?? throw new RanOutOfTyping(); }
}
[System.Diagnostics.DebuggerNonUserCode]
class Capped : StringWriter
{
    void Room(int more) { if (GetStringBuilder().Length + more > 20000) throw new TooMuchPrinted(); }
    public override void Write(char value) { Room(1); base.Write(value); }
    public override void Write(string value) { Room(value == null ? 0 : value.Length); base.Write(value); }
    public override void Write(char[] buffer, int index, int count) { Room(count); base.Write(buffer, index, count); }
}
class RanOutOfTyping : Exception { }
class TooMuchPrinted : Exception { }

// ---------------------------------------------------------------- the check harness's reading. Do not change this part.
// Before a check runs one of today's methods, it reads how the method is written in this file: its body, with the
// comments and the text in quotes taken out, and the calls it makes. A method that calls itself with the same
// arguments would never stop, and would stop the whole program when the computer ran out of room for the calls, so the
// check names it instead.
static class Reading
{
    // One method's body as it is written in this file, or "" when the file cannot be read. CallerFilePath is where
    // Program.cs was when it was built. The header is found however it is spaced: "Label( int seat,string reference )"
    // is the same header as "Label(int seat, string reference)".
    public static string BodyOf(string header, [System.Runtime.CompilerServices.CallerFilePath] string file = "")
    {
        string text;
        try { text = Tight(Squash(Plain(File.ReadAllText(file)))); } catch { return ""; }
        int at = text.IndexOf(Tight(Squash(header)));
        int open = at < 0 ? -1 : text.IndexOf('{', at);
        for (int i = open, depth = 0; open >= 0 && i < text.Length; i++)
        {
            if (text[i] == '{') depth++;
            else if (text[i] == '}' && --depth == 0) return text.Substring(open + 1, i - open - 1);
        }
        return "";
    }

    // The argument lists of every call a body makes to one name, each argument as written ("x" for text in quotes),
    // so a check can tell which version of the name a call runs: a call that fits the method it sits in is a call to
    // itself.
    public static List<string[]> CallsTo(string name, string body)
    {
        List<string[]> calls = new List<string[]>();
        for (int at = body.IndexOf(name); at >= 0; at = body.IndexOf(name, at + 1))
        {
            int from = at + name.Length;
            while (from < body.Length && body[from] == ' ') from++;
            bool whole = (at == 0 || !(char.IsLetterOrDigit(body[at - 1]) || body[at - 1] == '_'))
                && from < body.Length && body[from] == '(' && !body.Substring(0, at).TrimEnd().EndsWith("new");
            if (!whole) continue;
            List<string> args = new List<string>();
            int depth = 0, start = from + 1;
            for (int i = start; i < body.Length; i++)
            {
                char c = body[i];
                if (c == '(' || c == '[' || c == '{') depth++;
                else if ((c == ')' || c == ']' || c == '}') && depth-- == 0) { args.Add(body.Substring(start, i - start).Trim()); break; }
                else if (c == ',' && depth == 0) { args.Add(body.Substring(start, i - start).Trim()); start = i + 1; }
            }
            calls.Add(args.Count == 1 && args[0] == "" ? new string[0] : args.ToArray());
        }
        return calls;
    }

    // The names a body declares as an array of strings ("string[] booked = seats;", or "var booked = ..." made from
    // seats or ToArray()), so a check can tell that passing one of them is passing the seats again.
    public static List<string> ArraysIn(string body)
    {
        List<string> names = new List<string>();
        foreach (System.Text.RegularExpressions.Match m in System.Text.RegularExpressions.Regex.Matches(body, @"string\s*\[\s*\]\s*([A-Za-z_]\w*)"))
        {
            names.Add(m.Groups[1].Value);
        }
        foreach (System.Text.RegularExpressions.Match m in System.Text.RegularExpressions.Regex.Matches(body, @"\bvar\s+([A-Za-z_]\w*)\s*=\s*([^;]*)"))
        {
            string made = m.Groups[2].Value.Replace(" ", "");
            if (made == "seats" || made.EndsWith("ToArray()")) names.Add(m.Groups[1].Value);
        }
        return names;
    }

    static string Squash(string s) => string.Join(" ", s.Split((char[])null, StringSplitOptions.RemoveEmptyEntries));

    // No space beside a bracket, a comma or a semicolon, so two ways of spacing the same code read the same.
    static string Tight(string s) => System.Text.RegularExpressions.Regex.Replace(s, @"\s*([(),\[\]{};])\s*", "$1");

    // The text with comments taken out and every quoted string or character left as x, read in one pass the way C#
    // reads it; the code inside an interpolated string's { } is kept, since a call can sit there.
    static string Plain(string s)
    {
        System.Text.StringBuilder sb = new System.Text.StringBuilder();
        int i = 0;
        while (i < s.Length)
        {
            char c = s[i], n = i + 1 < s.Length ? s[i + 1] : ' ';
            if (c == '/' && n == '/') { while (i < s.Length && s[i] != '\n') i++; }
            else if (c == '/' && n == '*') { int e = s.IndexOf("*/", i + 2); i = e < 0 ? s.Length : e + 2; sb.Append(' '); }
            else if (c == '\'') { i++; while (i < s.Length && s[i] != '\'') i += s[i] == '\\' ? 2 : 1; i++; sb.Append(" x "); }
            else if (c == '"' || ((c == '@' || c == '$') && (n == '"' || ((n == '@' || n == '$') && i + 2 < s.Length && s[i + 2] == '"'))))
            {
                bool verbatim = false, holes = false;
                while (s[i] != '"') { verbatim |= s[i] == '@'; holes |= s[i] == '$'; i++; }
                i++;
                sb.Append(" x ");
                while (i < s.Length)
                {
                    if (verbatim && s[i] == '"' && i + 1 < s.Length && s[i + 1] == '"') { i += 2; continue; }
                    if (!verbatim && s[i] == '\\') { i += 2; continue; }
                    if (s[i] == '"') { i++; break; }
                    if (holes && s[i] == '{' && i + 1 < s.Length && s[i + 1] == '{') { i += 2; continue; }
                    if (holes && s[i] == '{')
                    {
                        int depth = 0, start = i + 1, colon = -1;
                        for (; i < s.Length; i++)
                        {
                            if (s[i] == '(' || s[i] == '[' || s[i] == '{') depth++;
                            else if (s[i] == ')' || s[i] == ']' || (s[i] == '}' && depth > 1)) depth--;
                            else if (s[i] == '}') break;
                            else if (s[i] == ':' && depth == 1 && colon < 0) colon = i;
                        }
                        sb.Append(' ').Append(Plain(s.Substring(start, (colon < 0 ? i : colon) - start))).Append(' ');
                        i++;
                        continue;
                    }
                    i++;
                }
            }
            else { sb.Append(c); i++; }
        }
        return sb.ToString();
    }
}
