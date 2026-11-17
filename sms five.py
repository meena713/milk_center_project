import tkinter as tk
from tkinter import ttk,messagebox,messagebox
from tkcalendar import DateEntry
from datetime import datetime
import pyodbc
import requests
#-------------paths------------
DB_PATH = r"D:/teja/eswar.mdb"

DB1_PATH = r"D:\McSAS - NeW\EXE\DATA\McSAS.mdb"
DB1_PWD  = "GooglE@888"
conn1 = pyodbc.connect(
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    f"DBQ={DB1_PATH};"
    f"PWD={DB1_PWD};"
)
cursor1 = conn1.cursor()

#------------query---------------
def fetch_milk_data(producer_no, mlk_date, session):
    sql = """
    SELECT ltrs, fat, snf, rate, amount,milk_type,producer_name
    FROM milk_receipts
    WHERE record_status = 'Active'
      AND producer_no = ?
      AND receipt_date = ?
      AND milk_session = ?
    """
    cursor1.execute(sql, (producer_no, mlk_date, session))
    return cursor1.fetchall()
#---------------end----------------------

#---------------build mesaage-----------------------

def build_message(rows, producer_no, mlk_date, session):
    if not rows:
        return None

    first =rows[0]
    msg = ""
    msg = (
        f"PNo:{pro_txt.get()}{'':3}"
        f"{first.producer_name}\n"
        f"Dt: {d_entry.get()}{'':3}"
        f"{day_combo.get()}\n"
      ) 
    for r in rows:

     msg += (
        f"{r.milk_type}{'':1}"
        f"{'Lts:' } {r.ltrs:.1f}{'':3}"
        f"{'FAT:'} {r.fat:.1f}{'':3}"
        f"{'SNF:'    :1} {r.snf:.1f}\n"
        f"{'Rate:'   :1}{r.rate:.2f}\n"
        f"{'Amt:' :1} {r.amount:.2f}\n"
     )
    #print(msg)
    return msg
#--------------ending-------------------

#-------------------genarate and send ------
def generate_and_send(event=None):
    producer_no = pro_txt.get()
    #producer_no = 77
    
    mlk_date = d_entry.get()
    #mlk_date = "31/12/2025"

    session = day_combo.get()
    #session = "AM"

    mobile = ph_txt.get()
    #mobile = 6302342220

    rows = fetch_milk_data(producer_no, mlk_date, session)
    message = build_message(rows, producer_no, mlk_date, session)


    if message:
      msg_txt.delete("1.0", tk.END)
      msg_txt.insert(tk.END, message)
      resp = send_sms_httpmsg(mobile, message)
    else:
       messagebox.showinfo("Message","Message not found") 
    #messagebox.showinfo("SMS Status", resp)
    #msg_txt.delete("1.0",tk.END)
    ph_txt.delete(0,tk.END)
    pro_txt.delete(0,tk.END)
    pro_txt.focus()

#-------------------------send message-----------

#--------------update phone number----------------
def update_phone(event=None):
    pno = pro_txt.get().strip()
    phone = ph_txt.get().strip()
    if not pno.isdigit() or not phone.isdigit():
        messagebox.showwarning("Invalid", "Please enter valid PNo or mobileno")
        return

    try:
        conn = pyodbc.connect(
            r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
            f"DBQ={DB_PATH};"
        )
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE sbcards SET pone=? WHERE relation= 'self' and pno = ?",
            (phone,pno,)
        )
        conn.commit()
        messagebox.showinfo("Message","Phone number updated")
    except Exception as e:
        messagebox.showerror("DB Error", str(e))

#--------------------fetch phone number------------
def fetch_phone(event=None):
    pno = pro_txt.get().strip()

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
            "SELECT pone FROM sbcards WHERE relation= 'self' and pno = ?",
            (pno,)
        )
        row = cursor.fetchone()

        if row:
            ph_txt.delete(0, tk.END)
            ph_txt.insert(0, row[0])
        else:
            ph_txt.delete(0, tk.END)
            messagebox.showinfo("Not Found", "PNo not found")

        conn.close()

    except Exception as e:
        messagebox.showerror("DB Error", str(e))


    ph_txt.focus()



# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("SMS Scheduler")

# App size
win_w = 450
win_h = 390

# Get screen size
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

# Calculate position
x = screen_w - win_w
y = screen_h - win_h

# Set geometry
root.geometry(f"{win_w}x{win_h}+{x}+{y}")


root.resizable(False, False)

for i in range(5):
    root.grid_columnconfigure(i, weight=1)


# ---------------- FONTS ----------------
LABEL_FONT = ("Segoe UI", 9, "bold")
INPUT_FONT = ("Segoe UI", 9, "bold")

# ---------------- WIDTH RULES ----------------
COMBO_W = 16        # for DatePicker & Combos
ENTRY_W = 18        # Entry must be wider than Combo
ENTRY_W_BOTTOM = 32
TEXT_W = 44

# ---------------- STYLE ----------------
style = ttk.Style()
style.configure("TCombobox", font=INPUT_FONT)

#==============about time==============
yr_list = []
for i in range(datetime.now().year-2,datetime.now().year+3):
     yr_list.append(i)

import calendar
month_list = [calendar.month_name[m] for m in range(1, 13)]


# ================= ROW 0 =================
tk.Label(root, text="Date", font=LABEL_FONT)\
  .grid(row=0, column=0, sticky="w", padx=5)

d_entry = DateEntry(root, width=COMBO_W, font=INPUT_FONT,date_pattern = "dd/mm/yyy")
d_entry.grid(row=0, column=1, sticky="w")

tk.Label(root, text="Year", font=LABEL_FONT)\
  .grid(row=0, column=2, sticky="w", padx=5)

yr_combo = ttk.Combobox(
           root,
           values=yr_list,
           width=COMBO_W,
           font=INPUT_FONT,
           state="readonly")
yr_combo.grid(row=0, column=3, sticky="w")
yr_combo.set(datetime.now().year)

# ================= ROW 1 =================
tk.Label(root, text="Day", font=LABEL_FONT)\
  .grid(row=1, column=0, sticky="w", padx=5)

day_combo = ttk.Combobox(
              root,
              values=["AM","PM"],
              width=COMBO_W,
              font=INPUT_FONT,
              state="readonly")
day_combo.grid(row=1, column=1, sticky="w")
if(datetime.now().hour>=12):
 day_combo.set("PM")
else:    
 day_combo.set("AM")

tk.Label(root, text="Month", font=LABEL_FONT)\
  .grid(row=1, column=2, sticky="w", padx=5)

month_combo = ttk.Combobox(
              root,
              values=month_list,
              width=COMBO_W,
              font=INPUT_FONT,
              state="readonly")
month_combo.grid(row=1, column=3, sticky="w")
month_combo.set(calendar.month_name[datetime.now().month])

# ================= ROW 2 =================+

tk.Label(root, text="SMS Type", font=LABEL_FONT)\
  .grid(row=2, column=0, sticky="w", padx=5)

type_combo = ttk.Combobox(
             root,
             values=["Daily SMS", "Fortnightly SMS"],
             width=COMBO_W,
             font=INPUT_FONT,
             state="readonly")
type_combo.grid(row=2, column=1, sticky="w")
type_combo.set("Daily SMS")


tk.Label(root, text="Fortnight", font=LABEL_FONT)\
  .grid(row=2, column=2, sticky="w", padx=5)

fn_combo = ttk.Combobox(
           root,
           values=["1st", "2nd"],
           width=COMBO_W,
           font=INPUT_FONT,
           state="readonly")
fn_combo.grid(row=2, column=3, sticky="w")
if(datetime.now().day<=15):
  fn_combo.set("1st")
else:
  fn_combo.set("2nd")
               
# ================= ROW 3 =================

tk.Label(root, text="Pro.No.", font=LABEL_FONT)\
  .grid(row=3, column=0, sticky="w", padx=5)

pro_txt = tk.Entry(
          root,
          width=ENTRY_W,
          font=INPUT_FONT,justify = "center")
pro_txt.grid(row=3, column=1, sticky="w")
pro_txt.bind("<Return>", fetch_phone)
pro_txt.focus()


# ================= ROW 4 & 5 =================

tk.Label(root, text="Receiver Phone", font=LABEL_FONT)\
  .grid(row=4, column=0, columnspan=6, pady=(4, 0))

ph_txt = tk.Entry(
         root,
         width=ENTRY_W_BOTTOM,
         font=INPUT_FONT)
ph_txt.grid(row=5, column=0, columnspan=6)
ph_txt.bind("<Return>",generate_and_send)

# ================= ROW 6 & 7 =================
tk.Label(root, text="message", font=LABEL_FONT)\
  .grid(row=6, column=0, columnspan=4)

msg_txt = tk.Text(
    root,
    height=8,
    width=TEXT_W,
    font=INPUT_FONT
)
msg_txt.grid(row=7, column=0, columnspan=4)
msg_txt.bind("<Return>",generate_and_send)
# ================= BUTTON =================

tk.Button(
    root,
    text="update_phone",
    width=12,
    font=LABEL_FONT,
    command=update_phone
).grid(row=8, column=0,ipady=10,ipadx =30, columnspan=5)

# ---------------- START ----------------
root.mainloop()
