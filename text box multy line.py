import tkinter as tk
import pyodbc
root = tk.Tk()
root.title("PNo & Mobile Numbers")
root.geometry("400x300")
#-------------text box----------------
txt = tk.Text(root, width=45, height=12)
txt.pack(padx=10, pady=10)
#----------------------------=function--------
def load_data():
    txt.delete("1.0", tk.END)   # clear old data

    conn = pyodbc.connect(
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        r"DBQ=D:\teja\eswar.mdb;"
    )
    cursor = conn.cursor()

    cursor.execute("""
        SELECT pno, pone
        FROM sbcards
        WHERE relation = 'self'
    """)

    row = cursor.fetchone()     # like rs.MoveFirst

    while row:
        line = f"PNo: {row.pno}   Mobile: {row.pone}\n"
        txt.insert(tk.END, line)

        row = cursor.fetchone() # ← MoveNext

    cursor.close()
    conn.close()
#---------------BUTTON--------------------------
tk.Button(root, text="Load Data", command=load_data).pack(pady=5)

root.mainloop()

