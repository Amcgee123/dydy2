namespace money_devider
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            //takes input
            int ammount_of_people = int.Parse(textBox2.Text);
            decimal ammount_of_money = decimal.Parse(textBox1.Text);
            //calculates money per person
            decimal money_per_person = ammount_of_money / ammount_of_people;

            textBox3.Text  = $"{money_per_person:c} per person";
            //outputs result
        }

        private void textBox3_TextChanged(object sender, EventArgs e)
        {
            
        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }
    }
}
