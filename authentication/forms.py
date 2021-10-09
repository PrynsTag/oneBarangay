"""Create your authentication forms here."""
from django import forms


class LoginForm(forms.Form):
    """Login Form."""

    email = forms.CharField(
        label="Your Email",
        label_suffix="",
        widget=forms.TextInput(attrs={"placeholder": "Email", "class": "form-control"}),
    )
    password = forms.CharField(
        label="Your Password",
        label_suffix="",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
            },
        ),
    )
    remember_me = forms.BooleanField(
        label="Remember Me",
        label_suffix="",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )


class SignUpForm(forms.Form):
    """Signup Form."""

    email = forms.EmailField(
        label="Your Email",
        label_suffix="",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control required",
            }
        ),
    )
    password = forms.CharField(
        label="Your Password",
        label_suffix="",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"},
        ),
    )
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
    terms_condition = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )


class ForgotPasswordForm(forms.Form):
    """Forgot Password Form."""

    email = forms.EmailField(
        label="Your Email",
        label_suffix="",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "juan_delacruz@gmail.com",
                "class": "form-control required",
                "autofocus": True,
            }
        ),
    )


class LockAccountForm(forms.Form):
    """Lock Account Form."""

    password = forms.CharField(
        label="Your Password",
        label_suffix="",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"},
        ),
    )
