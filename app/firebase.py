import os
import json
import base64
import firebase_admin
from firebase_admin import credentials, auth, firestore

# For Railway: use base64 env variable as the only source!
firebase_json_b64 = os.getenv("FIREBASE_CRED_BASE64")
if not firebase_json_b64:
    raise RuntimeError("FIREBASE_CRED_BASE64 env var is missing!")

firebase_json = json.loads(base64.b64decode(firebase_json_b64))
cred = credentials.Certificate(firebase_json)
firebase_admin.initialize_app(cred)

db = firestore.client()

def verify_token(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception:
        return None
