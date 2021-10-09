"""Create your authentication views here."""
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from .forms import ForgotPasswordForm, LockAccountForm, LoginForm, SignUpForm


class LoginFormView(FormView):
    """Form view for login."""

    template_name = "authentication/sign_in.html"
    form_class = LoginForm
    success_url = "/barangay_admin/dashboard/"
    error_css_class = "invalid-feedback"
    required_css_class = "required"

    def form_valid(self, form):
        """Authenticate user when login form is valid.

        Args:
          form: The html login form submitted.

        Returns:
          None: Redirects to dashboard.
        """
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        authenticate(username=username, password=password)

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """Return login form with errors when login form is invalid.

        Args:
          form: The html login form submitted.

        Returns:
          Render form with errors.
        """
        messages.add_message(self.request, messages.ERROR, f"Invalid credentials.\n{form.errors}")
        return self.render_to_response(self.get_context_data(form=form))


class RegisterFormView(FormView):
    """Form view for register form."""

    template_name = "authentication/sign_up.html"
    form_class = SignUpForm
    success_url = "/register"
    error_css_class = "invalid-feedback"
    required_css_class = "required"

    def form_valid(self, form):
        """Create a user account from submitted register form when register form is valid.

        Args:
          form: The html register form submitted.

        Returns:
          None: Redirects to register form.
        """
        username = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password")
        authenticate(username=username, password=raw_password)

        msg = f"Account created - please <a href={self.success_url}>login</a>."
        messages.add_message(self.request, messages.SUCCESS, msg)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """Return register form with errors when register form is invalid.

        Args:
          form: The html register form submitted

        Returns:
          Redirects form with errors.
        """
        messages.add_message(self.request, messages.ERROR, f"Account not created.\n{form.errors}")
        return self.render_to_response(self.get_context_data(form=form))


class ForgotPasswordFormView(FormView):
    """Form view for forgot password form."""

    template_name = "authentication/forgot_password.html"
    form_class = ForgotPasswordForm
    success_url = "/login/"
    error_css_class = "invalid-feedback"
    required_css_class = "required"

    def form_valid(self, form):
        """Send a password reset email to a user when login form is valid.

        Args:
          form: The html forgot password form submitted.

        Returns:
          None: Redirects to login.
        """
        messages.add_message(self.request, messages.SUCCESS, "Password reset sent to email!")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """Return forgot password form with errors when login form is invalid.

        Args:
          form: The html forgot password form submitted

        Returns:
          Render form with errors.
        """
        messages.add_message(
            self.request, messages.ERROR, f"Password reset not sent!\n{form.errors}"
        )
        return self.render_to_response(self.get_context_data(form=form))


class LockAccountFormView(FormView):
    """Form view for lock account form."""

    template_name = "authentication/lock_account.html"
    form_class = LockAccountForm
    success_url = "/barangay-admin/dashboard/"
    error_css_class = "invalid-feedback"
    required_css_class = "required"

    def form_valid(self, form):
        """Authenticate locked user.

        Args:
          form: The html login form submitted

        Returns:
          None: Redirects to dashboard.
        """
        messages.add_message(self.request, messages.SUCCESS, "Login successful!")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """Return lock account form with errors.

        Args:
          form: The html login form submitted

        Returns:
          Render form with errors.
        """
        messages.add_message(
            self.request, messages.ERROR, f"Login not successful!\n{form.errors}"
        )
        return self.render_to_response(self.get_context_data(form=form))
