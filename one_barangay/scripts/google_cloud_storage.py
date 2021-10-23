"""File for Google Cloud Storage."""
import logging
import os
import urllib.parse
from pathlib import Path

import aiohttp
from aiofile import AIOFile
from gcloud.aio.storage import Storage
from google.cloud import storage

from one_barangay.local_settings import logger


async def async_upload_to_bucket(
    filepath: str,
    file_obj,
    gcs_path: str,
):
    """Upload files to bucket.

    Args:
      filepath: str: The path to the file to be uploaded.
      file_obj: The file object from reading a file
      gcs_path: str: The target bucket name and sub-folder in
                     GCS to upload to. (e.g. documents/photo)

    Returns:
      The path to the uploaded file.
    """
    async with aiohttp.ClientSession() as session:
        gcs_storage = Storage(session=session)  # skipcq
        gcs_filename = filepath.split("/")[-1]
        await gcs_storage.upload(gcs_path, gcs_filename, file_obj)
        return f"https://storage.googleapis.com/{gcs_path}/{urllib.parse.quote(gcs_filename)}"


async def upload_to_gcs_runner(
    filepath: str,
    gcs_path: str,
):
    """Call the 'async_upload_to_bucket'.

    Args:
      filepath: str: The path to the file to be uploaded.
      gcs_path: str: The target bucket name and sub-folder in GCS.

    Returns:
      The path to the uploaded file.
    """
    # target_bucket_name = target_bucket_name
    # bucket_folder = bucket_folder
    try:
        async with AIOFile(filepath, mode="rb") as afp:
            f = await afp.read()
            path = await async_upload_to_bucket(filepath, f, gcs_path)
            return path
    except FileNotFoundError as e:
        logger.exception("File not found. Make sure the file exists. %s", e)
    except OSError as e:
        logger.exception("File not uploaded. %s", e)


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

        base_dir = Path(__file__).resolve().parent.parent  # TODO: Change to user location

        destination = os.path.join(base_dir, filename)
        blob = bucket.blob(path)
        blob.download_to_filename(destination)

        logging.info("%s downloaded to %s.", filename, destination)
    except FileNotFoundError as e:
        logger.exception("File not found. Make sure the file exists. %s", e)
    except OSError as e:
        logger.exception("%s not downloaded. %s", filename, e)


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
