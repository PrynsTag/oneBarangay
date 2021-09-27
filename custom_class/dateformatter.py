"""Custom class date formatter."""
import datetime
import math


class DateFormatter:
    """Split full date into date, time, and date & time."""

    def __init__(
        self,
        full_date: datetime.datetime = datetime.datetime.now(),
        date: datetime.datetime = datetime.date.today(),
        datetime_str: str = "",
        document_str="",
        separator: str = " ",
    ):
        """Initialize date formatter with full_date and separator."""
        self.full_date = full_date
        self.date = date
        self.separator = separator
        self.datetime_str = datetime_str
        self.document_str = document_str

    def date_splitter(self):
        """Split full date and time into date."""
        date_split = (str(self.full_date).split(" "))[0].split("-")
        year = int(date_split[0])
        month = int(date_split[1])
        day = int(date_split[2])

        return datetime.date(year=year, month=month, day=day)

    # 2021-09-18 23:00:00+00:00
    def datetime_splitter(self, utc_offset: int = 0):
        """Full date and time splitter with custom UTC.

        Args:
          utc_offset: int:  (Default value = 0)

        Returns:
            : date and time with added custom UTC
        """
        datetime_split = str(self.full_date).split(" ")
        date_split = datetime_split[0].split("-")
        year = date_split[0]
        month = date_split[1]
        day = date_split[2]
        time_split = datetime_split[1].split("+")[0].split(":")
        hour = time_split[0]
        minute = time_split[1]
        second = time_split[2]

        strp_datetime = datetime.datetime.strptime(
            f"{year}-{month}-{day} {hour}:{minute}:{second}", "%Y-%m-%d %H:%M:%S"
        )

        result_utc = strp_datetime + datetime.timedelta(hours=utc_offset)

        return result_utc

    def document_splitter(self):
        """Document ID split."""
        split_document_id = self.document_str.split("-")
        get_date = split_document_id[0]
        get_time = split_document_id[1]
        year = int(get_date[:4])
        month = int(get_date[4:6])
        day = int(get_date[6:8])
        time_int = int(get_time)

        return get_date, get_time, year, month, day, time_int

    def datetime_createdOn(self, utc_offset: int = 0):
        """Format date and time from created_on.

        Args:
          utc_offset: int:  (Default value = 0)

        Returns:
            : formatted date and time with added custom UTC
        """
        datetime_split = str(self.datetime_str).split(" ")
        date_split = datetime_split[0].split("-")
        year = date_split[0]
        month = date_split[1]
        day = date_split[2]
        time_split = datetime_split[1].split("+")[0].split(":")
        hour = time_split[0]
        minute = time_split[1]
        second = str(int(time_split[2].split(".")[0]))

        strp_datetime = datetime.datetime.strptime(
            f"{year}-{month}-{day} {hour}:{minute}:{second}", "%Y-%m-%d %H:%M:%S"
        )

        result_utc = strp_datetime + datetime.timedelta(hours=utc_offset)

        return result_utc

    def date_fb_convert(self):
        """Convert firebase DatetimeWithNanoseconds into python format date and time."""
        if isinstance(self.full_date, datetime.datetime):
            return self.full_date.__str__()

    def date_fb_convert_formatIt(self, date: datetime.datetime):
        """Convert firebase DatetimeWithNanoseconds into python format date and time.

        Args:
          date: datetime.datetime: firebase date and time format (DatetimeWithNanoseconds)

        Returns:
            Converted date and time into string
        """
        if isinstance(self.full_date, datetime.datetime):
            return self.full_date.__str__()

    def firebaseTime_formatIt(self, utc_offset: int = 0):
        """Convert firebase timestamp DatetimewithNanoseconds into python format date and time.

        Args:
          utc_offset: custom UTC

        Returns:
            : python format date and time with custom UTC
        """
        appointment_converted = self.date_fb_convert()
        appointment_offset = self.firebase_utcOffset(
            date=appointment_converted, utc_offset=utc_offset
        )

        return appointment_offset

    def firebase_utcOffset(self, date: str, utc_offset: int = 0):
        """Convert string and add UTC.

        Args:
          date: str:
          utc_offset: int:  (Default value = 0)

        Returns:
            : Full date and time with added custom UTC
        """
        datetime_split = date.split(" ")
        date_split = datetime_split[0].split("-")
        year = date_split[0]
        month = date_split[1]
        day = date_split[2]
        time_split = datetime_split[1].split("+")[0].split(":")
        hour = time_split[0]
        minute = time_split[1]
        second = str(int(math.floor(float(time_split[2]))))

        strp_datetime = datetime.datetime.strptime(
            f"{year}-{month}-{day} {hour}:{minute}:{second}", "%Y-%m-%d %H:%M:%S"
        )

        result_utc = strp_datetime + datetime.timedelta(hours=utc_offset)

        return result_utc

    def datetime_firestore_utc(
        self, query_key: list, data_dict: dict, utc_offset: int = 0
    ):
        """Convert firebase firestore DatetimeWithNanoseconds into python format.

        Args:
          query_key: list: list of firebase keys
          data_dict: dict: data from firebase firestore
          utc_offset: int:  (Default value = 0)

        Returns:
            appointment details with python date and time format.
        """
        for key in query_key:
            start_data = data_dict[key]
            year, month, day, hour, minute, second = (
                start_data.year,
                start_data.month,
                start_data.day,
                start_data.hour,
                start_data.minute,
                start_data.second,
            )
            full_date = (
                datetime.datetime(
                    year=year,
                    month=month,
                    day=day,
                    hour=hour,
                    minute=minute,
                    second=second,
                )
            ) + datetime.timedelta(hours=utc_offset)
            data_dict[key] = full_date

        return data_dict

    def datetime_timedelta_hours(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
        utc_offset: int,
        operator: str,
    ):
        """Date and time with custom timezone.

        Args:
          year: int: year of appointment
          month: int: month of appointment
          day: int: day of appointment
          hour: int: hour of appointment
          minute: int: minute of appointment
          second: int: second of appointment
          utc_offset: int: specify utc
          operator: str: (+ or -) date add/subtract using timedelta

        Returns:
            datetime with custom timezone
        """
        set_datetime = datetime.datetime(
            year=year, month=month, day=day, hour=hour, minute=minute, second=second
        )

        if operator == "+":
            add_utc = set_datetime + datetime.timedelta(hours=utc_offset)
            return add_utc
        elif operator == "-":
            minus_utc = set_datetime - datetime.timedelta(hours=utc_offset)
            return minus_utc
        else:
            raise Http404("Invalid Operator")
