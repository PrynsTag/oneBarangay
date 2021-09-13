class Date_Formatter:
    """Split full date into date, time, and date & time."""

    def __init__(self, full_date: str, separator: str):
        self.full_date = full_date
        self.formatted_full_date = "_".join(full_date)
        date_split = full_date.split(sep=separator)
        self.formatted_date = "_".join(date_split[:-1])
        self.formatted_time = date_split[-1:][0]
        self.formatted_date_time = f"{'_'.join(date_split[:-1])}_{date_split[-1:][0]}"

    def __str__(self):
        return f"Unformatted date: {self.full_date} Formatted date: {self.formatted_date} Formatted Time: {self.formatted_time}"
