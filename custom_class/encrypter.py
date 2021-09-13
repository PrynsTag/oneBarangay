import base64


class Encrypter:
    """This class encrypts and decrypts texts."""

    def __init__(self, text: str):
        self.text = text

    def __str__(self):
        return self.text

    def code_encoder(self):
        """This class converts text to base64."""
        text = self.text
        value_bytes = text.encode("ascii")
        base64_bytes = base64.urlsafe_b64encode(value_bytes)
        base64_message = base64_bytes.decode("ascii")
        return str(base64_message)

    def code_decoder(self):
        """This class converts text to base64."""
        value_bytes = self.text.encode("ascii")
        base64_bytes = base64.urlsafe_b64decode(value_bytes)
        base64_message = base64_bytes.decode("ascii")
        return str(base64_message)
