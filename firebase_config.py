import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

cred_json = os.environ.get("FIREBASE_ADMIN_CREDENTIALS")
cred = credentials.Certificate(json.loads(cred_json))
firebase_admin.initialize_app(cred)

db = firestore.client()
