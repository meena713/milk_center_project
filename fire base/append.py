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

print("✅ Firebase initialized")

root = db.reference("/")

# ---------- APPEND to pending_devices ----------
pending_ref = root.child("pending_devices")

pending_ref.child("DEVICE_1001").set({
    "mobile": "9000000001",
    "signature": "SIG-PENDING-001",
    "requested_at": datetime.now().isoformat()
})

print("✅ pending_devices data added")

# ---------- APPEND to authorized_devices ----------
auth_ref = root.child("authorized_devices")

auth_ref.child("DEVICE_2001").set({
    "mobile": "9000000002",
    "signature": "SIG-AUTH-001",
    "active": True,
    "approved_at": datetime.now().isoformat()
})

print("✅ authorized_devices data added")

print("🎉 Sample data appended successfully")
