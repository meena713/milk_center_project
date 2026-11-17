
import tkinter as tk
from tkinter import ttk,messagebox,messagebox
from tkcalendar import DateEntry
from datetime import datetime
import pyodbc
import requests
import os, sys, tkinter as tk

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
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
cur2 = conn1.cursor()
#-------------------------------------


#------------query1---------------
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
#------------query2---------------
def fetch_fn_data(from_date, to_date, pro_no):
    query = """
    SELECT *
    FROM milk_receipts
    WHERE receipt_date BETWEEN ? AND ?
    AND producer_no = ?
    AND record_status = 'Active'
    ORDER BY milk_type
     """

    cur2.execute(query, (from_date, to_date, pro_no))
#rows = cursor.fetchall()
    return cur2.fetchall()
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

#-------------------IP_FETCH ------
def fetch_ip(event=None):
    #ip_txt.delete("0",tk.END)
    ip = ip_txt.get().strip()
    if  ip=="":
        messagebox.showinfo("message","enter valid ip adrdress")
        ip_txt.insert(tk.END,"10.46.42.25")        
        pro_txt.focus()
    elif ip_txt !="":    
        pro_txt.focus()
#-------------------genarate and send ------
def generate_and_send(event=None):
    producer_no = pro_txt.get()
    
    mlk_date = d_entry.get()

    session = day_combo.get()

    mobile = ph_txt.get()
    gateway_ip =ip_txt.get()

    rows = fetch_milk_data(producer_no, mlk_date, session)
    message = build_message(rows, producer_no, mlk_date, session)
    if message:

        msg_txt.delete("1.0", tk.END)
        msg_txt.insert(tk.END, message)
    else:
        messagebox.showinfo("mesage","data not found")

    send_sms_via_gateway(gateway_ip, mobile, message)
    #messagebox.showinfo("SMS Status", Return)
    pro_txt.delete(0,tk.END)
    ph_txt.delete(0,tk.END)
    pro_txt.focus()

#-------------------------send message-----------
import requests

def send_sms_via_gateway(gateway_ip, receiver_phone, message):
    gateway_ip = gateway_ip.strip()   # 🔥 removes spaces

    url = f"http://{gateway_ip}:8080/"
    params = {
        "phone": receiver_phone,
        "msg": message
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        print("Server response:", response.text)
    except Exception as e:
        print("Connection error:", e)


#------------end----------------------------------
#--------------update phone number----------------
def update_phone(event=None):
    pno = pro_txt.get().strip()
    phone = ph_txt.get().strip()
    if not pno.isdigit() or not phone.isdigit():
        messagebox.showwarning("Invalid", "Please enter valid PNo or mobileno")
        return

    try:
        DB_PATH = r"D:/teja/eswar.mdb"

        DB1_PATH = r"D:\McSAS - NeW\EXE\DATA\McSAS.mdb"
        DB1_PWD  = "GooglE@888"
        conn1 = pyodbc.connect(
                r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
                f"DBQ={DB1_PATH};"
                f"PWD={DB1_PWD};"
             )
            
        cur2 = conn1.cursor()
        cur2.execute(
             "UPDATE PRODUCERS_ADDITIONAL_DETAILS SET mobile_no=? WHERE pno=?",
             (phone,pno)
            )
        conn1.commit()
        messagebox.showinfo("Message","Phone number updated")
    except Exception as e:
        messagebox.showerror("DB Error", str(e))

#--------------------fetch phone number------------
def fetch_phone(event=None):
    pno = pro_txt.get().strip()

    if not pno.isdigit():
        messagebox.showwarning("Invalid", "Please enter valid PNo")
        
        return pro_txt.focus()
    try:
        

        DB1_PATH = r"D:\McSAS - NeW\EXE\DATA\McSAS.mdb"
        DB1_PWD  = "GooglE@888"
        conn1 = pyodbc.connect(
                r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
                f"DBQ={DB1_PATH};"
                f"PWD={DB1_PWD};"
             )
            
        cur2 = conn1.cursor()
        cur2.execute(
            "SELECT mobile_no FROM PRODUCERS_ADDITIONAL_DETAILS WHERE  pno = ?",
            (pno,)
        )

        row = cur2.fetchone()

        if row:
            ph_txt.delete(0, tk.END)
            ph_txt.insert(0, row[0])
            ph_txt.focus()
        else:
            ph_txt.delete(0, tk.END)
            messagebox.showinfo("Not Found", "PNo not found")
            pro_txt.delete(0,tk.END)
            pro_txt.focus()
        conn1.close()

    except Exception as e:
        messagebox.showerror("DB Error", str(e))


    #ph_txt.focus()
#--------------------end-----------------------------------------
def fetch_rec_vcd(even=None):
    from decimal import Decimal

    try:
        yr = yr_combo.get()
        mnth = month_combo.get()
        fn = fn_combo.get()
        from_dt, to_dt = get_from_to_date(yr, mnth, fn)

        pno = pro_txt.get()
        #dtl = f"{month_combo.get()[:3]}{yr_combo.get()} {fn_combo.get()}"

        DB1_PATH = r"D:\McSAS - NeW\EXE\DATA\McSAS.mdb"
        DB1_PWD  = "GooglE@888"

        conn1 = pyodbc.connect(
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
            f"DBQ={DB1_PATH};"
            f"PWD={DB1_PWD};"
        )

        cur2 = conn1.cursor()
        cur2.execute(
            """SELECT * FROM RECOVERIES_ENTRY
               WHERE recovery_date BETWEEN ? AND ?
               AND producer_no = ?""",
            (from_dt, to_dt, pno)
        )

        rows = cur2.fetchall()

        rtot = Decimal('0')
        msg = "REC:\n"

        for r in rows:
            amt = Decimal(str(r.amount or 0))
            rtot += amt

            txt = (r.recovery_name or "")
            txt = txt.replace('(', ':')

            msg += f"{txt} : {amt:0.2f}\n"

        msg += f"totRec : {rtot:0.2f}"

        return rtot, msg

    except Exception as e:
        messagebox.showerror("DB Error", str(e))
        return Decimal('0'), ""   # ✅ VERY IMPORTANT

    finally:
        try:
            conn1.close()
        except:
            pass

#------------------fetch revovery detals-------------------------
def fetch_rec(even=None):
    from decimal import Decimal
    pno = pro_txt.get()
    dtl = f"{month_combo.get()[:3]}{yr_combo.get()} {fn_combo.get()}"

    try:
        conn = pyodbc.connect(
            r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
            f"DBQ={DB_PATH};"
        )
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM sprec WHERE dtl= ? and pno = ?",
            (dtl,pno,)
        )
        rows = cursor.fetchall()
        rtot = Decimal('0')
        msg = ""
        msg =( f"REC:\n"
            )
        for r in rows:
            rtot+= Decimal(str(r.amount))
            txt = r.rec[:-2]
            txt = txt.replace('(',':')
           
            msg += f"{txt} : {r.amount:>0.2f}\n"

                
        msg+=(f"{'totRec'} : {rtot:>5.2F}"
            )
        #print(msg)
        return rtot,msg
        conn.close()

    except Exception as e:
        messagebox.showerror("DB Error", str(e))




#----------------fn section start----------
from datetime import date
import calendar

def get_from_to_date(year, month_name, fn):
    year = int(year)

    # Convert month name to month number
    month = list(calendar.month_name).index(month_name)

    if fn == "1st":
        from_dt = date(year, month, 1)
        to_dt   = date(year, month, 15)
    else:  # 2nd fn
        last_day = calendar.monthrange(year, month)[1]
        from_dt = date(year, month, 16)
        to_dt   = date(year, month, last_day)

    return from_dt, to_dt
#--------------------------end-----------------------------

def build_fn_msg(rows2, from_date, to_date, pro_no):
    from decimal import Decimal
    if not rows2:
        return "No data found"

    fst = rows2[0]
    camt = Decimal('0')
    bamt = Decimal('0')

    msg2 = (
        f"PNo:{pro_no} {fst.producer_name}\n"
        f"{month_combo.get().strip()[:3]}{yr_combo.get().strip()} {fn_combo.get().strip()}\n"
    )

    for r in rows2:
        if r.milk_type == 'C':
            camt += Decimal(str(r.amount))
        else:
            bamt += Decimal(str(r.amount))

    msg2 += (
        f"{'Bm_amt':<8}:{bamt:>10.2f}\n"
        f"{'Cm_amt':<8}:{camt:>10.2f}\n"
        f"{'Tot_amt':<8}:{(camt+bamt):>10.2f}\n"
    )

    rtot, msg = fetch_rec_vcd()

    msg3 = (
        f"{msg2}"
        f"{msg}\n"
        f"{'Net':<8}:{(camt+bamt-rtot):>10.2f}\n"
    )

    return msg3
    #print(msg3)
#----------------coding end----------------
def send_fn_data(event=None):
    yr = yr_combo.get()
    mn = month_combo.get()
    fn = fn_combo.get()
    pro_no = pro_txt.get().strip()

    if not (yr and mn and fn and pro_no):
        print("Please select year, month, FN and producer number")
        return

    # 1. get date range
    from_date, to_date = get_from_to_date(yr, mn, fn)

    # 2. fetch data
    rows2 = fetch_fn_data(from_date, to_date, pro_no)

    # 3. build message
    msg3 = build_fn_msg(rows2, from_date, to_date, pro_no)

    #print(msg3)
  
   
    if msg3:

        msg_txt.delete("1.0", tk.END)
        msg_txt.insert(tk.END, msg3)
    else:
        messagebox.showinfo("mesage","data not found")
    mobile = ph_txt.get().strip()
    gateway_ip =ip_txt.get().strip()

    send_sms_via_gateway(gateway_ip, mobile, msg3)
    #messagebox.showinfo("SMS Status", Return)
    pro_txt.delete(0,tk.END)
    ph_txt.delete(0,tk.END)
    pro_txt.focus()


#-------------end-----------------------------------------    
def update_return_binding(event=None):
    # Remove previous Enter binding
    ph_txt.unbind("<Return>")

    # Bind based on combobox value
    if type_combo.get().strip() == 'Daily SMS':
        ph_txt.bind("<Return>", generate_and_send)
    else:
        ph_txt.bind("<Return>", send_fn_data)
# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("SMS Sender")
try:
    root.iconbitmap(resource_path("sms.ico"))
except Exception as e:
    print("Icon load failed:", e)
    
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
#yr_combo.bind("<<ComboboxSelected>>", combo_changed)

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
#month_combo.bind("<<ComboboxSelected>>", combo_changed)

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
# Bind combobox selection change
type_combo.bind("<<ComboboxSelected>>", update_return_binding)

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
#fn_combo.bind("<<ComboboxSelected>>", combo_changed)
               
# ================= ROW 3 =================

tk.Label(root, text="Pro.No.", font=LABEL_FONT)\
  .grid(row=3, column=0, sticky="w", padx=5)

pro_txt = tk.Entry(
          root,
          width=ENTRY_W,
          font=INPUT_FONT,justify = "center")
pro_txt.grid(row=3, column=1, sticky="w")
pro_txt.bind("<Return>", fetch_phone)
#pro_txt.focus()

tk.Label(root, text="IP Address", font=LABEL_FONT)\
  .grid(row=3, column=2, sticky="w", padx=5)

ip_txt = tk.Entry(
          root,
          width=ENTRY_W,
          font=INPUT_FONT,justify = "left")
ip_txt.grid(row=3, column=3, sticky="w")
ip_txt.bind("<Return>", fetch_ip)
ip_txt.focus()



# ================= ROW 4 & 5 =================

tk.Label(root, text="Receiver Phone", font=LABEL_FONT)\
  .grid(row=4, column=0, columnspan=6, pady=(4, 0))

ph_txt = tk.Entry(
         root,
         width=ENTRY_W_BOTTOM,
         font=INPUT_FONT)
ph_txt.grid(row=5, column=0, columnspan=6)
# Initial binding (IMPORTANT)
update_return_binding()

ph_txt.focus()
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
