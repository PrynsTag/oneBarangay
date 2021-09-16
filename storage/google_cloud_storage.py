"""File for Google Cloud Storage."""
import logging
import os
import urllib
from pathlib import Path

import aiohttp
from aiofile import AIOFile
from dotenv import load_dotenv
from gcloud.aio.storage import Storage
from google.cloud import storage

from auth.service_account import get_service_from_b64

load_dotenv()


async def async_upload_to_bucket(
    filepath: str,
    file_obj,
    target_bucket_name: str,
    bucket_folder: str,
):
    """Upload files to bucket.

    Args:
      filepath: str: The path to the file to be uploaded.
      file_obj: The file object from reading a file
      target_bucket_name: str: The bucket name from which to download to.
      bucket_folder: str: The folder from the bucket name from which to download to.

    Returns:
      The path to the uploaded file.
    """
    service_account_path = get_service_from_b64()
    async with aiohttp.ClientSession() as session:
        storage = Storage(service_file=service_account_path, session=session)
        gcs_filename = filepath.split("/")[-1]
        await storage.upload(
            target_bucket_name, f"{bucket_folder}/{gcs_filename}", file_obj
        )
        return f"https://storage.googleapis.com/\
                {target_bucket_name}/{bucket_folder}/\
                {urllib.parse.quote(gcs_filename)}"


async def upload_to_gcs_runner(filepath: str):
    """Call the 'async_upload_to_bucket'.

    Args:
      filepath: str: The path to the file to be uploaded.

    Returns:
      The path to the uploaded file.
    """
    target_bucket_name = str(os.getenv("GS_MEDIA_BUCKET_NAME"))
    bucket_folder = str(os.getenv("FILE_BUCKET_FOLDER"))
    try:
        async with AIOFile(filepath, mode="rb") as afp:
            f = await afp.read()
            path = await async_upload_to_bucket(
                filepath, f, target_bucket_name, bucket_folder
            )
            return path
    except Exception as e:
        logging.error(f"File not uploaded. {e}")


def download_from_gcs(
    filename: str,
    target_bucket_name: str,
    bucket_folder: str,
):
    """Download file from Google Cloud Storage bucket.

    Args:
      filename: str: The name of file being downloaded.
      target_bucket_name: str: The bucket name from which to download to.
      bucket_folder: str: The folder from the bucket name from which to download to.

    Returns:
      None.
    """
    try:
        storage_client = storage.Client(os.getenv("GOOGLE_PROJECT_ID"))
        bucket_name = storage_client.get_bucket(target_bucket_name)
        bucket = storage_client.get_bucket(bucket_name)
        path = os.path.join(bucket_folder, filename)

        base_dir = (
            Path(__file__).resolve().parent.parent
        )  # TODO: Change to user location

        destination = os.path.join(base_dir, filename)
        blob = bucket.blob(path)
        blob.download_to_filename(destination)

        logging.info(f"{filename} downloaded to {destination}.")
    except Exception as e:
        logging.error(f"{filename} not downloaded. {e}")


# if __name__ == "__main__":
# Sample Calls to Uploading to GCS
# asyncio.run(
#     upload_to_gcs_runner(
#         "<your_absolute_filepath>"
#     )
# )

# Sample Calls to Downloading from GCS
# download_from_gcs(
#     "kath.png",
#     str(os.getenv("GS_MEDIA_BUCKET_NAME")),
#     str(os.getenv("FILE_BUCKET_FOLDER")),
# )
