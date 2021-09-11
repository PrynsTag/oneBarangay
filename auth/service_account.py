"""Authenticate Google and Firebase Service Accounts."""
import ast
import base64
import json
import os
import tempfile

from dotenv import load_dotenv
from firebase_admin import credentials, initialize_app

# Load .env file
load_dotenv()


def firebase_authentication(b64_env_name="GOOGLE_STORAGE_CREDENTIALS"):
    """Authenticate service account in firebase.

    Args:
      b64_env_name:  (Default value = "GOOGLE_STORAGE_CREDENTIALS") The base64 encoded json file.

    Returns:
      A certificate object.
    """
    fd, path = tempfile.mkstemp()
    try:
        decoded_bytes = base64.b64decode(os.getenv(b64_env_name))
        decoded_str = str(decoded_bytes, "utf-8")
        json_dictionary = ast.literal_eval(decoded_str)

        with os.fdopen(fd, mode="w+") as tmp:
            json.dump(json_dictionary, tmp)
            tmp.flush()

        cred = credentials.Certificate(path)
        app = initialize_app(cred)
    finally:
        os.remove(path)

    return app
