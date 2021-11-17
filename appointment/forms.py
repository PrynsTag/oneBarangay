"""Appointment forms."""
import datetime

from django import forms


class AppointmentVerifyUser(forms.Form):
    """ID Verification class."""

    first_name = forms.CharField(max_length=50)
    middle_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)


class BarangayCertificate(forms.Form):
    """Class for Barangay Certificate."""

    date = forms.DateField(label="Date", initial=datetime.date.today())
    full_name = forms.CharField(label="Fullname", max_length=100, min_length=2, required=True)
    address = forms.CharField(label="Address", max_length=200, required=True)
    year = forms.CharField(
        label="Enter year of residency", max_length=4, min_length=4, required=True
    )
    issued_for = forms.CharField(label="Issued for", required=True)
    conforme = forms.CharField(label="Conforme", required=True)
    ctc_no = forms.CharField(label="CTC No.", required=True)
    region = forms.CharField(label="Region", required=True)
    or_no = forms.CharField(label="OR No.", required=True)
    amount = forms.DecimalField(label="Amount", decimal_places=2, required=True)
    valid_until = forms.DateField(label="Valid Until", required=True)
    prepared_by = forms.CharField(label="Prepared by", required=True)
