namespace AreaCalculator;

static class Program
{
    // The program starts here and opens the form. You do not need to change this file.
    [STAThread]
    static void Main()
    {
        ApplicationConfiguration.Initialize();
        Application.Run(new Form1());
    }
}
