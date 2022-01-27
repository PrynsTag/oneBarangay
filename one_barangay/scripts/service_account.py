"""Authenticate Google and Firebase Service Accounts."""
import ast
import base64
import logging
import os

import firebase_admin
from firebase_admin import credentials
from google.oauth2 import service_account

logger = logging.getLogger(__name__)


def decode_b64_to_dict(b64_env_name="GOOGLE_STORAGE_CREDENTIALS"):
    """Decode base64 value to dictionary.

    Args:
      b64_env_name:
        (Default value = "GOOGLE_STORAGE_CREDENTIALS") The value to decode.

    Returns:
      The dictionary credential or None if exception occured.
    """
    try:
        decoded_bytes = base64.b64decode(os.getenv(b64_env_name))
        decoded_str = str(decoded_bytes, "utf-8")
        dictionary_credential = ast.literal_eval(decoded_str)

        return dictionary_credential
    except ValueError as e:
        logger.exception("Decoding failed. %s", e)


def firestore_auth(name="firestore_app"):
    """Authenticate to cloud firestore using base64 decoder.

    Args:
      name: (Default value = "firestore_app") The name of the app if called multiple times.

    Returns:
      A newly initialized instance of App.
    """
    try:
        cred = credentials.Certificate(decode_b64_to_dict())
        app = firebase_admin.initialize_app(cred, name=name)
        logger.info("Credentials successfully created..")

        return app
    except ValueError as e:
        logger.exception("Credential creation failed. %s", e)


def gcloud_auth():
    """Authenticate to Google Cloud."""
    try:
        dictionary_credential = service_account.Credentials.from_service_account_info(decode_b64_to_dict())
        return dictionary_credential
    except ValueError as e:
        logger.exception("Decoding failed. %s", e)
