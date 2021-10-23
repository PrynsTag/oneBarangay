"""Custom class Emailer."""

import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class Emailer:
    """Class emailer."""

    def __init__(self, from_email: str, to_emails: str, subject: str, html_content: str):
        """Emailer initialization."""
        self.from_email = from_email
        self.to_emails = to_emails
        self.subject = subject
        self.html_content = html_content

    def send(self):
        """Send email."""
        message = Mail(
            from_email=self.from_email,
            to_emails=self.to_emails,
            subject=self.subject,
            html_content=self.html_content,
        )

        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        sg.send(message)
