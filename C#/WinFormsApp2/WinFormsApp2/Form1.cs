using static System.Windows.Forms.LinkLabel;
using Microsoft.Data.Sqlite;

namespace WinFormsApp2
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();

        }

        public void player_two_select_btn_Click(object sender, EventArgs e)
        {
            int player_one_selected = int.Parse(player_one_select_txt.Text);
            player_one_selected = player_one_selected + 1; 
        }

        public void player_two_select_bnt_Click(object sender, EventArgs e,)
        {
            int player_two_selected = int.Parse(player_two_select_txt.Text);
            player_two_selected = player_two_selected + 1;
            
            return player_two_selected;
        }

        
        
        string[] pokemondata = File.ReadAllLines("pokemon_with_base_hp.csv");
        

        public void give_data_p1()
        {
            string name_p1 = "ahhh";
            string type_p1 = "ahhhh";
            string attack_p1 = "ahhh";
        }

        public (int, string, int) readFromCSV() 
        {
            string s = pokemondata[0];

            string[] poke_values = s.Split(',').Select(sValue => sValue.Trim()).ToArray();

            int pokemon_id = int.Parse(poke_values[0]);
            string pokemon_name = poke_values[1];
            int pokemon_base_hp = int.Parse(poke_values[2]);

            return (pokemon_id, pokemon_name, pokemon_base_hp);
        }

        public (int, string, int) readFromCSV_p2()
        {
            string s = pokemondata[0];

            string[] poke_values = s.Split(',').Select(sValue => sValue.Trim()).ToArray();

            int pokemon_id_p2 = int.Parse(poke_values[0]);
            string pokemon_name_p2 = poke_values[1];
            int pokemon_base_hp_p2 = int.Parse(poke_values[2]);

            return (pokemon_id_p2, pokemon_name_p2, pokemon_base_hp_p2);
        }


        public void button1_Click(object sender, EventArgs e)
        {
         var (pokemon_id, pokemon_name, pokemon_base_hp) = readFromCSV();
         var (pokemon_id_p2, pokemon_name_p2, pokemon_base_hp_p2) = readFromCSV();

            string name_p1 = pokemon_name;
            string name_p2 = pokemon_name_p2;



            Pokemans player_one = new Pokemans(name_p1, type_p1, 5, 35, 100, attack_p1);
            Pokemans player_two = new Pokemans(name_p2, type_p2, 5, 35, 100, attack_p2);
            player_one.attack();

        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void player_one_select_txt_TextChanged(object sender, EventArgs e)
        {
            // collect id here (pokemon1)
        }

        private void player_two_select_txt_TextChanged(object sender, EventArgs e)
        {
            // collect id here (pokemon2)

        }
    }
}
