namespace WinFormsApp1
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
            textBox1 = new TextBox();
            textBox2 = new TextBox();
            textBox3 = new TextBox();
            y = new Label();
            label2 = new Label();
            label3 = new Label();
            SuspendLayout();
            // 
            // button1
            // 
            button1.Location = new Point(182, 99);
            button1.Name = "button1";
            button1.Size = new Size(75, 23);
            button1.TabIndex = 0;
            button1.Text = "calculate";
            button1.UseVisualStyleBackColor = true;
            button1.Click += button1_Click;
            // 
            // textBox1
            // 
            textBox1.AccessibleName = "lengh_textbox";
            textBox1.Location = new Point(69, 74);
            textBox1.Name = "textBox1";
            textBox1.Size = new Size(100, 23);
            textBox1.TabIndex = 1;
            // 
            // textBox2
            // 
            textBox2.AccessibleName = "with_textbox";
            textBox2.Location = new Point(69, 124);
            textBox2.Name = "textBox2";
            textBox2.Size = new Size(100, 23);
            textBox2.TabIndex = 2;
            // 
            // textBox3
            // 
            textBox3.BackColor = SystemColors.ButtonHighlight;
            textBox3.Location = new Point(276, 100);
            textBox3.Name = "textBox3";
            textBox3.ReadOnly = true;
            textBox3.ShortcutsEnabled = false;
            textBox3.Size = new Size(100, 23);
            textBox3.TabIndex = 3;
            textBox3.TextChanged += textBox3_TextChanged;
            // 
            // y
            // 
            y.AutoSize = true;
            y.Location = new Point(67, 58);
            y.Name = "y";
            y.Size = new Size(37, 15);
            y.TabIndex = 4;
            y.Text = "lengh";
            y.Click += label1_Click;
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Location = new Point(71, 111);
            label2.Name = "label2";
            label2.Size = new Size(30, 15);
            label2.TabIndex = 5;
            label2.Text = "with";
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Location = new Point(277, 87);
            label3.Name = "label3";
            label3.Size = new Size(29, 15);
            label3.TabIndex = 6;
            label3.Text = "area";
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 450);
            Controls.Add(label3);
            Controls.Add(label2);
            Controls.Add(y);
            Controls.Add(textBox3);
            Controls.Add(textBox2);
            Controls.Add(textBox1);
            Controls.Add(button1);
            Name = "Form1";
            Text = "Form1";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Button button1;
        private TextBox textBox1;
        private TextBox textBox2;
        private TextBox textBox3;
        private Label y;
        private Label label2;
        private Label label3;
        private Button button2;
        private TextBox textBox4;
        private TextBox textBox5;
        private TextBox textBox6;
        private Label label4;
        private Label label5;
        private Label label6;
    }
}
