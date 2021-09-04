"""Create your App models here."""
from django.db import models

from config.storage_backends import GoogleCloudMediaStorage


class File(models.Model):
    """Model to upload files and images in Google Cloud Storage."""

    file_field = models.FileField(
        upload_to="documents/", storage=GoogleCloudMediaStorage()
    )
    image_field = models.ImageField(
        upload_to="images/", storage=GoogleCloudMediaStorage()
    )

    def __str__(self):
        """Print File Class nicely."""
        return f"{self.image_field.name}, ({self.image_field.size})"
