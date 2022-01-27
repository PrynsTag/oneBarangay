"""File for working with json."""
import json
from typing import Any


class UserManagementJSON:
    """Class for working with json."""

    def __init__(self, filename: str = "auth_data.json"):
        """Initialize JSONFunctions attributes."""
        self.filename = filename

    def add_row_to_auth_json(self, user: dict) -> None:
        """Add a row to json file.

        Args:
          user: Dict: The user to be added.

        Returns:
          None.
        """
        dictionary_file = self.read_auth_to_json()

        dictionary_file["rows"].append(user)
        dictionary_file["total"] += 1
        dictionary_file["totalNotFiltered"] = dictionary_file["total"]

        self.store_auth_to_json(dictionary_file)

    def modify_row_in_auth_json(self, user_info: dict) -> None:
        """Modify a user in json file.

        Args:
          user_info: Dict: The information of user to be modified.

        Returns:
          None.
        """
        dictionary_file = self.read_auth_to_json()

        user_index = next(
            (idx for idx, item in enumerate(dictionary_file["rows"]) if item["uid"] == user_info["uid"]),
            None,
        )

        if user_index is not None:
            dictionary_file["rows"][user_index] = user_info

            self.store_auth_to_json(dictionary_file)

    def delete_row_in_auth_json(self, uid: str) -> None:
        """Delete a row in json file.

        Args:
          uid: str: The user id to be deleted.

        Returns:
          None.
        """
        dictionary_file = self.read_auth_to_json()

        user_index = next((idx for idx, item in enumerate(dictionary_file["rows"]) if item["uid"] == uid), None)

        if user_index is not None:
            del dictionary_file["rows"][user_index]

            dictionary_file["total"] -= 1
            dictionary_file["totalNotFiltered"] = dictionary_file["total"]

            self.store_auth_to_json(dictionary_file)

    def get_user_auth_data(self, uid: str) -> dict:
        """Get user in json file.

        Args:
          uid: str: The user id to be searched.

        Returns:
          The dictionary user data.
        """
        dictionary_file = self.read_auth_to_json()
        user_data = next((user for user in dictionary_file["rows"] if user["uid"] == uid), None)
        return user_data

    def format_auth_data(self, user_list: list[dict[str, Any]]) -> dict:
        """Format a list of user for data table.

        Args:
          user_list: List[Dict[str, Any]]: A list of user from firebase auth.

        Returns:
          The formatted dictionary.
        """
        return {
            "total": len(user_list),
            "totalNotFiltered": len(user_list),
            "rows": user_list,
        }

    def read_auth_to_json(self) -> dict:
        """Read json file."""
        with open(self.filename, encoding="UTF-8") as file:
            dictionary_file = json.load(file)

        return dictionary_file

    def store_auth_to_json(self, formatted_dictionary: dict) -> None:
        """Store formatted dictionary data to json file.

        Args:
          formatted_dictionary: Dict: A formatted dictionary data.

        Returns:
          None.
        """
        with open(self.filename, "w", encoding="UTF-8") as file:
            json.dump(formatted_dictionary, file)
