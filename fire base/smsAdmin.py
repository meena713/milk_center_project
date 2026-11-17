
import tkinter as tk
from tkinter import ttk,messagebox,messagebox
from tkcalendar import DateEntry
from datetime import datetime
import pyodbc
import requests
import os, sys, tkinter as tk
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime


# ---------- CONFIG ----------
SERVICE_ACCOUNT_FILE = "satya9441019881-firebase-adminsdk-fbsvc-386ddb8461.json"
DATABASE_URL = "https://satya9441019881-default-rtdb.firebaseio.com/"
# ----------------------------

# Initialize Firebase
cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
firebase_admin.initialize_app(cred, {
    "databaseURL": DATABASE_URL
})

# ---------- Fetch device IDs ----------
def fetch_device_ids():
    ref = db.reference("authorised_devices")
    data = ref.get()

    devices = []

    if data:
        for  value in data.items():
            
                devices.append(value.get("device_id"))

    return devices


# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("SMS Mamager")
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
ENTRY_W = 30       # Entry must be wider than Combo
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
tk.Label(root, text="     DEVICES__TYPE", font=LABEL_FONT)\
  .grid(row=0, column=2, sticky="W", padx=5)



# ================= ROW 1 =================
device_combo = ttk.Combobox(
             root,
             values=["Authorized_Devices", "Pending_Devices"],
             width=30,
             font=INPUT_FONT,
             state="readonly")
device_combo.grid(row=1, column=2, sticky="w")
device_combo.set("Select Device type")
#device.bind("<<ComboboxSelected>>", on_select)
#def on_select(event):
    #print("Selected Device:", combo.get())

# ================= ROW 2 =================+
tk.Label(
    root,
    text=" Device ID:",
    font=LABEL_FONT,
    width=15,          # 👈 controls label length
    anchor="w"         # align text to the left inside the label
).grid(row=2, column=0, sticky="w", padx=10)

id_combo = ttk.Combobox(
             root,
             #values=["Daily SMS", "Fortnightly SMS"],
             width=COMBO_W,
             font=INPUT_FONT,
             state="readonly")
id_combo.grid(row=2, column=1, sticky="w")
#id_combo.set("Daily SMS")


tk.Button(
    root,
    text="update_phone",
    width=12,
    font=LABEL_FONT,
    #command=update_phone
).grid(row=2, column=3,ipady=10,ipadx =30, columnspan=5)

               
# ================= ROW 3 =================

tk.Label(root, text="Pro.No.", font=LABEL_FONT)\
  .grid(row=3, column=0, sticky="w", padx=5)

pro_txt = tk.Entry(
          root,
          width=ENTRY_W,
          font=INPUT_FONT,justify = "center")
pro_txt.grid(row=3, column=1, sticky="w")
#pro_txt.bind("<Return>", fetch_phone)
#pro_txt.focus()

tk.Label(root, text="IP Address", font=LABEL_FONT)\
  .grid(row=3, column=2, sticky="w", padx=5)

ip_txt = tk.Entry(
          root,
          width=ENTRY_W,
          font=INPUT_FONT,justify = "left")
ip_txt.grid(row=3, column=3, sticky="w")
#ip_txt.bind("<Return>", fetch_ip)
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
#update_return_binding()

ph_txt.focus()
# ================= ROW 6 & 7 =================
tk.Label(root, text="message", font=LABEL_FONT)\
  .grid(row=6, column=0, columnspan=4)

msg_txt = tk.Text(
    root,
    height=10,
    width=TEXT_W,
    font=INPUT_FONT
)
msg_txt.grid(row=7, column=0, columnspan=4)
#msg_txt.bind("<Return>",generate_and_send)
# ================= BUTTON =================

tk.Button(
    root,
    text="update_phone",
    width=12,
    font=LABEL_FONT,
    #command=update_phone
).grid(row=8, column=0,ipady=10,ipadx =30, columnspan=5)

# ---------------- START ----------------
root.mainloop()
