"""Routing Request to Views of OCR Pages."""
from django.core.files.base import ContentFile
from django.shortcuts import render

from ocr.models import File

def ocr_files(request):
    """Fetch OCR HTML Pages.

    Args:
      request: The URL Request.

    Returns:
      Renders ocr_files.html.

    """
    return render(
        request=request,
        template_name="ocr/ocr_files.html",
    )


def scan_file(request):
    """Fetch the uploaded files for scanning.

    Args:
      request: The URL Request.

    Returns:
      The scan_file.html page requested in the URL.

    """
    return render(
        request=request,
        template_name="ocr/scan_result.html",
    )
