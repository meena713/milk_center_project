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

print("✅ Firebase initialized")

ref = db.reference("test_crud")

# ---------- CREATE ----------
ref.child("test_device").set({
    "status": "created",
    "time": datetime.now().isoformat()
})
print("✅ CREATE success")

# ---------- READ ----------
data = ref.child("test_device").get()
print("📖 READ data:", data)

# ---------- UPDATE ----------
ref.child("test_device").update({
    "status": "updated"
})
print("✏️ UPDATE success")

# ---------- DELETE ----------
ref.child("test_device").delete()
print("🗑️ DELETE success")

print("🎉 ALL CRUD OPERATIONS WORKING")
