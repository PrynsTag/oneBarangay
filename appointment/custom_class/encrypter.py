"""Custom class encrypter."""
import base64

from django.http import Http404


class Encrypter:
    """This class encrypts and decrypts texts."""

    def __init__(self, text: str):
        """Initialize class with text."""
        self.text = text

    def __str__(self):
        """Output text."""
        return self.text

    def code_encoder(self):
        """Convert text to base64."""
        try:
            text = self.text
            value_bytes = text.encode("ascii")
            base64_bytes = base64.urlsafe_b64encode(value_bytes)
            base64_message = base64_bytes.decode("ascii")
            return str(base64_message)
        except UnicodeDecodeError as incorrect_code:
            raise Http404 from incorrect_code

    def code_decoder(self):
        """Convert text to base64."""
        try:
            value_bytes = self.text.encode("ascii")
            base64_bytes = base64.urlsafe_b64decode(value_bytes)
            base64_message = base64_bytes.decode("ascii")
            return str(base64_message)
        except UnicodeDecodeError as incorrect_code:
            raise Http404 from incorrect_code
