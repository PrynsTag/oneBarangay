"""Create your forms here."""
from django import forms
from django.core.validators import RegexValidator


class UserManagementCreateForm(forms.Form):
    """Create user form."""

    error_css_class = "is-invalid"
    required_css_class = "required"

    user_id = forms.CharField(
        required=False,
        label="User I.D.",
        label_suffix="",
        widget=forms.HiddenInput(),
    )

    email = forms.EmailField(
        label="User Email",
        label_suffix="",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control text-black",
            }
        ),
    )

    display_name = forms.CharField(
        required=False,
        label="Display Name",
        label_suffix="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Juan Dela Cruz",
                "class": "form-control text-black",
            }
        ),
    )

    role = forms.ChoiceField(
        label="User Role",
        label_suffix="",
        choices=[
            ("resident", "Resident"),
            ("admin", "Barangay Admin"),
            ("secretary", "Barangay Secretary"),
            ("worker", "Barangay Worker"),
        ],
        widget=forms.Select(
            attrs={"class": "form-select text-black", "aria-label": "User Role Select"}
        ),
    )

    disabled = forms.ChoiceField(
        label="Account Status",
        label_suffix="",
        choices=[
            (False, "Enable"),
            (True, "Disable"),
        ],
        widget=forms.Select(
            attrs={"class": "form-select text-black", "aria-label": "User Status Select"}
        ),
    )

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: \
        '+999999999'. Up to 15 digits allowed.",
    )
    contact_number = forms.CharField(
        validators=[phone_regex],
        required=False,
        label="Phone Number",
        label_suffix="",
        max_length=17,
        widget=forms.TextInput(
            attrs={
                "placeholder": "+631234567891",
                "class": "form-control text-black",
                "type": "tel",
                "pattern": r"^\+?1?\d{9,15}$",
            }
        ),
    )

    # photo_url = forms.ImageField(
    #     required=False,
    #     label="Profile Picture",
    #     label_suffix="",
    #     widget=forms.FileInput(attrs={"class": "form-control"}),
    # )
