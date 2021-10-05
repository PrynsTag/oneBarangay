"""Module for firestore operations."""
import datetime
import time

from django.http import Http404
from firebase_admin import auth, firestore

from appointment.custom_class.dateformatter import DateFormatter
from appointment.custom_class.dummy import Dummy
from appointment.custom_class.encrypter import Encrypter
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
          firstname: str:
          middlename: str:
          lastname: str:

        Returns:
            resident information.
        """
        user_list = []

        user_collection = self.db.collection("users")
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
          search_key: str:
          value: str:

        Returns:
            results searched in firebase firestore user collection
        """
        user_list = []
        user_collection = self.db.collection("users")
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
        doc_ref_account = self.db.collection("users")
        doc_ref_appointment = self.db.collection("appointments")

        for account_ref_result in doc_ref_account.stream():
            account_ids.append(account_ref_result.id)

            doc_ref_appointment_id = doc_ref_appointment.where(
                "user_uid", "==", account_ref_result.id
            ).stream()

            for appointment_result in doc_ref_appointment_id:
                appointment_ids.append(appointment_result.id)

            auth.delete_users(account_ids)

            time.sleep(1)

        for account_id in account_ids:
            doc_ref_account.document(account_id).delete()
            time.sleep(1)

        for appointment_id in appointment_ids:
            doc_ref_appointment.document(appointment_id).delete()
            time.sleep(1)

    def search_verification(self):
        """Search account for verification."""
        user_ref = self.db.collection("test").where("age", "==", 22).get()

        user_list = []

        for res in user_ref:
            user_list.append(res.to_dict())

        return user_ref

    def day_appointments(self, date: datetime.date, utc_offset: int):
        """Get appointment date in firestore.

        You can also manually search the appointment just input the date (year, month, day)

        Args:
          date: datetime.date:  (Default value = datetime.date.today())
          utc_offset: int:  (Default value = 0)
          date: datetime.date:  (Default value = datetime.date.today())
          utc_offset: int:  (Default value = 0)

        Returns:
            get appointment list in firebase firestore
        """
        year = date.year
        month = date.month
        day = date.day

        start_date = datetime.datetime.strptime(
            f"{year}-{month}-{day} {23}:{11}:{59}",
            "%Y-%m-%d %H:%M:%S",
        )

        start_date_delta = start_date - datetime.timedelta(days=1, hours=utc_offset)

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

        for appointment in result:
            appointment_list.append(appointment.to_dict())

        count = len(appointment_list)
        return count, appointment_list

    def search_appointment(self, document_id: str):
        """Search user appointment.

        Args:
          document_id: str: input user document id
          document_id: str:

        Returns:
            user appointment info
        """
        return self.db.collection("appointments").document(document_id).get().to_dict()

    def search_appointment_userid(self, user_uid: str):
        """Search appointemnt using user uid.

        Args:
          user_uid: str:

        Returns:
            appointment details of user
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
          year: int:
          month: int:
          day: int:
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

        for result_count, appointment in result:
            count = result_count + 1
            appointment_list.append(appointment.to_dict())

        return count, appointment_list

    def search_document(self, document_id: str, collection_name: str):
        """Search appointment using document id.

        Args:
          document_id: document id of appointment
          document_id: str:
          collection_name: str:

        Returns:
            appointment details using document id
        """
        appointment_ref = self.db.collection(collection_name).document(document_id)
        appointment = appointment_ref.get()

        return appointment.to_dict()

    def update_appointment_status(self, document_id: str, collection_name: str):
        """Change appointment/document status.

        Args:
          document_id: document id of appointment
          document_id: str:
          collection_name: str:

        Returns:
            Change firebase firestore document status
        """
        appointment_ref = self.db.collection(collection_name).document(document_id)
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
          year: int:
          month: int:
          day: int:
          hour: int:
          minute: int:
          second: int:
          document_id: str:
          utc_offset: int:
          query_list: list:

        Returns:
            'list of appointments with specific time and date'
        """
        full_date = datetime.datetime.now()
        date = datetime.date.today()

        start_day = DateFormatter(full_date=full_date, date=date).datetime_timedelta_hours(
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

        end_day = DateFormatter(full_date=full_date, date=date).datetime_timedelta_hours(
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

            appointment_info = DateFormatter(
                full_date=full_date, date=date
            ).datetime_firestore_utc(
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
                # Not exists(datetime_info): 2021-10-02 16:15:00
                new_document_id = Encrypter(
                    text=Dummy().document_id(
                        year=datetime_info.year,
                        month=datetime_info.month,
                        day=datetime_info.day,
                        hour=datetime_info.hour,
                        minute=datetime_info.minute,
                    )
                ).code_encoder()

                check_available.append(
                    {
                        "available": True,
                        "start_appointment": datetime_info,
                        "end_appointment": datetime_info + datetime.timedelta(minutes=15),
                        "document_id": new_document_id,
                    }
                )

        # For Current Appointment
        encrypt = Encrypter(text=document_id).code_encoder()
        current_user = DateFormatter(full_date=full_date, date=date).datetime_firestore_utc(
            query_key=query_list,
            data_dict=self.search_document(document_id=encrypt, collection_name="appointments"),
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
        start_appointment: datetime.datetime,
        end_appointment: datetime.datetime,
        time_interval: int = 15,
    ):
        """Set start, end and time interval of residents' appointments.

        Args:
          start_appointment: datetime:
          end_appointment: datetime:
          time_interval: int:  (Default value = 15)
          start_appointment: datetime.datetime:
          end_appointment: datetime.datetime:
          time_interval: int:  (Default value = 15)

        Returns:
            change appointment settings for admin.
        """
        self.db.collection("admin_settings").document("appointment").set(
            {
                "start_appointment": start_appointment,
                "end_appointment": end_appointment,
                "time_interval": time_interval,
            }
        )

    def out_appointment_settings(self):
        """Get admin appointment settings."""
        settings_ref = self.db.collection("admin_settings").document("appointment").get()

        return settings_ref.to_dict()

    def reschedule(self, old_id, new_id):
        """Reschedule appointment.

        Args:
          old_id: old document id
          new_id: new document id

        Returns:
            None change appointment time
        """
        old_data = self.search_appointment(document_id=old_id)
        # new_date_time = datetime.datetime.strptime(
        #     Encrypter(text=new_id).code_decoder(), "%Y%m%d-%H%M"
        # )

        start_appointment = Encrypter(text=new_id).code_decoder()

        # end_appointment = start_appointment + datetime.timedelta(minutes=15)
        #
        # created_on = datetime.datetime.now()

        new_data = old_data
        new_data["start_appointment"] = start_appointment

        # print(start_appointment)

        raise Http404("test reschedule")

    def data_col_row(self, user_list: list, row: int):
        """Convert data list into two dimensional list.

        Args:
          user_list: list of user info
          row: number of rows per column

        Returns:
            two dimensional list
        """
        f_list = []
        temp_list: list = []

        for user in user_list:
            if len(temp_list) <= row:
                temp_list.append(user)
            else:
                f_list.append(temp_list)
                temp_list = []

        if len(temp_list) != 0:
            f_list.append(temp_list)
            temp_list = []

        return f_list

    def resched_timedelta(
        self,
        data: dict,
        start_appointment: datetime.datetime,
        decrypt_document_id: str,
        key_timedelta: list,
        operator: str,
        utc_offset: int,
    ):
        """Reschedule appointment with custom UTC offset.

        Args:
          data: data of user
          start_appointment: date of start appointment
          decrypt_document_id: decrypted document id
          key_timedelta: key from firebase data fields
          operator: specify add or subtract ("+" or "-")
          utc_offset: preferred UTC

        Returns:
            New data dictionary and change all of the value from key field
        """
        full_date = datetime.datetime.now()
        date = full_date.date()

        admin_settings = self.out_appointment_settings()
        admin_time_interval = admin_settings["time_interval"]
        data["start_appointment"] = start_appointment
        data["end_appointment"] = start_appointment + datetime.timedelta(
            minutes=admin_time_interval
        )
        data["created_on"] = datetime.datetime.now()
        data["document_id"] = decrypt_document_id

        timedelta_data = DateFormatter(full_date=full_date, date=date).dict_format_utcoffset(
            data=data, key_timedelta=key_timedelta, operator=operator, utc_offset=utc_offset
        )

        return timedelta_data
