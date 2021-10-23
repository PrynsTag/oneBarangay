"""Create your bulk_sched forms here."""
from django import forms


class BulkSchedCreateForm(forms.Form):
    """Form for bulk_sched."""

    error_css_class = "is-invalid"
    required_css_class = "required"

    EVENT_CHOICES = (
        ("rbi", "RBI Collection"),
        ("covid vaccine", "COVID Vaccine"),
        ("circumcision", "Circumcision"),
        ("basketball", "Basketball Competition"),
    )
    NOTIFICATION_CHOICES = (
        ("app", "App"),
        ("email", "Email"),
        ("text", "Text"),
    )
    RELATIONSHIP_CHOICES = (
        ("head of family", "Head of Family"),
        ("father", "Father"),
        ("mother", "Mother"),
        ("son", "Son"),
        ("daughter", "Daughter"),
    )
    STREET_CHOICES = (
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
    resident_quantity = forms.IntegerField(
        label_suffix="",
        min_value=0,
        widget=forms.NumberInput(attrs={"class": "form-control rounded-end"}),
    )
    relationship_type = forms.ChoiceField(
        label_suffix="",
        widget=forms.Select(attrs={"class": "form-select", "aria-label": "Relationship Select"}),
        choices=RELATIONSHIP_CHOICES,
    )
    street = forms.ChoiceField(
        label_suffix="",
        widget=forms.Select(attrs={"class": "form-select", "aria-label": "Street Select"}),
        choices=STREET_CHOICES,
    )
    time_interval = forms.IntegerField(
        label_suffix="",
        min_value=0,
        widget=forms.NumberInput(attrs={"class": "form-control rounded-end"}),
    )
    notification_type = forms.MultipleChoiceField(
        label_suffix="",
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-checkbox"}),
        choices=NOTIFICATION_CHOICES,
    )
    start_date = forms.DateTimeField(
        label_suffix="",
        label="Start Date",
        widget=forms.DateTimeInput(
            attrs={"class": "form-control rounded-end", "autocomplete": "off"}
        ),
    )
    end_date = forms.DateTimeField(
        label_suffix="",
        label="End Date",
        widget=forms.DateTimeInput(
            attrs={"class": "form-control rounded-end rounded-end", "autocomplete": "off"}
        ),
    )
