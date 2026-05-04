import tkinter as tk
import numpy as np
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Calculator")
        self.root.geometry("350x500")
        self.root.resizable(False, False)

        # Color Palette
        self.bg_color = "#1e1e1e"
        self.btn_color = "#333333"
        self.text_color = "#ffffff"
        self.accent_color = "#ff9500" # Orange for operators

        self.root.configure(bg=self.bg_color)

        self.expression = ""

        # Display Screen
        self.screen_var = tk.StringVar()
        self.screen = tk.Entry(
            root, textvariable=self.screen_var, font=("Arial", 30),
            bg=self.bg_color, fg=self.text_color, borderwidth=0,
            justify='right', insertbackground=self.text_color
        )
        self.screen.pack(fill="both", ipadx=8, ipady=30, padx=10, pady=20)

        # Button Layout
        self.create_buttons()

        # Keyboard Bindings
        self.bind_keys()

    def create_buttons(self):
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack()

        buttons = [
            'C', '/', '*', '-',
            '7', '8', '9', '+',
            '4', '5', '6', '=',
            '1', '2', '3', '0',
            '.', 'Delete'
        ]

        row, col = 0, 0
        for btn_text in buttons:
            # Color logic
            color = self.accent_color if btn_text in ['/', '*', '-', '+', '=', 'C'] else self.btn_color

            # Create button
            btn = tk.Button(
                button_frame, text=btn_text, width=5, height=2,
                font=("Arial", 14, "bold"), bg=color, fg=self.text_color,
                activebackground="#555555", relief="flat",
                command=lambda b=btn_text: self.on_click(b)
            )

            # Special layout for "=" and "0" or "Delete"
            if btn_text == "=":
                btn.grid(row=row, column=col, rowspan=2, sticky="nsew", padx=2, pady=2)
            else:
                btn.grid(row=row, column=col, padx=2, pady=2)

            col += 1
            if col > 3:
                col = 0
                row += 1

    def on_click(self, char):
        if char == "C":
            self.expression = ""
        elif char == "Delete":
            self.expression = self.expression[:-1]
        elif char == "=":
            try:
                # Basic math evaluation
                self.expression = str(eval(self.expression))
            except Exception:
                messagebox.showerror("Error", "Invalid Input")
                self.expression = ""
        else:
            self.expression += str(char)

        self.screen_var.set(self.expression)

    def bind_keys(self):
        # Bind numbers and operators
        for i in range(10):
            self.root.bind(str(i), lambda e, i=i: self.on_click(i))

        self.root.bind('+', lambda e: self.on_click('+'))
        self.root.bind('-', lambda e: self.on_click('-'))
        self.root.bind('*', lambda e: self.on_click('*'))
        self.root.bind('/', lambda e: self.on_click('/'))
        self.root.bind('.', lambda e: self.on_click('.'))

        # Action keys
        self.root.bind('<Return>', lambda e: self.on_click('='))
        self.root.bind('<BackSpace>', lambda e: self.on_click('Delete'))
        self.root.bind('<Escape>', lambda e: self.on_click('C'))

if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()


# simple calculator 
