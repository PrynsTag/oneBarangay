"""Routing Request to Views of OCR Pages."""
import asyncio

from django.core.files.storage import default_storage
from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from dotenv import load_dotenv

from ocr.form_recognizer import form_recognizer_runner
from ocr.forms import UploadForm

load_dotenv()


class FileUploadView(FormView):
    """View for file upload."""

    form_class = UploadForm
    template_name = "ocr/file_upload.html"
    success_url = "ocr/ocr_files.html"

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
        form = UploadForm(request.POST, request.FILES)
        files = request.FILES.getlist("upload_file")

        if form.is_valid():
            for file in files:
                default_storage.save(file.name, file)

            return render(
                request,
                "ocr/ocr_files.html",
                {"files": files},
            )
        else:
            form = UploadForm()

            return render(
                request=request,
                template_name="ocr/file_upload.html",
                context={"form": form},
            )


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
