"""Authenticate Google and Firebase Service Accounts."""
import logging
import os
import re

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials

load_dotenv()

logger = logging.getLogger(__name__)


def firestore_auth(name="firestore_app"):
    """Authenticate to cloud firestore."""
    try:
        dict_credential = {
            "type": "service_account",
            "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
            "project_id": os.getenv("FIREBASE_PROJECT_ID"),
            "private_key": re.sub(r"/\\n/g", "\n", os.getenv("FIREBASE_PRIVATE_KEY")),
            "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
        }
        cred = credentials.Certificate(dict_credential)
        logger.info("creating credential...")
        app = firebase_admin.initialize_app(cred, name=name)
        logger.info("Credentials successfully created..")

        return app
    except ValueError as e:
        logger.exception("Credential creation failed. %s", e)
