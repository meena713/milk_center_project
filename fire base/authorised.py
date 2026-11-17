import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# ---------------- CONFIG ----------------
SERVICE_ACCOUNT_FILE = "satya9441019881-firebase-adminsdk-fbsvc-386ddb8461.json"
DATABASE_URL = "https://satya9441019881-default-rtdb.firebaseio.com/"

# Initialize Firebase (only once)
cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
firebase_admin.initialize_app(cred, {"databaseURL": DATABASE_URL})
print("✅ Firebase initialized\n")

# Root reference
root = db.reference("/")

# ---------------- FUNCTIONS ----------------

def list_pending_devices():
    """List all pending devices"""
    pending_ref = root.child("pending_devices")
    data = pending_ref.get()
    if not data:
        print("❌ No pending devices found.")
        return {}
    
    print("\n📋 Pending Devices:")
    print("-" * 50)
    for key, value in data.items():
        mobile = value.get("mobile", "N/A")
        signature = value.get("signature", "N/A")
        requested_at = value.get("requested_at", "N/A")

        if isinstance(requested_at, (int, float)):
            requested_at = datetime.fromtimestamp(requested_at / 1000).strftime("%Y-%m-%d %H:%M:%S")

        print(f"Device ID: {key} | Mobile: {mobile} | Signature: {signature} | Requested: {requested_at}")
    print("-" * 50)
    return data

def approve_device_by_mobile():
    """Approve a pending device using its mobile number"""
    pending = list_pending_devices()
    if not pending:
        return

    mobile_to_approve = input("Enter the mobile number to authorize: ").strip()
    if not mobile_to_approve:
        print("❌ Mobile number cannot be empty.")
        return

    found = None
    for device_id, info in pending.items():
        if info.get("mobile") == mobile_to_approve:
            found = (device_id, info)
            break

    if not found:
        print(f"❌ No pending device found with mobile {mobile_to_approve}")
        return

    device_id, info = found

    # ✅ Move to authorized_devices
    root.child("authorized_devices").child(device_id).set({
        "mobile": info.get("mobile"),
        "signature": info.get("signature"),
        "active": True,
        "approved_at": datetime.now().strftime("%Y-%m-%d")
    })

    # ✅ Delete from pending_devices
    root.child("pending_devices").child(device_id).delete()

    print(f"✅ Device with mobile {mobile_to_approve} authorized successfully!")

def main_menu():
    """Main menu for admin"""
    while True:
        print("\n===== Pending Devices Admin Menu =====")
        print("1. List pending devices")
        print("2. Approve device by mobile number")
        print("3. Exit")

        choice = input("Enter choice (1/2/3): ").strip()

        if choice == "1":
            list_pending_devices()
        elif choice == "2":
            approve_device_by_mobile()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("❌ Invalid choice. Enter 1, 2, or 3 only.")

# ---------------- RUN ----------------
if __name__ == "__main__":
    main_menu()
