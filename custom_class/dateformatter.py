"""Custom class date formatter."""
import datetime
import time


class DateFormatter:
    """Split full date into date, time, and date & time."""

    def __init__(
        self,
        full_date: datetime.datetime = datetime.datetime.now(),
        date: datetime.datetime = datetime.date.today(),
        separator: str = " ",
    ):
        """Initialize date formatter with full_date and separator."""
        self.full_date = full_date
        self.date = date
        self.separator = separator

    def date_splitter(self):
        date_split = (str(self.full_date).split(" "))[0].split("-")
        year = int(date_split[0])
        month = int(date_split[1])
        day = int(date_split[2])

        return datetime.date(year=year, month=month, day=day)
