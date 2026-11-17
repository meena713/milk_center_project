import tkinter as tk
import pyodbc

root = tk.Tk()
root.title("PNo & Mobile Numbers")
root.geometry("450x300")

# ----- Frame to hold Text + Scrollbars -----
frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill="both", expand=True)

# ----- Scrollbars -----
v_scroll = tk.Scrollbar(frame, orient="vertical")
h_scroll = tk.Scrollbar(frame, orient="horizontal")

# ----- Text widget -----
txt = tk.Text(
    frame,
    wrap="none",                 # REQUIRED for horizontal scrollbar
    yscrollcommand=v_scroll.set,
    xscrollcommand=h_scroll.set,
    width=50,
    height=12
)

# Link scrollbars to text widget
v_scroll.config(command=txt.yview)
h_scroll.config(command=txt.xview)

# Layout
txt.grid(row=0, column=0, sticky="nsew")
v_scroll.grid(row=0, column=1, sticky="ns")
h_scroll.grid(row=1, column=0, sticky="ew")

frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
