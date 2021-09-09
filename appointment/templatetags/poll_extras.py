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

    Returns: base64 string
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

    Returns: Standard date ("April 18, 2021")
    """
    split_date = value.split("_")
    date = datetime.datetime(int(split_date[0]), int(split_date[1]), int(split_date[2]))

    return date.strftime("%B %d, %Y")


@register.filter("military_to_standard_time")
def military_to_standard_time(value):
    """Convert military time to standard time.

    Args:
      value: str: Input military time (ex. "0100", "0200", "0300")

    Returns: standard time ("07:00 am")
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
        print("Invalid time please try again")
        return "Invalid Time"
