import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Load credentials from environment variable
firebase_credentials_json = os.getenv("FIREBASE_ADMIN_CREDENTIALS")
if not firebase_credentials_json:
    raise ValueError("Missing FIREBASE_ADMIN_CREDENTIALS env variable")

firebase_credentials = json.loads(firebase_credentials_json)

# Initialize Firebase app
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred)

# Export Firestore DB
db = firestore.client()
