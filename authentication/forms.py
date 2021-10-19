"""Create your authentication forms here."""
from django import forms


class ForgotPasswordForm(forms.Form):
    """Forgot Password Form."""

    error_css_class = "is-invalid"
    required_css_class = "required"

    email = forms.EmailField(
        label="Your Email",
        label_suffix="",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "juan_delacruz@gmail.com",
                "class": "form-control",
                "autofocus": True,
            }
        ),
    )


class LockAccountForm(forms.Form):
    """Lock Account Form."""

    error_css_class = "invalid-feedback"
    required_css_class = "required"

    password = forms.CharField(
        label="Your Password",
        label_suffix="",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"},
        ),
    )


class AuthenticationForm(LockAccountForm, ForgotPasswordForm):
    """Login, Signup and Forgot Password Form."""

    confirm_password = forms.CharField(
        label="Confirm Password",
        label_suffix="",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Re-type Password",
                "class": "form-control",
            }
        ),
    )
    remember_me = forms.BooleanField(
        label="Remember Me",
        label_suffix="",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    terms_condition = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    def clean(self):
        """Customize cleaning for form fields."""
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if (password and confirm_password) and (password != confirm_password):
            raise forms.ValidationError("Password and Confirm Password do not match.")

        return cleaned_data
