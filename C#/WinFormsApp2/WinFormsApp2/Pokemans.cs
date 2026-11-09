using System;
using System.Collections.Generic;
using System.Text;
using System.Diagnostics;

namespace WinFormsApp2
{
    internal class Pokemans
    {
        // Fields that EVERY pokemon must have
        public string name;
        public string type;
        public int level;
        public int hp;
        public string attacks;

        // Constructor
        public Pokemans(string name, string type, int level, int hp, int energy, string attacks)
        {
            this.name = name;
            this.type = type;
            this.level = level;
            this.hp = hp;
            this.attacks =attacks;

            Debug.WriteLine($"Pokemon {this.name} created with {this.type}");

        }

        // Methods
        // Attack
        public void attack() 
        {
            Debug.WriteLine($"Pokemon {this.name} with {this.attacks}, attack number, attack damage");            
        }
        // Dodge
        public void dodge()
        {
            Debug.WriteLine("dodge");
        }
        // Heal
        public void heal()
        {
            Debug.WriteLine("heal");
        }
        // Level up
        public void levelUp()
        {
            Debug.WriteLine("level up");
        }

    }
}
