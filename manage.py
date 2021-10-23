#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from google.auth.exceptions import DefaultCredentialsError

from one_barangay.local_settings import logger


def main():
    """Run administrative tasks."""
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "one_barangay.settings")
    # os.environ["FIRESTORE_DATASET"] = "rbi"
    # os.environ["FIRESTORE_EMULATOR_HOST"] = "127.0.0.1:8080"
    # os.environ["FIRESTORE_EMULATOR_HOST_PATH"] = "127.0.0.1:8080/firestore"
    # os.environ["FIRESTORE_HOST"] = "http://127.0.0.1:8080"
    # os.environ["FIRESTORE_PROJECT_ID"] = "onebarangay-malanday"

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

    if os.getenv("GAE_ENV", "").startswith("standard"):
        try:
            import googleclouddebugger  # For GCP pylint: disable=import-outside-toplevel

            googleclouddebugger.enable(
                module="oneBarangay",
                version="v1.0",
                breakpoint_enable_canary=True,
            )
            logger.info("Cloud Debugger started.")

        except ImportError as exc:
            logger.exception(
                "Couldn't import Cloud Debugger. "
                "Are you sure its installed and "
                "is available in your requirements.txt?\n%s",
                exc,
            )
        except DefaultCredentialsError as e:
            logger.exception("The credential json or path is invalid.. %s", e)


if __name__ == "__main__":
    main()
