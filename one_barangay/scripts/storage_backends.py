"""File for cloud storage backends."""
import json
import logging
import os
import sys
import threading
from abc import ABC
from json import JSONDecodeError
from urllib.parse import urljoin

import boto3
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobClient, ContentSettings
from boto3.exceptions import S3UploadFailedError
from botocore.exceptions import ClientError
from django.conf import settings
from dotenv import load_dotenv
from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import setting

logger = logging.getLogger(__name__)

load_dotenv()


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


class ProgressPercentage:
    """Class for progress bar UI."""

    def __init__(self, filename):
        """Initialize file properties."""
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        """Call for displaying progress."""
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                f"\r{self._filename}  {self._seen_so_far} / {self._size}  {percentage:.2f}"
            )
            sys.stdout.flush()


class AwsS3:
    """Class to interact with AWS."""

    def __init__(self, bucket_name):
        """Initialize AWS properties and credentials."""
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("aws_access_key_id"),
            aws_secret_access_key=os.getenv("aws_secret_access_key"),
            aws_session_token=os.getenv("aws_session_token"),
        )
        self.s3_resource = boto3.resource(
            "s3",
            aws_access_key_id=os.getenv("aws_access_key_id"),
            aws_secret_access_key=os.getenv("aws_secret_access_key"),
            aws_session_token=os.getenv("aws_session_token"),
        ).Bucket(bucket_name)

    def upload_local_json_file(self, file_name, canonical_id, object_name=None):
        """Upload local json file to AWS.

        Args:
          file_name: The name of a file to upload.
          canonical_id: The canonical id of a user.
          object_name: (Default value = None) The object name of a file.

        Returns:
          None.
        """
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        # Upload the file
        try:
            self.s3_client.upload_file(
                file_name,
                self.bucket_name,
                object_name,
                Callback=ProgressPercentage(file_name),
                ExtraArgs={
                    "ContentType": "application/json",
                    "GrantRead": "uri=http://acs.amazonaws.com/groups/global/AllUsers",
                    "GrantFullControl": f"id={canonical_id}",
                },
            )
        except ClientError as e:
            logger.error(e)
        except S3UploadFailedError as e:
            logger.error(e)

    def append_to_local_json_file(self, key, canonical_id, new_row):
        """Append row to local json file.

        Args:
          key: The key or filename of a file.
          canonical_id: Canonical ID of a user.
          new_row: The new row to append to.

        Returns:
          None.
        """
        s3_object = self.s3_resource.Object(key=key)

        json_data = json.load(s3_object.get()["Body"])

        json_data["rows"] += new_row
        json_data["total"] = len(json_data["rows"])
        json_data["totalNotFiltered"] = json_data["total"]

        with open("rbi_data.json", "w", encoding="UTF-8") as file:
            json.dump(json_data, file)

        s3_object.put(
            Body=json.dumps(json_data),
            ContentType="application/json",
            GrantRead="uri=http://acs.amazonaws.com/groups/global/AllUsers",
            GrantFullControl=f"id={canonical_id}",
        )


class AzureStorageBlob:
    """Class to interact with Azure Storage."""

    def __init__(self, sas_token=None, container_name=None, blob_name=None):
        """Initialize Azure properties and credentials."""
        self.sas_token = (
            os.getenv("AZURE_STORAGE_CONTAINER_SAS") if sas_token is None else sas_token
        )
        self.container_name = (
            os.getenv("AZURE_STORAGE_CONTAINER_NAME")
            if container_name is None
            else container_name
        )
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
