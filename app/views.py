"""Create your App views here."""
from django.shortcuts import render


def index(request):
    """Display home page.

    Args:
      request: The URL Request.

    Returns:
      render home page.
    """
    return render(request, "app/index.html")


def government(request):
    """Display about pages.

    Args:
      request: URL request

    Returns:
        render about page.
    """
    return render(request, "app/government.html")


def work(request):
    """Display about page.

    Args:
      request: URL request

    Returns:
        render about page.
    """
    return render(request, "app/work.html")


def pricing(request):
    """Display pricing page.

    Args:
      request: URL request

    Returns:
        render pricing page.
    """
    return render(request, "app/pricing.html")


def contact(request):
    """Display contact page.

    Args:
      request: URL request

    Returns:
        render contact page.
    """
    return render(request, "app/contact.html")
