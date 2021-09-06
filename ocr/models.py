"""Create your App models here."""
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from config.storage_backends import GoogleCloudMediaStorage


class UploadFile(models.Model):
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

    def get_absolute_url(self):
        """Get the absolute url."""
        return reverse("scan_result", kwargs={"name": self.upload_file.name})

    def save(self, *args, **kwargs):
        """Save file with slug filename.

        Args:
          *args: Other arguments.
          **kwargs: Keyword arguments.

        Returns:
          None
        """
        if not self.id:
            self.slug = slugify(self.upload_file)
        super(UploadFile, self).save(*args, **kwargs)
