"""File for cloud storage backends."""
import json
import os
from abc import ABC
from json import JSONDecodeError
from urllib.parse import urljoin

from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobClient, ContentSettings
from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import setting

from one_barangay.local_settings import logger


class GoogleCloudMediaStorage(GoogleCloudStorage, ABC):
    """GoogleCloudMediaStorage extensions suitable for handing Django's Media files.

    Requires following settings:
    MEDIA_URL, GS_MEDIA_BUCKET_NAME

    In addition to
    https://django-storages.readthedocs.io/en/latest/backends/gcloud.html
    """

    def __init__(self, *args, **kwargs):
        """Initialize media bucket name."""
        if not settings.MEDIA_URL:
            raise Exception("MEDIA_URL has not been configured")
        kwargs["bucket_name"] = setting("GS_MEDIA_BUCKET_NAME")
        super().__init__(*args, **kwargs)

    def url(self, name):
        """URL method that doesn't call Google.

        Args:
          name: The name of file to fetch.

        Returns:
          The URL path.
        """
        return urljoin(settings.MEDIA_URL, name)


class GoogleCloudStaticStorage(GoogleCloudStorage, ABC):
    """GoogleCloudStaticStorage extensions suitable for handing Django's Static files.

    Requires following settings:
    STATIC_URL, GS_STATIC_BUCKET_NAME

    In addition to
    https://django-storages.readthedocs.io/en/latest/backends/gcloud.html
    """

    def __init__(self, *args, **kwargs):
        """Initialize static bucket name."""
        if not settings.STATIC_URL:
            raise Exception("STATIC_URL has not been configured")
        kwargs["bucket_name"] = setting("GS_STATIC_BUCKET_NAME")
        super().__init__(*args, **kwargs)

    def url(self, name):
        """URL method that doesn't call Google.

        Args:
          name: The name of file to fetch.

        Returns:
          The URL path.
        """
        return urljoin(settings.STATIC_URL, name)


class AzureStorageBlob:
    """Class to interact with Azure Storage."""

    def __init__(self, sas_token=None, container_name=None, blob_name=None):
        """Initialize Azure properties and credentials."""
        self.sas_token = os.getenv("AZURE_STORAGE_CONTAINER_SAS") if sas_token is None else sas_token
        self.container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME") if container_name is None else container_name
        self.blob_name = os.getenv("AZURE_STORAGE_BLOB_NAME") if blob_name is None else blob_name
        self.account_url = "https://onebaragay.blob.core.windows.net"
        self.file_url = f"{self.account_url}/{self.container_name}/{self.blob_name}"
        self.blob_client = BlobClient.from_blob_url(blob_url=self.sas_token)

    def upload_local_json_file(self, file_path, content_type="application/json"):
        """Upload local json file to Azure.

        Args:
          file_path: Local json file path to upload.
          content_type: (Default value = "application/json") The content type of file to upload.

        Returns:
          None.
        """
        try:
            with open(file_path, "rb") as blob_file:
                self.blob_client.upload_blob(
                    data=blob_file,
                    overwrite=True,
                    content_settings=ContentSettings(content_type=content_type),
                )
            logger.info("File uploaded to Azure.")
        except ResourceExistsError as e:
            logger.error("Resource Exists. Add overwrite=True in your upload_blob.\n%s", e)

    def read_json_file(self):
        """Read json file from Azure."""
        try:
            blob_download = self.blob_client.download_blob()
            blob_content = blob_download.readall().decode("utf-8")

            return json.loads(blob_content)
        except JSONDecodeError as e:
            logger.error(e)

    def upload_json_data(self, json_data):
        """Upload json data to Azure.

        Args:
          json_data: The json data to upload.

        Returns:
         None.
        """
        try:
            self.blob_client.upload_blob(
                data=json.dumps(json_data),
                overwrite=True,
                content_settings=ContentSettings(content_type="application/json"),
            )
            logger.info("File uploaded to Azure.")
        except JSONDecodeError as e:
            logger.error("File NOT uploaded to Azure. %s", e)

    def append_to_json_data(self, new_row):
        """Append a row to json data.

        Args:
          new_row: A list of dictionary row to append.

        Returns:
          The newly appended json.
        """
        json_data = self.read_json_file()

        json_data["rows"] += new_row
        json_data["total"] = len(json_data["rows"])
        json_data["totalNotFiltered"] = json_data["total"]

        return json_data
