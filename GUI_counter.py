import tkinter as tk

def increment():
    current = int(label_value["text"])
    label_value.config(text=str(current + 1))

def decrement():
    current = int(label_value["text"])
    label_value.config(text=str(current - 1))

def reset():
    label_value.config(text="0")

# Create main window
root = tk.Tk()
root.title("Simple Counter")
root.geometry("300x200")  # width x height

# Title label
title = tk.Label(root, text="Counter App", font=("Helvetica", 16))
title.pack(pady=10)

# Value label
label_value = tk.Label(root, text="0", font=("Helvetica", 24))
label_value.pack(pady=10)

# Buttons frame
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=10)

btn_inc = tk.Button(buttons_frame, text="+", width=5, command=increment)
btn_inc.grid(row=0, column=0, padx=5)

btn_dec = tk.Button(buttons_frame, text="-", width=5, command=decrement)
btn_dec.grid(row=0, column=1, padx=5)

btn_reset = tk.Button(buttons_frame, text="Reset", width=8, command=reset)
btn_reset.grid(row=0, column=2, padx=5)

# Start GUI loop
root.mainloop()
