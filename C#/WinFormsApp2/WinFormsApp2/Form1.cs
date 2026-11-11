namespace WinFormsApp2
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Debug.WriteLine("test");
            Pokemans pikachu = new Pokemans("Pikachu", "Electric", 5, 35, 100, "Thunder Shock");
            pikachu.attack();

        }
    }
}
