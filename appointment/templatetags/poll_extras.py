"""Appointment poll_extras."""
import base64
import datetime

from django import template

register = template.Library()


@register.filter("base64_encode")
def base64_encode(value):
    """Convert text to base64.

    Args:
      value: Any string or texts

    Returns:
      base64 string
    """
    value_bytes = value.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(value_bytes)
    base64_message = base64_bytes.decode("ascii")
    return str(base64_message)


@register.filter("date_formatter")
def date_formatter(value):
    """Format underscored date to MM DD, YYYY.

    Args:
      value: Input date with underscore YYYY_MM_DD ("2021_09_08")

    Returns:
      Standard date ("April 18, 2021")
    """
    split_date = value.split("_")
    date = datetime.datetime(int(split_date[0]), int(split_date[1]), int(split_date[2]))

    return date.strftime("%B %d, %Y")


@register.filter("military_to_standard_time")
def military_to_standard_time(value):
    """Convert military time to standard time.

    Args:
      value: str: Input military time (ex. "0100", "0200", "0300")

    Returns:
      standard time ("07:00 am")
    """
    hour_mod = int(value[:-2]) % 12
    hour_two_dig = int(value[:-2])

    if hour_two_dig % 12 == 0 and hour_two_dig == 0:
        return "12:00 am"
    elif hour_two_dig % 12 == 0 and hour_two_dig == 12:
        return "12:00 pm"
    elif hour_two_dig < 12:
        return f"0{hour_mod}:00 am" if hour_mod < 10 else f"{hour_mod}:00 am"
    elif hour_two_dig > 12:
        return f"0{hour_mod}:00 pm" if hour_mod < 10 else f"{hour_mod}:00 pm"
    else:
        return "Invalid Time"


@register.filter("firebase_timestamp_format")
def firebase_timestamp_format(value, utc_offset: int = 0):
    """Convert firebase firestore timestamp format into python.

    Args:
      value: firebase date and time format
      utc_offset: int:  (Default value = 0)
      utc_offset: int:  (Default value = 0)

    Returns:
      python format timestamp
    """
    value_str = str(value)
    full_datetime_stripe = datetime.datetime.strptime(value_str, "%Y-%m-%d %H:%M:%S%z")

    result_utc = full_datetime_stripe + datetime.timedelta(hours=utc_offset)

    return datetime_to_time(result_utc)


@register.filter("firebase_datetime_format")
def firebase_datetime_format(value, utc_offset: int = 0):
    """Convert firebase firestore timestamp format into python.

    Args:
      value: firebase date and time format
      utc_offset: int:  (Default value = 0)
      utc_offset: int:  (Default value = 0)

    Returns:
      python format timestamp
    """
    value_str = str(value)
    full_datetime_stripe = datetime.datetime.strptime(value_str, "%Y-%m-%d %H:%M:%S%z")

    result_utc = full_datetime_stripe + datetime.timedelta(hours=utc_offset)

    return datetime.datetime.strftime(result_utc, "%B %d, %Y")


@register.filter("datetime_to_time")
def datetime_to_time(value):
    """Get time from date and time format.

    Args:
      value: datetime type

    Returns:
        time
    """
    return value.strftime("%I:%M %p")


@register.filter("count_list")
def count_list(value):
    """Count number of list.

    Args:
      value: collection list

    Returns:
        Number of data from the list
    """
    return len(value)


@register.filter("text_slugify")
def text_slugify(value):
    """Convert text to slugify.

    Args:
      value: text

    Returns:
        Text in slugify format
    """
    return slugify(value)


@register.filter("nano_to_date")
def nano_to_date(value):
    """Convert nano to date.

    Args:
      value: Firebase Nanosecond

    Returns:
        Date format
    """
    nano_to_datetime = datetime.datetime(
        year=value.year,
        month=value.month,
        day=value.day,
        hour=value.hour,
        minute=value.minute,
        second=value.second,
    )
    nano_timedelta = nano_to_datetime + datetime.timedelta(hours=8)
    return nano_timedelta.date()


@register.filter("date_to_str")
def date_to_str(value):
    """Convert date into string.

    Args:
      value: date

    Returns:
        String format of date
    """
    date_convert_str = nano_to_date(value).__str__()
    return date_convert_str


@register.filter("join_dict")
def join_dict(value, key):
    """Join text in dictionary collection.

    Args:
      value: data in dictionary collection
      key: key value in data collection

    Returns:
        Joined string format documents
    """
    temp_list = []

    for data in value:
        temp_list.append(data[key])

    return ", ".join(temp_list)
