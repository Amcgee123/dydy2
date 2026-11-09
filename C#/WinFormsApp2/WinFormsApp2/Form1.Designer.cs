namespace WinFormsApp2
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            button1 = new Button();
            button2 = new Button();
            button3 = new Button();
            button4 = new Button();
            button5 = new Button();
            button6 = new Button();
            button7 = new Button();
            button8 = new Button();
            pictureBox1 = new PictureBox();
            pictureBox2 = new PictureBox();
            player_two_select_bnt = new Button();
            player_one_select_txt = new TextBox();
            label1 = new Label();
            player_two_select_txt = new TextBox();
            player_two_select_btn = new Button();
            ((System.ComponentModel.ISupportInitialize)pictureBox1).BeginInit();
            ((System.ComponentModel.ISupportInitialize)pictureBox2).BeginInit();
            SuspendLayout();
            // 
            // button1
            // 
            button1.Location = new Point(713, 12);
            button1.Name = "button1";
            button1.Size = new Size(75, 23);
            button1.TabIndex = 0;
            button1.Text = "button1";
            button1.UseVisualStyleBackColor = true;
            button1.Click += button1_Click;
            // 
            // button2
            // 
            button2.Location = new Point(713, 41);
            button2.Name = "button2";
            button2.Size = new Size(75, 23);
            button2.TabIndex = 1;
            button2.Text = "button2";
            button2.UseVisualStyleBackColor = true;
            // 
            // button3
            // 
            button3.Location = new Point(713, 70);
            button3.Name = "button3";
            button3.Size = new Size(75, 23);
            button3.TabIndex = 2;
            button3.Text = "button3";
            button3.UseVisualStyleBackColor = true;
            // 
            // button4
            // 
            button4.Location = new Point(713, 99);
            button4.Name = "button4";
            button4.Size = new Size(75, 23);
            button4.TabIndex = 3;
            button4.Text = "button4";
            button4.UseVisualStyleBackColor = true;
            // 
            // button5
            // 
            button5.Location = new Point(12, 415);
            button5.Name = "button5";
            button5.Size = new Size(75, 23);
            button5.TabIndex = 7;
            button5.Text = "button5";
            button5.UseVisualStyleBackColor = true;
            // 
            // button6
            // 
            button6.Location = new Point(12, 386);
            button6.Name = "button6";
            button6.Size = new Size(75, 23);
            button6.TabIndex = 6;
            button6.Text = "button6";
            button6.UseVisualStyleBackColor = true;
            // 
            // button7
            // 
            button7.Location = new Point(12, 357);
            button7.Name = "button7";
            button7.Size = new Size(75, 23);
            button7.TabIndex = 5;
            button7.Text = "button7";
            button7.UseVisualStyleBackColor = true;
            // 
            // button8
            // 
            button8.Location = new Point(12, 328);
            button8.Name = "button8";
            button8.Size = new Size(75, 23);
            button8.TabIndex = 4;
            button8.Text = "button8";
            button8.UseVisualStyleBackColor = true;
            // 
            // pictureBox1
            // 
            pictureBox1.Location = new Point(102, 265);
            pictureBox1.Name = "pictureBox1";
            pictureBox1.Size = new Size(100, 144);
            pictureBox1.TabIndex = 8;
            pictureBox1.TabStop = false;
            // 
            // pictureBox2
            // 
            pictureBox2.Location = new Point(597, 41);
            pictureBox2.Name = "pictureBox2";
            pictureBox2.Size = new Size(100, 144);
            pictureBox2.TabIndex = 9;
            pictureBox2.TabStop = false;
            // 
            // player_two_select_bnt
            // 
            player_two_select_bnt.Location = new Point(63, 299);
            player_two_select_bnt.Name = "player_two_select_bnt";
            player_two_select_bnt.Size = new Size(24, 23);
            player_two_select_bnt.TabIndex = 10;
            player_two_select_bnt.Text = "button9";
            player_two_select_bnt.UseVisualStyleBackColor = true;
            player_two_select_bnt.Click += player_two_select_bnt_Click;
            // 
            // player_one_select_txt
            // 
            player_one_select_txt.Location = new Point(12, 300);
            player_one_select_txt.Name = "player_one_select_txt";
            player_one_select_txt.Size = new Size(45, 23);
            player_one_select_txt.TabIndex = 11;
            player_one_select_txt.TextChanged += player_one_select_txt_TextChanged;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Location = new Point(12, 16);
            label1.Name = "label1";
            label1.Size = new Size(101, 15);
            label1.TabIndex = 12;
            label1.Text = "enter pokemon id";
            // 
            // player_two_select_txt
            // 
            player_two_select_txt.Location = new Point(611, 13);
            player_two_select_txt.Name = "player_two_select_txt";
            player_two_select_txt.Size = new Size(45, 23);
            player_two_select_txt.TabIndex = 14;
            player_two_select_txt.TextChanged += player_two_select_txt_TextChanged;
            // 
            // player_two_select_btn
            // 
            player_two_select_btn.Location = new Point(662, 12);
            player_two_select_btn.Name = "player_two_select_btn";
            player_two_select_btn.Size = new Size(24, 23);
            player_two_select_btn.TabIndex = 13;
            player_two_select_btn.Text = "button10";
            player_two_select_btn.UseVisualStyleBackColor = true;
            player_two_select_btn.Click += player_two_select_btn_Click;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 450);
            Controls.Add(player_two_select_txt);
            Controls.Add(player_two_select_btn);
            Controls.Add(label1);
            Controls.Add(player_one_select_txt);
            Controls.Add(player_two_select_bnt);
            Controls.Add(pictureBox2);
            Controls.Add(pictureBox1);
            Controls.Add(button5);
            Controls.Add(button6);
            Controls.Add(button7);
            Controls.Add(button8);
            Controls.Add(button4);
            Controls.Add(button3);
            Controls.Add(button2);
            Controls.Add(button1);
            Name = "Form1";
            Text = "Form1";
            Load += Form1_Load;
            ((System.ComponentModel.ISupportInitialize)pictureBox1).EndInit();
            ((System.ComponentModel.ISupportInitialize)pictureBox2).EndInit();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Button button1;
        private Button button2;
        private Button button3;
        private Button button4;
        private Button button5;
        private Button button6;
        private Button button7;
        private Button button8;
        private PictureBox pictureBox1;
        private PictureBox pictureBox2;
        private Button player_two_select_bnt;
        private TextBox player_one_select_txt;
        private Label label1;
        private TextBox player_two_select_txt;
        private Button player_two_select_btn;
    }
}
