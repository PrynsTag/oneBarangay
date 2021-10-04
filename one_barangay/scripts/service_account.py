"""Authenticate Google and Firebase Service Accounts."""
import base64
import json
import logging
import os

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials

load_dotenv()

logger = logging.getLogger(__name__)


def firestore_auth(name="firestore_app", b64_env_name="GOOGLE_STORAGE_CREDENTIALS"):
    """Authenticate to cloud firestore using base64 decoder.

    Args:
      b64_env_name:
        (Default value = "GOOGLE_STORAGE_CREDENTIALS") A environment variable with base64 value.
      name: (Default value = "firestore_app") The name of the app if called multiple times.

    Returns:
      A newly initialized instance of App.
    """
    try:
        decoded_bytes = base64.b64decode(os.getenv(b64_env_name))
        decoded_str = str(decoded_bytes, "utf-8")
        dictionary_credential = json.loads(decoded_str)

        cred = credentials.Certificate(dictionary_credential)
        logger.info("creating credential...")

        app = firebase_admin.initialize_app(cred, name=name)
        logger.info("Credentials successfully created..")

        return app
    except ValueError as e:
        logger.exception("Credential creation failed. %s", e)
