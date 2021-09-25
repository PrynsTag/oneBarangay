#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from google.auth.exceptions import DefaultCredentialsError

from auth.service_account import get_service_from_b64


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "one_barangay.settings")
    os.environ["FIRESTORE_DATASET"] = "rbi"
    os.environ["FIRESTORE_EMULATOR_HOST"] = "127.0.0.1:8080"
    os.environ["FIRESTORE_EMULATOR_HOST_PATH"] = "127.0.0.1:8080/firestore"
    os.environ["FIRESTORE_HOST"] = "http://127.0.0.1:8080"
    os.environ["FIRESTORE_PROJECT_ID"] = "onebarangay-malanday"

    try:
        from django.core.management import (  # For Django pylint: disable=import-outside-toplevel
            execute_from_command_line,
        )
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

    try:
        import googleclouddebugger  # For GCP pylint: disable=import-outside-toplevel

        googleclouddebugger.enable(
            breakpoint_enable_canary=True,
            service_account_json_file=get_service_from_b64(),
        )
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Cloud Debugger. "
            "Are you sure its installed and "
            "is available in your requirements.txt?"
        ) from exc
    except DefaultCredentialsError as e:
        raise ImportError("The credential json or path is invalid..") from e


if __name__ == "__main__":
    main()
