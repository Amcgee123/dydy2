using System;
using System.Collections.Generic;
using System.text;

namespace onlinebanking 
{
	public Class1 bankaccount()
	{
		// atributes
		private string customerName;
		private decimal balance;

        //constructor - used to initialize the atributes
		bankacount()
		{
			customerName = " ";
			balance = 0;
        }

        //methods
        public void makeDeposit(decimal amount)
		{
			balance+= amount;
        }

		public void makeWithdrawal(decimal amount)
		{
			balance-= amount;
		}

		public decimal getbalance()
		{
			return balance;
        }
    }
}
