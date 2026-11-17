import tkinter as tk
from tkinter import messagebox
import pyodbc

DB_PATH = r"D:/teja/eswar.mdb"

def fetch_phone(event=None):
    pno = pno_entry.get().strip()

    if not pno.isdigit():
        messagebox.showwarning("Invalid", "Please enter valid PNo")
        return

    try:
        conn = pyodbc.connect(
            r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
            f"DBQ={DB_PATH};"
        )
        cursor = conn.cursor()

        cursor.execute(
            "SELECT pone FROM sbcards WHERE pno = ?",
            (pno,)
        )
        row = cursor.fetchone()

        if row:
            phone_entry.delete(0, tk.END)
            phone_entry.insert(0, row[0])
        else:
            phone_entry.delete(0, tk.END)
            messagebox.showinfo("Not Found", "PNo not found")

        conn.close()

    except Exception as e:
        messagebox.showerror("DB Error", str(e))


# ---------------- GUI ----------------
root = tk.Tk()
root.title("PNo Lookup")
root.geometry("300x120")

tk.Label(root, text="PNo").grid(row=0, column=0, padx=10, pady=10)
pno_entry = tk.Entry(root)
pno_entry.grid(row=0, column=1)

tk.Label(root, text="Phone No").grid(row=1, column=0, padx=10)
phone_entry = tk.Entry(root)
phone_entry.grid(row=1, column=1)

# 🔑 Enter key binding
pno_entry.bind("<Return>", fetch_phone)

pno_entry.focus()

root.mainloop()
