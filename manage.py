#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from google.auth.exceptions import DefaultCredentialsError

from auth.service_account import get_service_from_b64


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "one_barangay.settings")
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
    except DefaultCredentialsError as exc:
        raise ImportError("The credential json or path is invalid..") from exc


if __name__ == "__main__":
    main()
