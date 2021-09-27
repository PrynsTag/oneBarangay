"""Routing Request to Views of OCR Pages."""
import asyncio
import json
import logging

from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from dotenv import load_dotenv

from ocr.form_recognizer import form_recognizer_runner
from ocr.forms import UploadForm
from ocr.scripts import Script

load_dotenv()

logger = logging.getLogger(__name__)


class FileUploadView(FormView):
    """View for file upload."""

    form_class = UploadForm
    template_name = "ocr/file_upload.html"
    success_url = "ocr/ocr_files.html"

    def __init__(self):
        """Initialize FileUploadView class variables."""
        self.script = Script()

    def post(self, request, *args, **kwargs):
        """Post request from file upload.

        Args:
          request: The URL request.
          *args: Additional arguments.
          **kwargs: Additional keyword arguments.

        Returns:
          on success: The ocr_files along with context.
          on fail: The file_upload.html along with context.
        """
        files = [request.FILES[file] for file in request.FILES]
        # TODO: Get thumbnail data from dropzone
        # TODO: Pass the thumbnail data to session
        dict_files = [json.loads(file) for file in request.POST.getlist("fileData")]

        request.session["files"] = self.script.format_dictionary_file(dict_files)

        for file in files:
            default_storage.save(file.name, file)

        return HttpResponse(request.session["files"])


class ScanFileView(FormView):
    """View for file upload."""

    template_name = "ocr/file_upload.html"

    def post(self, request, *args, **kwargs):
        """Get context data and run form recognizer.

        Args:
          request: The URL Request.
          **kwargs: Additional keyword argument (Filename).
          *args: Additional Arguments

        Returns:
          : scan_result.html with context of detected text from table image.
        """
        return render(request, self.template_name)


class OCRFilesView(TemplateView):
    """Display ocr_files template."""

    template_name = "ocr/ocr_files.html"

    def get_context_data(self, **kwargs):
        """Get context data of ocr_files.

        Args:
          **kwargs: Keyword arguments.

        Returns:
          : files as context data.
        """
        return {"files": self.request.session["files"]}


class ScanResultView(TemplateView):
    """View for scan_result.html."""

    template_name = "ocr/scan_result.html"

    def get_context_data(self, **kwargs):
        """Get context data and run form recognizer.

        Args:
          **kwargs: Additional keyword argument (Filename).

        Returns:
          scan_result.html with context of detected text from table image.
        """
        ocr = asyncio.run(form_recognizer_runner(kwargs["filename"]))
        return {"ocr_header": ocr[0], "ocr_text": ocr[1]}
