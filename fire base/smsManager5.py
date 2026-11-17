import tkinter as tk
from tkinter import ttk
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# 🔧 CHANGE THESE TWO VALUES
SERVICE_ACCOUNT_FILE = "satya9441019881-firebase-adminsdk-fbsvc-386ddb8461.json"   # your downloaded file name
DATABASE_URL = "https://satya9441019881-default-rtdb.firebaseio.com/"

# Initialize Firebase
cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
firebase_admin.initialize_app(cred, {
    "databaseURL": DATABASE_URL
})


# ---------- Reading device id names ----------
def show_device_types(event=None):
    ref = db.reference("/")
    data = ref.child(combo_device_type.get()).get()

    ids = []

    if data:
        print("Authorised device ids")
        for device_id in data.keys():
            print(device_id)
            ids.append(device_id)

    # ✅ THIS MUST BE INSIDE THE FUNCTION
    if ids:
        combo_device_id["values"] = ids
        combo_device_id.set(ids[0])
        entry_mobile.delete(0, tk.END)
        entry_sign.delete(0, tk.END)
        entry_dt.delete(0, tk.END)
        entry_user.delete(0, tk.END)
        entry_adrs.delete(0, tk.END)

    else:
        combo_device_id["values"] = []
        combo_device_id.set("No devices")
        entry_mobile.delete(0, tk.END)
        entry_sign.delete(0, tk.END)
        entry_dt.delete(0, tk.END)
        entry_user.delete(0, tk.END)
        entry_adrs.delete(0, tk.END)
#------------Delete devices by device id---------------------

    
def delete_device():
    ref = db.reference("/")
    device_id = combo_device_id.get()
    device_type = combo_device_type.get()
     # Delete from pending_devices
    ref.child(device_type).child(device_id).delete()
    print(f"✅ Device with device id {device_id} deleted successfully!")

   
#------Reading device id values -------------------------
def show_device_details(event=None):
    ref = db.reference("/")

    device_id = combo_device_id.get()
    device_type = combo_device_type.get()

    if not device_id or device_id == "No devices":
        return

    data = ref.child(device_type).child(device_id).get()

    if not data:
        return

    info = data   # ✅ THIS IS THE FIX

    # clear old values
    entry_dt.delete(0, tk.END)
    entry_dt.insert(0, data.get("dt", ""))


    combo_active.set(str(data.get("active", "")))

    entry_mobile.delete(0, tk.END)
    entry_mobile.insert(0, data.get("mobile", ""))

    entry_sign.delete(0, tk.END)
    entry_sign.insert(0, data.get("signature", ""))

    entry_user.delete(0, tk.END)
    entry_user.insert(0, data.get("user", ""))

    entry_adrs.delete(0, tk.END)
    entry_adrs.insert(0, data.get("address", ""))

    # Active (ComboBox)
    #combo_active.set(str(info.get("active", "")))

#-------------update device---------------------------
def update_device_details():
    ref = db.reference("/")

    device_id = combo_device_id.get()
    device_type = combo_device_type.get()
    if not device_id:
        return

    ref = db.reference(f"{device_type}/{device_id}")

      # 👉 authorized date (TODAY only)
    dt_only = datetime.now().strftime("%Y-%m-%d")

    print(dt_only)

    ref.update({
        "mobile": entry_mobile.get(),
        "signature": entry_sign.get(),
        "dt": entry_dt.get(),
        "active": combo_active.get() == "True",
        "user": entry_user.get(),
        "address": entry_adrs.get()
    })

    print("Updated successfully")

    #reload_device_data(device_id)
#------------------on device select------------
def on_device_select(event=None):
    device_id = combo_device_id.get()
    if device_id:
        load_device_data(device_id)

#--------load device data-------------------------
def load_device_data(device_id):
    device_type = combo_data_type.get()
    ref = db.reference(device_type).child(device_id)
    data = ref.get()

    if not data:
        return
    entry_dt.delete(0, tk.END)
    entry_dt.insert(0, data.get("dt", ""))


    combo_active.set(str(data.get("active", "")))

    entry_mobile.delete(0, tk.END)
    entry_mobile.insert(0, data.get("mobile", ""))

    entry_sign.delete(0, tk.END)
    entry_sign.insert(0, data.get("signature", ""))

    entry_user.delete(0, tk.END)
    entry_user.insert(0, data.get("user", ""))

    entry_adrs.delete(0, tk.END)
    entry_adrs.insert(0, data.get("address", ""))
    
#-------authorised-----------------------------------


def authorize_device():
    root = db.reference("/")

    device_id = combo_device_id.get().strip()
    if not device_id:
        print("Device ID missing")
        return

    pending_ref = root.child("pending_devices").child(device_id)
    pending_data = pending_ref.get()

    if not pending_data:
        print("Device not found in pending_devices")
        return

    mobile = pending_data.get("mobile", "")
    signature = pending_data.get("signature", "")

    # 👉 authorized date (TODAY only)
    dt_only = datetime.now().strftime("%Y-%m-%d")

    
    authorized_data = {
        "mobile": mobile,
        "signature": signature,
        "dt": dt_only,
        "active": combo_active.get() == "True",
        "user": entry_user.get(),
        "address": entry_adrs.get()
     }
    # write authorized device
    root.child("authorized_devices").child(device_id).set(authorized_data)

    # remove from pending
    pending_ref.delete()

    print("Device authorized successfully ✅")
#----------code ending-------------------------------------------


    
root = tk.Tk()
root.title("SMS Manager")
root.geometry("520x460")

LABEL_FONT = ("Arial", 14)

# ---------- Column size control (KEY FIX) ----------
root.grid_columnconfigure(0, minsize=120)  # Label column
root.grid_columnconfigure(1, minsize=250)  # Entry / Combo
root.grid_columnconfigure(2, minsize=140)  # Button column

for r in range(1, 9):
    root.grid_rowconfigure(r, minsize=50)

# ---------- Row 0 : Title ----------
tk.Label(
    root,
    text="SMS MANAGER",
    font=("Arial", 12, "bold")
).grid(row=0, column=0, columnspan=3, pady=10)

# ---------- Row 1 : Device_typ ----------
tk.Label(root, text="Device_typ", font=LABEL_FONT)\
    .grid(row=1, column=0, sticky="w", padx=5)

combo_device_type = ttk.Combobox(
    root,
    values=["authorized_devices", "pending_devices"],
    state="readonly",
    width=24
)
combo_device_type.grid(row=1, column=1, padx=5)
combo_device_type.current(0)
combo_device_type.bind("<<ComboboxSelected>>", show_device_types)

# ---------- Row 2 : Device_ID ----------
tk.Label(root, text="Device_ID", font=LABEL_FONT)\
    .grid(row=2, column=0, sticky="w", padx=5)

combo_device_id = ttk.Combobox(root, width=24)
combo_device_id.grid(row=2, column=1, padx=5)


combo_device_id.bind("<<ComboboxSelected>>", show_device_details)
#combo_device_id.bind("<<ComboboxSelected>>", on_device_select)


tk.Button(root, text="Update", width=10, command=update_device_details)\
    .grid(row=2, column=2, padx=5)

# ---------- Row 3 : approd_dt ----------
tk.Label(root, text="approd_dt", font=LABEL_FONT)\
    .grid(row=3, column=0, sticky="w", padx=5)

entry_dt = tk.Entry(root, width=26)
entry_dt.grid(row=3, column=1, padx=5)

tk.Button(root, text="Update", width=10)\
    .grid(row=3, column=2, padx=5)

# ---------- Row 4 : Active ----------
tk.Label(root, text="Active", font=LABEL_FONT)\
    .grid(row=4, column=0, sticky="w", padx=5)

combo_active = ttk.Combobox(
    root,
    values=["True", "False"],
    state="readonly",
    width=24
)
combo_active.grid(row=4, column=1, padx=5)
combo_active.current(0)

tk.Button(root, text="Delete", width=10,command=delete_device)\
    .grid(row=4, column=2, padx=5)

# ---------- Row 5 : mobile ----------
tk.Label(root, text="mobile", font=LABEL_FONT)\
    .grid(row=5, column=0, sticky="w", padx=5)

entry_mobile=tk.Entry(root, width=26)
entry_mobile.grid(row=5, column=1, padx=5)

tk.Button(root, text="Authorise", width=10,command=authorize_device)\
    .grid(row=5, column=2, padx=5)

# ---------- Row 6 : Signature ----------
tk.Label(root, text="Signature", font=LABEL_FONT)\
    .grid(row=6, column=0, sticky="w", padx=5)

entry_sign = tk.Entry(root, width=26)
entry_sign.grid(row=6, column=1, padx=5)

tk.Button(root, text="UnAuthorise", width=10,command="")\
    .grid(row=6, column=2, padx=5)
# ---------- Row 7 : Signature ----------
tk.Label(root, text="User_name", font=LABEL_FONT)\
    .grid(row=7, column=0, sticky="w", padx=5)

entry_user = tk.Entry(root, width=26)
entry_user.grid(row=7, column=1, padx=5)
# ---------- Row 8 : Signature ----------
tk.Label(root, text="user_Address", font=LABEL_FONT)\
    .grid(row=8, column=0, sticky="w", padx=5)

entry_adrs = tk.Entry(root, width=26)
entry_adrs.grid(row=8, column=1, padx=5)


root.mainloop()
