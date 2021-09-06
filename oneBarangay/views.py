"""Create your views here."""
from django.shortcuts import render


def handler403(request, exception=None):
    """Override default handler for a custom style 403 error.

    Args:
      request: The URL request.
      exception:  (Default value = None) The error thrown.

    Returns:
      The custom error page for 403 errors.
    """
    response = render(request, template_name="403.html")
    response.status_code = 403
    return response


def handler404(request, exception=None):
    """Override default handler for a custom style 404 error.

    Args:
      request: The URL request.
      exception:  (Default value = None) The error thrown.

    Returns:
      The custom error page for 403 errors.
    """
    response = render(request, template_name="404.html")
    response.status_code = 404
    return response


def handler500(request, exception=None):
    """Override default handler for a custom style 500 error.

    Args:
      request: The URL request.
      exception:  (Default value = None) The error thrown.

    Returns:
      The custom error page for 403 errors.
    """
    response = render(request, template_name="500.html")
    response.status_code = 500
    return response
