// Riverside Cinema: the program you read in the starting point check.
// Build it (Ctrl+Shift+B), run it (F5) and compare the last line with your prediction.

Console.WriteLine("Riverside Cinema: ticket calculator");

Console.Write("Your name: ");
string name = Console.ReadLine();

Console.Write("How many tickets? ");
int tickets = int.Parse(Console.ReadLine());

decimal total = 0;

for (int i = 1; i <= tickets; i++)
{
    Console.Write($"Age of person {i}: ");
    int age = int.Parse(Console.ReadLine());

    if (age < 16)
    {
        total += 5.50m;
    }
    else if (age >= 65)
    {
        total += 6.00m;
    }
    else
    {
        total += 9.25m;
    }
}

bool bigGroup = tickets >= 4;

if (bigGroup)
{
    total = total * 0.9m;
    Console.WriteLine("Group discount applied (10% off).");
}

Console.WriteLine($"{name}, your {tickets} ticket(s) come to {total:C}");
