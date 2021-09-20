"""Appointment forms."""
from django import forms


class IdVerification(forms.Form):
    """ID Verification class."""

    first_name = forms.CharField(max_length=50)
    middle_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
