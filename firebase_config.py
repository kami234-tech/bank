import os
import json
import firebase_admin
from firebase_admin import credentials

# Load the Firebase Admin credentials from the environment variable
firebase_credentials_json = os.environ.get('FIREBASE_ADMIN_CREDENTIALS')
if firebase_credentials_json:
    firebase_credentials = json.loads(firebase_credentials_json)
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred)
else:
    # Handle the case where the environment variable is not set
    raise ValueError("FIREBASE_ADMIN_CREDENTIALS environment variable is not set.")
