"""Appointment forms."""
from django import forms
from django.forms import fields


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
