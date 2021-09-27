"""Authenticate Google and Firebase Service Accounts."""
import ast
import base64
import json
import logging
import os
import tempfile

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials

# Load .env file
load_dotenv()


def get_service_from_b64(b64_env_name="GOOGLE_STORAGE_CREDENTIALS"):
    """Authenticate using a service account for google products.

    Args:
      b64_env_name:  (Default value = "GOOGLE_STORAGE_CREDENTIALS") The base64 text.

    Returns:
      A path to file.
    """
    fd, path = tempfile.mkstemp()
    try:
        decoded_bytes = base64.b64decode(os.getenv(b64_env_name))
        decoded_str = str(decoded_bytes, "utf-8")
        json_dictionary = ast.literal_eval(decoded_str)

        with os.fdopen(fd, mode="w+") as tmp:
            logging.info("Temp file creating at %s.", path)
            json.dump(json_dictionary, tmp)
            tmp.flush()

        logging.info("File created %s.", path)

    except EOFError as e:
        logging.error("Temp File not Created. %s", e)

    return path


def firestore_auth(name="firestore_app"):
    """Authenticate to cloud firestore."""
    cred = credentials.Certificate(get_service_from_b64())
    return firebase_admin.initialize_app(cred, name=name)