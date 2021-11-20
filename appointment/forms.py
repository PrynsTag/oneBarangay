"""Appointment forms."""
from django import forms
from django.forms import fields

from one_barangay.widgets import DatePickerWidget

document_list = [
    ("barangay-certificate", "Barangay Certificate"),
    ("barangay-clearance", "Barangay Clearance"),
    ("barangay-cedula", "Barangay Cedula"),
    ("barangay-local-employment", "Barangay Local Employment"),
    ("barangay-verification", "Barangay Verification"),
    ("certificate-of-indigency", "Certificate of Indigency"),
]


class AppointmentVerifyUser(forms.Form):
    """ID Verification class."""

    first_name = forms.CharField(max_length=50)
    middle_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)


class BarangayCertificate(forms.Form):
    """Class for Barangay Certificate."""

    date = fields.DateField(widget=forms.widgets.DateInput(attrs={"type": "date"}))
    fullname = forms.CharField(label="Fullname", max_length=100, min_length=2, required=True)
    address = forms.CharField(label="Address", max_length=200, required=True)
    year = forms.CharField(
        label="Enter year of residency", max_length=4, min_length=4, required=True
    )
    issued = forms.CharField(label="Issued for", required=True)
    conforme = forms.CharField(label="Conforme", required=True)
    ctc = forms.CharField(label="CTC No.", max_length=15, required=True)
    region = forms.CharField(label="Region", required=True)
    orno = forms.CharField(label="OR No.", required=True)
    amount = forms.DecimalField(label="Amount", decimal_places=2, required=True)
    valid = fields.DateField(widget=forms.widgets.DateInput(attrs={"type": "date"}))
    prepared = forms.CharField(label="Prepared by", required=True)


class BarangayClearance(forms.Form):
    """Class for Barangay Clearance."""

    date = fields.DateField(widget=forms.widgets.DateInput(attrs={"type": "date"}))
    fullname = forms.CharField(label="Fullname", max_length=100, min_length=2, required=True)
    address = forms.CharField(label="Address", max_length=200, required=True)
    year = forms.CharField(
        label="Enter year of residency", max_length=4, min_length=4, required=True
    )
    issued = forms.CharField(label="Issued for", required=True, initial="Clearance")
    conforme = forms.CharField(label="Conforme", required=True)
    ctc = forms.CharField(label="CTC No.", max_length=15, required=True)
    region = forms.CharField(label="Region", required=True)
    amount = forms.DecimalField(label="Amount", decimal_places=2, required=True)
    valid = fields.DateField(widget=forms.widgets.DateInput(attrs={"type": "date"}))
    prepared = forms.CharField(label="Prepared by", required=True)


class BarangayIndigency(forms.Form):
    """Class for Barangay Indigency."""

    date = fields.DateField(widget=forms.widgets.DateInput(attrs={"type": "date"}))
    fullname = forms.CharField(label="Fullname", max_length=100, min_length=2, required=True)
    address = forms.CharField(label="Address", max_length=200, required=True)
    year = forms.CharField(
        label="Enter year of residency", max_length=4, min_length=4, required=True
    )
    purpose = forms.CharField(label="Purpose", required=True)
    recipient = forms.CharField(label="Recipient", required=True)
    conforme = forms.CharField(label="Conforme", required=True)
    ctc = forms.CharField(label="CTC No.", max_length=15, required=True)
    region = forms.CharField(label="Region", required=True)
    valid = fields.DateField(widget=forms.widgets.DateInput(attrs={"type": "date"}))
    prepared = forms.CharField(label="Prepared by", required=True)


class BarangayLocalEmployment(forms.Form):
    """Class for Barangay Local Employment."""

    date = fields.DateField(widget=forms.widgets.DateInput(attrs={"type": "date"}))
    fullname = forms.CharField(label="Fullname", max_length=100, min_length=2, required=True)
    address = forms.CharField(label="Address", max_length=200, required=True)
    year = forms.CharField(
        label="Enter year of residency", max_length=4, min_length=4, required=True
    )
    conforme = forms.CharField(label="Conforme", required=True)
    ctc = forms.CharField(label="CTC No.", max_length=15, required=True)
    region = forms.CharField(label="Region", required=True)
    orno = forms.CharField(label="OR No.", required=True)
    amount = forms.DecimalField(label="Amount", decimal_places=2, required=True)
    valid = fields.DateField(widget=forms.widgets.DateInput(attrs={"type": "date"}))
    prepared = forms.CharField(label="Prepared by", required=True)


class BarangayVerification(forms.Form):
    """Class for Barangay Local Employment."""

    date = fields.DateField(widget=forms.widgets.DateInput(attrs={"type": "date"}))
    fullname = forms.CharField(label="Fullname", max_length=100, min_length=2, required=True)
    address = forms.CharField(label="Address", max_length=200, required=True)
    year = forms.CharField(
        label="Enter year of residency", max_length=4, min_length=4, required=True
    )
    conforme = forms.CharField(label="Conforme", required=True)
    ctc = forms.CharField(label="CTC No.", max_length=15, required=True)
    region = forms.CharField(label="Region", required=True)
    orno = forms.CharField(label="OR No.", required=True)
    amount = forms.DecimalField(label="Amount", decimal_places=2, required=True)
    valid = fields.DateField(widget=forms.widgets.DateInput(attrs={"type": "date"}))
    prepared = forms.CharField(label="Prepared by", required=True)
