namespace AreaCalculator;

// The area calculator. The form is already built: open Form1.cs [Design] to see it.
//   txtLength      the length, typed by the user
//   txtWidth       the width, typed by the user
//   btnCalculate   the button
//   txtArea        the answer (ReadOnly, so nobody can type in it)
public partial class Form1 : Form
{
    public Form1()
    {
        InitializeComponent();
    }

    // Visual Studio wrote this method, and it runs every time Calculate is clicked.
    // Task 2: write your lines between the two braces.
    //   1. read the length from txtLength and convert it to a double
    //   2. read the width from txtWidth and convert it to a double
    //   3. multiply them
    //   4. show the answer in txtArea
    private void btnCalculate_Click(object sender, EventArgs e)
    {
         
    }

    private void txtLength_TextChanged(object sender, EventArgs e)
    {

    }
}
