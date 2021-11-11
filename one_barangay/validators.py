"""Validator functions for input fields."""
import os

import magic
from django.core.exceptions import ValidationError


def validate_extension(file):
    """Validate accepted file extensions.

    Args:
      file: The file to be validated.

    Returns:
      None.

    Raises:
      ValidationError.
    """
    valid_mime_types = ["application/pdf", "image/jpeg", "image/png", "image/jpg"]
    file_mime_type = magic.from_buffer(file.read(2048), mime=True)

    if file_mime_type not in valid_mime_types:
        raise ValidationError("Unsupported file type.")

    valid_file_extensions = [".pdf", ".jpeg", ".png", ".jpg"]
    ext = os.path.splitext(file.name)[1]

    if ext.lower() not in valid_file_extensions:
        raise ValidationError("Unacceptable file extension.")


def validate_image(file):
    """Validate accepted file extensions.

    Args:
      file: The file to be validated.

    Returns:
      None.

    Raises:
      ValidationError.
    """
    valid_mime_types = ["image/jpeg", "image/png", "image/jpg"]
    file_mime_type = magic.from_buffer(file.read(2048), mime=True)

    if file_mime_type not in valid_mime_types:
        raise ValidationError("Unsupported file type. Use JPG, JPEG, and PNG files.")

    valid_file_extensions = [".jpeg", ".png", ".jpg"]
    ext = os.path.splitext(file.name)[1]

    if ext.lower() not in valid_file_extensions:
        raise ValidationError("Unacceptable file extension. Use JPG, JPEG, and PNG files.")
