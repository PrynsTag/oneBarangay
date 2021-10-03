"""Helper functions for OCR."""
import copy
import json
import logging
import math
from datetime import datetime

import pytz
from dotenv import load_dotenv

from one_barangay.scripts.storage_backends import AzureStorageBlob

load_dotenv()

logger = logging.getLogger(__name__)


class Script:
    """Script for helper functions."""

    def format_firestore_data(self, family_document_list):
        """Format RBI firestore data.

        Query all the data from firestore and format for json writing.
        Args:
          family_document_list: A list of family in each document

        Returns:
          The formatted data in dictionary.
        """
        # Split family_members and house_data

        copy_family_document_list = copy.deepcopy(family_document_list)

        family_member_list = [
            family_copy.pop("family_members")
            for family_copy in copy_family_document_list
            if family_copy.get("family_members", None)
        ]

        # Join house_data to each family_member
        family_member_rows = [
            house_data | family_member
            for house_data, family in zip(copy_family_document_list, family_member_list)
            for name, family_member in family.items()
        ]

        formatted_data = {
            "total": len(family_member_rows),
            "totalNotFiltered": len(family_member_rows),
            "rows": family_member_rows,
        }

        return formatted_data

    def append_to_local_json_file(self, new_data, filename="rbi_data", store_to_cloud=False):
        """Write data to json file.

        Args:
          filename: The name of the file without extension.
          new_data: The data you want to append to.
          store_to_cloud: A boolean check to store the file to GCS.

        Returns:
          None.
        """
        with open(f"{filename}.json", encoding="UTF-8") as file:
            json_data = json.load(file)

            json_data["rows"] += new_data["rows"]
            json_data["total"] = len(json_data["rows"])
            json_data["totalNotFiltered"] = json_data["total"]

        with open(f"{filename}.json", "w", encoding="UTF-8") as file:
            json.dump(json_data, file)

        if store_to_cloud:
            AzureStorageBlob().upload_local_json_file(f"{filename}.json")

    def format_file_upload_card(self, dictionary_list):
        """Format uploaded file details for display.

        Args:
          dictionary_list: A list of dictionary to format.

        Returns:
          The formatted dictionary list.
        """
        for dictionary in dictionary_list:
            size_bytes = dictionary["size"]

            if size_bytes == 0:
                return "0B"

            size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
            i = int(math.floor(math.log(size_bytes, 1024)))
            power = math.pow(1024, i)
            size = round(size_bytes / power, 2)

            dictionary["size"] = f"{size} {size_name[i]}"

            # TODO: Fix Key Error
            try:
                dictionary["last_modified"] = (
                    datetime.fromisoformat(dictionary["last_modified"].replace("Z", ""))
                    .astimezone(tz=pytz.timezone("Asia/Manila"))
                    .strftime("%B %d, %Y")
                )
            except KeyError as e:
                logger.exception("Key not found. %s", e)
        return dictionary_list
