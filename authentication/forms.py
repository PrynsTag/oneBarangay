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
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
                "pattern": r"^\S{8,}$",
                "onchange": "this.setCustomValidity(this.validity.patternMismatch ? "
                "'Must have at least 8 characters' : ''); "
                "if(this.checkValidity()) form.confirm_password.pattern = this.value;",
                "oninput": "password.setCustomValidity("
                "password.value !== confirm_password.value ? "
                "'Password is not the same with the confirm password.' : '')",
            }
        ),
    )

    def clean_password(self):
        """Clean password for minimum length."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")

        if len(password) < 8:
            raise forms.ValidationError("The minimum password length is 8 characters.")

        return cleaned_data


class AuthenticationForm(LockAccountForm, ForgotPasswordForm):
    """Login, Signup and Forgot Password Form."""

    confirm_password = forms.CharField(
        label="Confirm Password",
        label_suffix="",
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Re-type Password",
                "class": "form-control",
                "pattern": r"^\S{8,}$",
                "onchange": "this.setCustomValidity(this.validity.patternMismatch ? "
                "'Please enter the same Password as above' : '');",
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
