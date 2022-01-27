"""Create your bulk_sched forms here."""
import datetime

from dateutil.relativedelta import relativedelta
from django import forms
from django.templatetags.static import static


class BulkSchedCreateForm(forms.Form):
    """Form for bulk_sched."""

    error_css_class = "is-invalid"
    required_css_class = "required"

    EVENT_CHOICES = (
        (None, "--- Select Event ---"),
        ("rbi", "RBI Collection"),
        ("covid vaccine", "COVID Vaccine"),
        ("circumcision", "Circumcision"),
        ("basketball", "Basketball Competition"),
    )
    NOTIFICATION_CHOICES = (
        ("Mobile", "Mobile"),
        ("Email", "Email"),
        ("Web", "Web"),
        # ("text", "Text"),
    )
    RELATIONSHIP_CHOICES = (
        (None, "--- Select Role ---"),
        ("Father", "Father"),
        ("Mother", "Mother"),
        ("Son", "Son"),
        ("Daughter", "Daughter"),
    )
    STREET_CHOICES = (
        (None, "--- Select Street ---"),
        ("", "All"),
        ("A. Duque", "A. Duque"),
        ("Aca Road", "Aca Road"),
        ("Bangcal Extension", "Bangcal Extension"),
        ("Bartolome Street", "Bartolome Street"),
        ("C. Molina Street", "C. Molina Street"),
        ("Central Road", "Central Road"),
        ("Cherry Blossom Street", "Cherry Blossom Street"),
        ("Dr. Bartolome", "Dr. Bartolome"),
        ("East Road", "East Road"),
        ("F. San Diego Street", "F. San Diego Street"),
        ("I. Fernando", "I. Fernando"),
        ("I. Lozada Street", "I. Lozada Street"),
        ("Jollibee Drive-Through", "Jollibee Drive-Through"),
        ("M.H. del Pilar Footbridge (footway)", "M.H. del Pilar Footbridge (footway)"),
        ("Main Road", "Main Road"),
        ("North Road", "North Road"),
        ("Orange Street", "Orange Street"),
        ("P. Adriano", "P. Adriano"),
        ("Peach Street", "Peach Street"),
        ("Road 1", "Road 1"),
        ("Roseville Street", "Roseville Street"),
        ("South RoadSt. Elsewhere Street", "South RoadSt. Elsewhere Street"),
        ("T. Santiago Street", "T. Santiago Street"),
        ("West Road", "West Road"),
    )

    event = forms.ChoiceField(
        label_suffix="",
        widget=forms.Select(attrs={"class": "form-select", "aria-label": "Event Select"}),
        choices=EVENT_CHOICES,
    )
    # resident_quantity = forms.IntegerField(
    #     label_suffix="",
    #     min_value=0,
    #     widget=forms.NumberInput(attrs={"class": "form-control rounded-end"}),
    # )
    # relationship_type = forms.ChoiceField(
    #     label_suffix="",
    #     label="Family Role",
    #     widget=forms.Select(attrs={"class": "form-select",
    #     "aria-label": "Relationship Select"}),
    #     choices=RELATIONSHIP_CHOICES,
    # )
    # street = forms.ChoiceField(
    #     label_suffix="",
    #     widget=forms.Select(attrs={"class": "form-select", "aria-label": "Street Select"}),
    #     choices=STREET_CHOICES,
    # )
    # time_interval = forms.IntegerField(
    #     label_suffix="",
    #     min_value=0,
    #     widget=forms.NumberInput(attrs={"class": "form-control rounded-end"}),
    # )
    notification_type = forms.MultipleChoiceField(
        label_suffix="",
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-checkbox"}),
        choices=NOTIFICATION_CHOICES,
    )
    start_date = forms.DateTimeField(
        label_suffix="",
        label="Start Date",
        widget=forms.DateTimeInput(attrs={"class": "form-control rounded-end", "autocomplete": "off"}),
    )
    end_date = forms.DateTimeField(
        label_suffix="",
        label="End Date",
        widget=forms.DateTimeInput(attrs={"class": "form-control rounded-end rounded-end", "autocomplete": "off"}),
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    event_message = forms.CharField(
        label_suffix="",
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )


class DatePickerWidget(forms.DateInput):
    """Widget for xdsoft datepicker."""

    class Media:
        """Media files for DatePicker widget."""

        css = {"all": (static("/assets/vendor/xdsoft-datepicker/dist/xdsoft-datepicker.min.css"),)}
        js = (
            static("/assets/vendor/jquery/dist/jquery.min.js"),
            static("/assets/vendor/xdsoft-datepicker/dist/xdsoft-datepicker.min.js"),
        )


class BarangayCertificate(forms.Form):
    """Class for Barangay Certificate."""

    document_validity = datetime.date.today() + relativedelta(months=+3)

    date = forms.DateField(
        label="Date",
        widget=DatePickerWidget(attrs={"class": "form-control", "autocomplete": "off"}),
    )
    full_name = forms.CharField(
        label="Fullname",
        max_length=100,
        min_length=2,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    address = forms.CharField(
        label="Address",
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    year = forms.CharField(
        label="Enter year of residency",
        max_length=4,
        min_length=4,
        widget=DatePickerWidget(attrs={"class": "form-control", "autocomplete": "off"}),
    )
    issued_for = forms.CharField(
        label="Issued for",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    conforme = forms.CharField(
        label="Conforme",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    ctc_no = forms.CharField(
        label="CTC No.",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    region = forms.CharField(
        label="Region",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    or_no = forms.CharField(
        label="OR No.",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    amount = forms.DecimalField(
        label="Amount",
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    valid_until = forms.DateField(
        label="Valid Until",
        widget=DatePickerWidget(attrs={"class": "form-control", "autocomplete": "off"}),
    )
    prepared_by = forms.CharField(
        label="Prepared by",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
