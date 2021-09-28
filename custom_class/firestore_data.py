"""Module for firestore operations."""
import datetime
import time

import firebase_admin
from firebase_admin import auth, credentials, firestore

from custom_class.dateformatter import DateFormatter
from custom_class.encrypter import Encrypter
from one_barangay.scripts.service_account import firestore_auth

firestore_auth = firestore_auth(name="appointment_firestore_app")


class FirestoreData:
    """Manage firestore data."""

    def __init__(self):
        """Initialize firebase connection."""
        self.db = firestore.client(firestore_auth)

    def verify_identification(self, firstname: str, middlename: str, lastname: str):
        """For verification of identification.

        Args:
          firstname: str: user firstname
          middlename: str: user middlename
          lastname: str: user lastname

        Returns:
          resident information.
        """
        user_list = []

        user_collection = self.db.collection("test_users")
        query = (
            user_collection.where("first_name", "==", firstname)
            .where("middle_name", "==", middlename)
            .where("last_name", "==", lastname)
        ).stream()

        for info in query:
            user_list.append(info.to_dict())

        if len(user_list) == 1:
            return user_list
        else:
            f_name_result, results = self.query_list("first_name", firstname)

            if results:
                for info in f_name_result:
                    user_list.append(info)

            m_name_result, results = self.query_list("middle_name", middlename)

            if results:
                for info in m_name_result:
                    user_list.append(info)

            l_name_result, results = self.query_list("last_name", lastname)

            if results:
                for info in l_name_result:
                    user_list.append(info)

            return user_list

    def query_list(self, search_key: str, value: str):
        """Search user with specific key and value to compare.

        Args:
          search_key: str: key dictionary in firebase firestore data
          value: str: value to be search

        Returns:
          results searched in firebase firestore user collection
        """
        user_list = []
        user_collection = self.db.collection("test_users")
        query = user_collection.where(search_key, "==", value).stream()

        for info in query:
            user_list.append(info.to_dict())

        if len(user_list) != 0:
            return user_list, True
        else:
            return None, False

    def delete_account_auth(self):
        """Delete all account."""
        account_ids = []
        appointment_ids = []
        doc_ref_account = self.db.collection("test_users")
        doc_ref_appointment = self.db.collection("appointments")

        for result in doc_ref_account.stream():
            account_ids.append(result.id)

            doc_ref_appointment_id = doc_ref_appointment.where(
                "user_uid", "==", result.id
            ).stream()

            for result in doc_ref_appointment_id:
                appointment_ids.append(result.id)

            auth.delete_users(account_ids)

            time.sleep(1)

        for id in account_ids:
            doc_ref_account.document(id).delete()
            time.sleep(1)

        for id in appointment_ids:
            doc_ref_appointment.document(id).delete()
            time.sleep(1)

    def search_verification(self):
        """Search account for verification."""
        user_ref = self.db.collection("test").where("age", "==", 22).get()

        for res in user_ref:
            print(res.to_dict())

    def day_appointments(self, date: datetime.date = datetime.date.today(), utc_offset: int = 0):
        """Get appointment date in firestore.

        You can also manually search the appointment just input the date (year, month, day)

        Args:
          date: datetime.date:  (Default value = datetime.date.today())
          utc_offset: int:  (Default value = 0)

        Returns:
          get appointment list in firebase firestore
        """
        count = 1

        year = int((str(date)).split(" ")[0].split("-")[0])
        month = int((str(date)).split(" ")[0].split("-")[1])
        day = int((str(date)).split(" ")[0].split("-")[2])

        start_date = datetime.datetime.strptime(
            f"{year}-{month}-{day - 1} {23}:{11}:{59}",
            "%Y-%m-%d %H:%M:%S",
        )

        start_date_delta = start_date - datetime.timedelta(hours=utc_offset)

        end_date = datetime.datetime.strptime(
            f"{year}-{month}-{day} {23}:{11}:{59}", "%Y-%m-%d %H:%M:%S"
        )

        end_date_delta = end_date - datetime.timedelta(hours=utc_offset)

        date_ref = (
            self.db.collection("appointments")
            .where("start_appointment", ">=", start_date_delta)
            .where("start_appointment", "<=", end_date_delta)
            .order_by("start_appointment")
        )
        result = date_ref.get()

        appointment_list = []

        for count, appointment in enumerate(result):
            count += 1
            appointment_list.append(appointment.to_dict())

        return count, appointment_list

    def search_appointment(self, document_id: str):
        """Search user appointment.

        Args:
          document_id: str: input user document id

        Returns:
          user appointment info
        """
        return self.db.collection("appointments").document(document_id).get().to_dict()

    def search_appointment_userId(self, user_uid: str):
        """Search appointemnt using user uid.

        Args:
          user_uid: str: input user's uid
        Returns:
          : appointment details of user
        """
        appointment_ref = (
            self.db.collection("appointments").where("user_uid", "==", user_uid).stream()
        )

        user_list = []

        for user in appointment_ref:
            user_list.append(user.to_dict())

        if len(user_list) == 1:
            return user_list[0]

    def search_appointment_day(self, year: int, month: int, day: int, utc_offset: int = 0):
        """Search appointment using date.

        Args:
          year: int: year of appointment
          month: int: month of appointment
          day: int: day of appointment
          utc_offset: int:  (Default value = 0)
        Returns:
          list of appointments in specific date.
        """
        count = 1

        start_date = datetime.datetime.strptime(
            f"{year}-{month}-{day - 1} {23}:{11}:{59}",
            "%Y-%m-%d %H:%M:%S",
        )

        start_date_delta = start_date - datetime.timedelta(hours=utc_offset)

        end_date = datetime.datetime.strptime(
            f"{year}-{month}-{day} {23}:{11}:{59}", "%Y-%m-%d %H:%M:%S"
        )

        end_date_delta = end_date - datetime.timedelta(hours=utc_offset)

        date_ref = (
            self.db.collection("appointments")
            .where("start_appointment", ">", start_date_delta)
            .where("start_appointment", "<=", end_date_delta)
            .order_by("start_appointment")
        )
        result = date_ref.get()

        appointment_list = []

        for count, appointment in enumerate(result):
            count += 1
            appointment_list.append(appointment.to_dict())

        return count, appointment_list

    def search_document(self, document_id):
        """Search appointment using document id.

        Args:
          document_id: document id of appointment

        Returns:
          appointment details using document id
        """
        appointment_ref = self.db.collection("appointments").document(document_id)
        appointment = appointment_ref.get()

        return appointment.to_dict()

    def update_appointment_status(self, document_id):
        """Change appointment/document status.

        Args:
          document_id: document id of appointment

        Returns:
          Change firebase firestore document status
        """
        appointment_ref = self.db.collection("appointments").document(document_id)
        get_appointment = appointment_ref.get().to_dict()

        if get_appointment["status"] == "request":
            appointment_ref.update({"status": "process"})
            return True

        elif get_appointment["status"] == "process":
            appointment_ref.update({"status": "get"})
            return True

        elif get_appointment["status"] == "get":
            appointment_ref.update({"status": "completed"})
            return True

    def resched_appointment(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
        document_id: str,
        utc_offset: int,
        datetime: datetime,
        query_list: list,
    ):
        """Reschedule appointment.

        Args:
          year: int: year of appointment
          month: int: month of appointment
          day: int: day of appointment
          hour: int: hour of appointment
          minute: int: minute of appointment
          second: int: second of appointment
          document_id: str: document id of appointment in firebase firestore
          utc_offset: int: specify timezone
          datetime: datetime: package datetime
          query_list: list: list down keys for firebase firestore in appointment collection

        Returns:
          'list of appointments with specific time and date'
        """
        start_day = DateFormatter().datetime_timedelta_hours(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            utc_offset=utc_offset,
            operator="-",
        )

        start_day = start_day - datetime.timedelta(days=1)

        end_day = DateFormatter().datetime_timedelta_hours(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            utc_offset=utc_offset,
            operator="-",
        )

        appointment_ref = self.db.collection("appointments")
        query_appointment = (
            appointment_ref.where("start_appointment", ">", start_day)
            .where("start_appointment", "<=", end_day)
            .order_by("start_appointment", direction=firestore.Query.ASCENDING)
        )

        results = query_appointment.stream()

        appointment_list = []

        for appointment in results:
            data_appointment = appointment.to_dict()

            print(f"Data Appointment: {data_appointment}")

            appointment_info = DateFormatter().datetime_firestore_utc(
                query_key=query_list,
                data_dict=data_appointment,
                utc_offset=utc_offset,
            )

            data_appointment = appointment_info
            appointment_list.append(appointment_info)

        admin_ref = self.db.collection("admin_settings")
        query_admin = admin_ref.document("appointment").get()
        query_admin_result = query_admin.to_dict()
        admin_start_appointment = query_admin_result["start_appointment"] + datetime.timedelta(
            hours=utc_offset
        )
        admin_end_appointment = query_admin_result["end_appointment"] + datetime.timedelta(
            hours=utc_offset
        )

        start_datetime = datetime.datetime(
            year=year,
            month=month,
            day=day,
            hour=admin_start_appointment.hour,
            minute=query_admin_result["start_appointment"].minute,
            second=query_admin_result["start_appointment"].second,
        )

        end_datetime = datetime.datetime(
            year=year,
            month=month,
            day=day,
            hour=admin_end_appointment.hour,
            minute=query_admin_result["end_appointment"].minute,
            second=query_admin_result["end_appointment"].second,
        )

        datetime_list = []

        while start_datetime < end_datetime:
            datetime_list.append(start_datetime)
            start_datetime = start_datetime + datetime.timedelta(
                minutes=query_admin_result["time_interval"]
            )

        check_available = []

        # Adding available status on appointment list
        for datetime_info in datetime_list:
            exist = False
            for appointment in appointment_list:
                if datetime_info == appointment["start_appointment"]:
                    appointment["available"] = False
                    check_available.append(appointment)
                    exist = True
                    break

            if exist:
                continue
            else:
                check_available.append(
                    {
                        "available": True,
                        "start_appointment": datetime_info,
                        "end_appointment": datetime_info + datetime.timedelta(minutes=15),
                    }
                )

        # For Current Appointment
        encrypt = Encrypter(text=document_id).code_encoder()
        current_user = DateFormatter().datetime_firestore_utc(
            query_key=query_list,
            data_dict=self.search_document(document_id=encrypt),
            utc_offset=8,
        )

        check_current = []

        for check_info in check_available:
            if check_info["start_appointment"] == current_user["start_appointment"]:
                check_info["current_user"] = True
                check_current.append(check_info)
            else:
                check_current.append(check_info)

        return check_current

    def set_appointment_settings(
        self,
        start_appointment: datetime,
        end_appointment: datetime,
        time_interval: int = 15,
    ):
        """Set start, end and time interval of residents' appointments.

        Args:
          start_appointment: datetime:
          end_appointment: datetime:
          time_interval: int:  (Default value = 15)

        Returns:
            change appointment settings for admin.
        """
        self.db.collection("admin_settings").document("appointment").set(
            {
                "start_appointment": 7,
                "end_appointment": 17,
                "time_interval": 15,
            }
        )

        print("Settings for appointment is success")

    def out_appointment_settings(self):
        """Get admin appointment settings."""
        settings_ref = self.db.collection("admin_settings").document("appointment").get()

        return settings_ref.to_dict()
