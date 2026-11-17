import tkinter as tk
from tkinter import ttk

# ---------------- Window ----------------
root = tk.Tk()
root.title("ownSMS APK Manager")
root.geometry("560x420")

FONT_LBL = ("Arial", 11)
FONT_TITLE = ("Arial", 16, "bold")

# ---------------- Grid spacing ----------------
root.grid_columnconfigure(0, minsize=160)
root.grid_columnconfigure(1, minsize=230)
root.grid_columnconfigure(2, minsize=140)

for r in range(1, 9):
    root.grid_rowconfigure(r, minsize=40)

# ---------------- Title (Row 0) ----------------
tk.Label(
    root,
    text="ownSMS APK Manager",
    font=FONT_TITLE
).grid(row=0, column=0, columnspan=3, pady=15)

# ---------------- Dummy callbacks ----------------
def action(name):
    print(f"{name} clicked")

# ---------------- Row 1 ----------------
tk.Label(root, text="Device Type", font=FONT_LBL)\
    .grid(row=1, column=0, sticky="w", padx=10)

combo_device_type = ttk.Combobox(
    root, values=["Authorized", "Pending"],
    state="readonly", width=24
)
combo_device_type.grid(row=1, column=1, padx=10)

tk.Button(root, text="Update", width=12,
          command=lambda: action("Update"))\
    .grid(row=1, column=2, padx=10, pady=5)

# ---------------- Row 2 ----------------
tk.Label(root, text="Device ID", font=FONT_LBL)\
    .grid(row=2, column=0, sticky="w", padx=10)

combo_device_id = ttk.Combobox(
    root, values=["DEV001", "DEV002"],
    width=24
)
combo_device_id.grid(row=2, column=1, padx=10)

tk.Button(root, text="Delete", width=12,
          command=lambda: action("Delete"))\
    .grid(row=2, column=2, padx=10, pady=5)

# ---------------- Row 3 ----------------
tk.Label(root, text="Active", font=FONT_LBL)\
    .grid(row=3, column=0, sticky="w", padx=10)

combo_active = ttk.Combobox(
    root, values=["True", "False"],
    state="readonly", width=24
)
combo_active.grid(row=3, column=1, padx=10)

tk.Button(root, text="Authorize", width=12,
          command=lambda: action("Authorize"))\
    .grid(row=3, column=2, padx=10, pady=5)

# ---------------- Row 4 ----------------
tk.Label(root, text="Approved Date", font=FONT_LBL)\
    .grid(row=4, column=0, sticky="w", padx=10)

entry_dt = tk.Entry(root, width=27)
entry_dt.grid(row=4, column=1, padx=10)

tk.Button(root, text="UnAuthorize", width=12,
          command=lambda: action("UnAuthorize"))\
    .grid(row=4, column=2, padx=10, pady=5)

# ---------------- Row 5 ----------------
tk.Label(root, text="Mobile Number", font=FONT_LBL)\
    .grid(row=5, column=0, sticky="w", padx=10)

entry_mobile = tk.Entry(root, width=27)
entry_mobile.grid(row=5, column=1, padx=10)

tk.Button(root, text="Update", width=12)\
    .grid(row=5, column=2, padx=10, pady=5)

# ---------------- Row 6 ----------------
tk.Label(root, text="Signature", font=FONT_LBL)\
    .grid(row=6, column=0, sticky="w", padx=10)

entry_sign = tk.Entry(root, width=27)
entry_sign.grid(row=6, column=1, padx=10)

tk.Button(root, text="Delete", width=12)\
    .grid(row=6, column=2, padx=10, pady=5)

# ---------------- Row 7 ----------------
tk.Label(root, text="Remarks", font=FONT_LBL)\
    .grid(row=7, column=0, sticky="w", padx=10)

entry_remark = tk.Entry(root, width=27)
entry_remark.grid(row=7, column=1, padx=10)

tk.Button(root, text="Save", width=12)\
    .grid(row=7, column=2, padx=10, pady=5)

# ---------------- Row 8 ----------------
tk.Label(root, text="Last Updated", font=FONT_LBL)\
    .grid(row=8, column=0, sticky="w", padx=10)

entry_updated = tk.Entry(root, width=27)
entry_updated.grid(row=8, column=1, padx=10)

tk.Button(root, text="Close", width=12,
          command=root.destroy)\
    .grid(row=8, column=2, padx=10, pady=5)

# ---------------- Start ----------------
root.mainloop()
