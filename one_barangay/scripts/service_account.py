"""Authenticate Google and Firebase Service Accounts."""
import os

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials

load_dotenv()


def firestore_auth(name="firestore_app"):
    """Authenticate to cloud firestore."""
    cred = credentials.Certificate(
        {
            "type": "service_account",
            "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
            "project_id": os.getenv("FIREBASE_PROJECT_ID"),
            "private_key": os.getenv("FIREBASE_PRIVATE_KEY"),
            "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
        }
    )
    return firebase_admin.initialize_app(cred, name=name)
