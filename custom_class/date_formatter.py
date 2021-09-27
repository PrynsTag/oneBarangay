"""Custom class date_formatter."""


class Date_Formatter:
    """Split full date into date, time, and date & time."""

    def __init__(self, full_date: str, separator: str):
        """Date formatter initialization."""
        self.full_date = full_date
        self.formatted_full_date = "_".join(full_date)
        date_split = full_date.split(sep=separator)
        self.formatted_date = "_".join(date_split[:-1])
        self.formatted_time = date_split[-1:][0]
        self.formatted_date_time = f"{'_'.join(date_split[:-1])}_{date_split[-1:][0]}"

    def __str__(self):
        """Date formatter output values."""
        full_date = self.full_date
        formatted_date = self.formatted_date
        formatted_time = self.formatted_time
        return (
            f"Unformatted date: {full_date} Formatted date: "
            f"{formatted_date} Formatted Time: {formatted_time}"
        )
