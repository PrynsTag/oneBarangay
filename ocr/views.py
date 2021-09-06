"""Routing Request to Views of OCR Pages."""
from django.core.files.base import ContentFile
from django.shortcuts import render

from ocr.models import File

from .forms import FileFieldForm


def file_upload(request):
    """Handle file uploads.

    Args:
      request: The URL Request.

    Returns:
      On Success: Renders ocr_files to output uploaded files.
      On File: Renders file_upload again to display validation errors
    """
    if request.method == "POST":
        form = FileFieldForm(request.POST, request.FILES)
        files = request.FILES.getlist("file_field")
        if form.is_valid():
            for file in files:
                upload = File()
                for chunks in file.chunks():
                    upload.file_field.save(file.name, ContentFile(chunks))
            return render(
                request,
                "ocr/ocr_files.html",
                {"files": files},
            )
        else:
            form = FileFieldForm()
            return render(
                request=request,
                template_name="ocr/file_upload.html",
                context={"form": form},
            )
    else:
        form = FileFieldForm()
        return render(
            request=request,
            template_name="ocr/file_upload.html",
            context={"form": form},
        )


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
