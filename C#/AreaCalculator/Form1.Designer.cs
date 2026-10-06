namespace AreaCalculator;

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

    // Visual Studio writes this file when you drag controls onto the form and change their properties.
    // Do not type your own code in here: it is rewritten every time the form changes.
    private void InitializeComponent()
    {
        lblLength = new Label();
        txtLength = new TextBox();
        lblWidth = new Label();
        txtWidth = new TextBox();
        btnCalculate = new Button();
        lblArea = new Label();
        txtArea = new TextBox();
        SuspendLayout();
        // 
        // lblLength
        // 
        lblLength.AutoSize = true;
        lblLength.Location = new Point(26, 26);
        lblLength.Name = "lblLength";
        lblLength.Size = new Size(66, 15);
        lblLength.TabIndex = 0;
        lblLength.Text = "Length (m)";
        // 
        // txtLength
        // 
        txtLength.Location = new Point(140, 22);
        txtLength.Margin = new Padding(3, 2, 3, 2);
        txtLength.Name = "txtLength";
        txtLength.Size = new Size(123, 23);
        txtLength.TabIndex = 1;
        txtLength.TextChanged += txtLength_TextChanged;
        // 
        // lblWidth
        // 
        lblWidth.AutoSize = true;
        lblWidth.Location = new Point(26, 63);
        lblWidth.Name = "lblWidth";
        lblWidth.Size = new Size(61, 15);
        lblWidth.TabIndex = 2;
        lblWidth.Text = "Width (m)";
        // 
        // txtWidth
        // 
        txtWidth.Location = new Point(140, 60);
        txtWidth.Margin = new Padding(3, 2, 3, 2);
        txtWidth.Name = "txtWidth";
        txtWidth.Size = new Size(123, 23);
        txtWidth.TabIndex = 3;
        txtWidth.TextChanged += this.txtWidth_TextChanged;
        // 
        // btnCalculate
        // 
        btnCalculate.Location = new Point(140, 98);
        btnCalculate.Margin = new Padding(3, 2, 3, 2);
        btnCalculate.Name = "btnCalculate";
        btnCalculate.Size = new Size(122, 28);
        btnCalculate.TabIndex = 4;
        btnCalculate.Text = "Calculate";
        btnCalculate.UseVisualStyleBackColor = true;
        btnCalculate.Click += btnCalculate_Click;
        // 
        // lblArea
        // 
        lblArea.AutoSize = true;
        lblArea.Location = new Point(26, 146);
        lblArea.Name = "lblArea";
        lblArea.Size = new Size(57, 15);
        lblArea.TabIndex = 5;
        lblArea.Text = "Area (m²)";
        // 
        // txtArea
        // 
        txtArea.Location = new Point(140, 142);
        txtArea.Margin = new Padding(3, 2, 3, 2);
        txtArea.Name = "txtArea";
        txtArea.ReadOnly = true;
        txtArea.Size = new Size(123, 23);
        txtArea.TabIndex = 6;
        txtArea.TabStop = false;
        txtArea.TextChanged += this.txtArea_TextChanged;
        // 
        // Form1
        // 
        AcceptButton = btnCalculate;
        AutoScaleDimensions = new SizeF(7F, 15F);
        AutoScaleMode = AutoScaleMode.Font;
        ClientSize = new Size(298, 188);
        Controls.Add(txtArea);
        Controls.Add(lblArea);
        Controls.Add(btnCalculate);
        Controls.Add(txtWidth);
        Controls.Add(lblWidth);
        Controls.Add(txtLength);
        Controls.Add(lblLength);
        FormBorderStyle = FormBorderStyle.FixedSingle;
        Margin = new Padding(3, 2, 3, 2);
        MaximizeBox = false;
        Name = "Form1";
        Text = "Area calculator";
        ResumeLayout(false);
        PerformLayout();
    }

    #endregion

    private Label lblLength;
    private TextBox txtLength;
    private Label lblWidth;
    private TextBox txtWidth;
    private Button btnCalculate;
    private Label lblArea;
    private TextBox txtArea;
}
