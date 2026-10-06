// LoopLab: 05 - Iteration, part 1. Rung: 1 · Copy the model.
// Four small programs, one loop each: two for loops, then two while loops. This project is for this lesson only;
// next lesson opens the trips desk, the project you keep all term.
//
// HOW TO WORK. Run it first. Every run prints what the four finished models do, then the CHECKS: each part of today's
// task prints PASS, FIX or a dash (not started yet), and the last line is your RESULTS LINE, which the exit ticket asks
// you to paste. Today's parts are the methods marked YOUR TURN; each sits under a finished method with the same shape.
// Under each YOUR TURN heading is a "My prediction:" line: before you write the method, type what its check will want
// from it, then write, run and compare. Nothing else in the file is yours to change today.

// ---------------------------------------------------------------- the check harness. Do not change this part.
// It runs each of today's methods with fixed typing, catches what they print or give back, and compares.
// If a method stops early, what it printed is replaced by one line saying why.
string Capture(Action run, string typed)
{
    TextReader oldIn = Console.In; TextWriter oldOut = Console.Out;
    Capped caught = new Capped();
    Console.SetIn(new Typing(typed));
    Console.SetOut(caught);
    string stopped = "";
    try { run(); }
    catch (RanOutOfTyping) { stopped = "[stopped: it asked again after the last typed line. Does the loop ever stop?]"; }
    catch (TooMuchPrinted) { stopped = "[stopped: it printed far too much. Does the loop ever stop?]"; }
    catch (Exception e) { stopped = $"[stopped with {e.GetType().Name}]"; }
    finally { Console.SetIn(oldIn); Console.SetOut(oldOut); }
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
string Show(string s) => s.Replace("\n", " / ").TrimEnd(' ', '/');
string Overall(params string[] verdicts) => verdicts.All(v => v == "-") ? "-" : (verdicts.All(v => v == "PASS") ? "PASS" : "FIX");
string LastLine(string s) => s.TrimEnd('\n').Split('\n').Last();
string Stopped(string printed) => printed.Contains("[stopped") ? printed.Substring(printed.IndexOf("[stopped")) : "";
string More(string line, int times) => string.Concat(Enumerable.Repeat(line + "\n", times));
int Times(string s, string part) => (s.Length - s.Replace(part, "").Length) / part.Length;

// ---------------------------------------------------------------- the four finished models, run once each
Console.WriteLine("THE MODELS: what each finished method does");
Console.WriteLine($"Repeat(\"Boro\", 2) prints: {Show(Capture(() => Repeat("Boro", 2), ""))}");
Console.WriteLine($"TimesTwo() ends: {LastLine(Capture(() => TimesTwo(), ""))}");
Console.WriteLine($"WeeksToPass(90, 30) gives {WeeksToPass(90m, 30m)}: exactly 90 has not passed 90, so it saves once more");
int seatsTyped = 0;
Capture(() => { seatsTyped = AskForSeats(); }, "nine\n9\n4\n");
Console.WriteLine($"AskForSeats(), typed nine, then 9, then 4, gives {seatsTyped}");
Console.WriteLine();

Console.WriteLine("CHECKS");
// Task 2a: numbered lines
string a1 = Capture(() => NumberedLines("Boro", 3), "");
string a2 = Capture(() => NumberedLines("Boro", 1), "");
bool startedA = a1.Length > 0 || a2.Length > 0;
string v2a = Overall(
    Check("2a", "Boro, 3 times", a1, "1 Boro\n2 Boro\n3 Boro\n", startedA),
    Check("2a", "Boro, once", a2, "1 Boro\n", startedA));
// Task 2b: any times table, 1 to 12
string b1 = Capture(() => TimesTable(4), "");
string b2 = Capture(() => TimesTable(9), "");
bool startedB = b1.Length > 0 || b2.Length > 0;
string v2b = Overall(
    Check("2b", "the 4 times table", b1,
        "1 x 4 = 4\n2 x 4 = 8\n3 x 4 = 12\n4 x 4 = 16\n5 x 4 = 20\n6 x 4 = 24\n7 x 4 = 28\n8 x 4 = 32\n9 x 4 = 36\n10 x 4 = 40\n11 x 4 = 44\n12 x 4 = 48\n",
        startedB),
    Check("2b", "the 9 times table, last line", LastLine(b2), "12 x 9 = 108", startedB));
// Task 2c: donations until the total passes the limit
int c1 = -1, c2 = -1, c3 = -1;
string cp1 = Capture(() => { c1 = Donations(1000m); }, "400\n400\n300\n" + More("5000", 10));
string cp2 = Capture(() => { c2 = Donations(1000m); }, "500\n500\n100\n" + More("5000", 10));
string cp3 = Capture(() => { c3 = Donations(500m); }, "600\n" + More("5000", 10));
bool startedC = c1 != -1 || c2 != -1 || c3 != -1 || cp1.Length > 0 || cp2.Length > 0 || cp3.Length > 0;
string done = "All money allocated";
string words = Stopped(cp1) != "" ? Stopped(cp1)
    : Times(cp1, done) == 0 ? "no All money allocated"
    : Times(cp1, done) > 1 ? $"All money allocated {Times(cp1, done)} times"
    : cp1.TrimEnd().EndsWith(done) ? "All money allocated, once, at the end" : "something printed after All money allocated";
string v2c = Overall(
    Check("2c", "400, 400, 300 against 1000", Stopped(cp1) != "" ? Stopped(cp1) : c1.ToString(), "3", startedC),
    Check("2c", "500, 500, 100 against 1000", Stopped(cp2) != "" ? Stopped(cp2) : c2.ToString(), "3", startedC),
    Check("2c", "600 against 500", Stopped(cp3) != "" ? Stopped(cp3) : c3.ToString(), "1", startedC),
    Check("2c", "the last words", words, "All money allocated, once, at the end", startedC));
// Task 2d: the quiz that asks again
int d1 = -1, d2 = -1;
string dp1 = Capture(() => { d1 = SumQuiz(); }, "14\nfifteen\n15\n" + More("15", 20));
string dp2 = Capture(() => { d2 = SumQuiz(); }, "15\n" + More("15", 20));
bool startedD = d1 != -1 || d2 != -1 || dp1.Length > 0 || dp2.Length > 0;
string v2d = Overall(
    Check("2d", "14, then fifteen, then 15", Stopped(dp1) != "" ? Stopped(dp1) : d1.ToString(), "3", startedD),
    Check("2d", "15 first time", Stopped(dp2) != "" ? Stopped(dp2) : d2.ToString(), "1", startedD));
Console.WriteLine($"{pass} of {pass + fail} checks PASS");
Console.WriteLine();
Console.WriteLine("Your results line (copy it into the exit ticket, question two):");
Console.WriteLine($"2a {v2a}  2b {v2b}  2c {v2c}  2d {v2d}");

// ================================================================ Task 2a: a for loop that counts
// THE MODEL, finished: a word printed a number of times, one per line.
// A for loop has three parts in its header: start (int i = 1); keep going while (i <= times); step (i++).
// i <= times is inclusive: the last go is when i equals times. In Python this was range(1, times + 1).
static void Repeat(string word, int times)
{
    for (int i = 1; i <= times; i++)
    {
        Console.WriteLine(word);
    }
}

// YOUR TURN, Task 2a: the same, with each line numbered from 1. NumberedLines("Boro", 3) prints "1 Boro",
// then "2 Boro", then "3 Boro".
// The same shape as Repeat, one thing changed: what each line prints.
// My prediction:
static void NumberedLines(string word, int times)
{
    // Task 2a: your for loop goes here. Look up at Repeat: same start, same test, same step.
    // Until you write it, this method prints nothing, and the check shows a dash.
}

// ================================================================ Task 2b: a for loop whose counter does the maths
// THE MODEL, finished: the 2 times table, from 1 x 2 = 2 up to 12 x 2 = 24. The counter i is used twice on each line.
static void TimesTwo()
{
    for (int i = 1; i <= 12; i++)
    {
        Console.WriteLine($"{i} x 2 = {i * 2}");
    }
}

// YOUR TURN, Task 2b: any times table, 1 to 12. TimesTable(4) prints "1 x 4 = 4" up to "12 x 4 = 48".
// The same shape as TimesTwo, one thing changed: the table comes in as a parameter instead of always being 2.
// My prediction:
static void TimesTable(int table)
{
    // Task 2b: your for loop goes here. Look up at TimesTwo, and change the one thing.
    // Until you write it, this method prints nothing, and the check shows a dash.
}

// ================================================================ Task 2c: a while loop that stops when a total passes a limit
// THE MODEL, finished: how many weeks of saving it takes until the savings are MORE than the target.
// A while loop tests its condition BEFORE each go, and the body must change what the condition tests (saved grows),
// or the loop never ends. saved <= target means "not past the target yet", so exactly the target goes round again.
static int WeeksToPass(decimal target, decimal perWeek)
{
    decimal saved = 0m;
    int weeks = 0;
    while (saved <= target)
    {
        saved = saved + perWeek;
        weeks = weeks + 1;
    }
    return weeks;
}

// YOUR TURN, Task 2c: a charity gives away money in small donations. Keep asking "Donation: " and adding each amount
// typed, as long as the total has NOT passed the limit. When it has, print "All money allocated" once, after the loop,
// and give back how many donations were taken. 400, 400 and 300 against a limit of 1000 gives 3.
// The same shape as WeeksToPass, one thing changed: each amount is typed in, decimal.Parse(Console.ReadLine()).
// My prediction:
static int Donations(decimal limit)
{
    // Task 2c: your while loop goes here. Look up at WeeksToPass: the condition is tested before each go,
    // and the body must change what the condition tests. Count the donations; print the message after the loop.
    return -1;   // -1 means not started yet: replace it with the count you built
}

// ================================================================ Task 2d: a while loop that asks until the answer is right
// THE MODEL, finished: keeps asking for a number of seats until a whole number from 1 to 8 is typed, then gives it
// back. int.TryParse never crashes on a word, as in lesson 04: it leaves seats at 0, which is not 1 to 8, so the
// loop asks again.
static int AskForSeats()
{
    int seats = 0;
    while (seats < 1 || seats > 8)
    {
        Console.Write("How many seats (1 to 8)? ");
        int.TryParse(Console.ReadLine(), out seats);
    }
    return seats;
}

// YOUR TURN, Task 2d: a quiz question. Keep asking "What is 7 + 8? " until 15 is typed, and give back how many tries
// it took. Typing 14, then fifteen, then 15 gives 3, and the word must never crash the program.
// The same shape as AskForSeats, two things changed: the test is whether the answer is 15, and a count goes up on
// every go.
// My prediction:
static int SumQuiz()
{
    // Task 2d: your while loop goes here. Look up at AskForSeats: TryParse inside the loop, and the loop
    // runs while the answer is not right yet. Add a count that goes up by one on every go.
    return -1;   // -1 means not started yet: replace it with the count you built
}

// ---------------------------------------------------------------- the check harness's typing and printing. Do not change this part.
// The checks type into your methods from a list. If a method asks for more than the list holds, or prints without
// end, the check stops it and says so, instead of waiting for ever.
class Typing : StringReader
{
    public Typing(string typed) : base(typed) { }
    public override string ReadLine() => base.ReadLine() ?? throw new RanOutOfTyping();
}
class Capped : StringWriter
{
    void Room(int more) { if (GetStringBuilder().Length + more > 20000) throw new TooMuchPrinted(); }
    public override void Write(char value) { Room(1); base.Write(value); }
    public override void Write(string value) { Room(value == null ? 0 : value.Length); base.Write(value); }
    public override void Write(char[] buffer, int index, int count) { Room(count); base.Write(buffer, index, count); }
}
class RanOutOfTyping : Exception { }
class TooMuchPrinted : Exception { }
