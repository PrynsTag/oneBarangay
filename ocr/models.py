"""Create your App models here."""
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from config.storage_backends import GoogleCloudMediaStorage


class Upload(models.Model):
    """Model to upload files and images in Google Cloud Storage."""

    upload_file = models.FileField(
        upload_to="documents/", storage=GoogleCloudMediaStorage()
    )

    def __str__(self):
        """Print File Class nicely."""
        return f"{self.upload_file.name}"

    def get_absolute_url(self):
        """Get the absolute url."""
        return reverse("scan_result", kwargs={"filename": self.upload_file.name})

    def save(self, *args, **kwargs):
        """Save file with slug filename.

        Args:
          *args: Other arguments.
          **kwargs: Keyword arguments.

        Returns:
          None
        """
        if not self.id:
            self.slug = slugify(self.upload_file.name)
        super().save(*args, **kwargs)
