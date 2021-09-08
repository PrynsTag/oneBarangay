"""Routing Request to Views of OCR Pages."""
import json
import os
import re

from django.shortcuts import render
from django.views.generic import FormView, ListView, TemplateView
from dotenv import load_dotenv
from google.cloud import storage, vision

from ocr.forms import UploadForm
from ocr.models import Upload

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
            for _ in files:
                form.save()

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


class ScanFileView(ListView):
    """View for ocr_files.html."""

    model = Upload
    template_name = "ocr/ocr_files.html"
    context_object_name = "files"


class ScanResultView(TemplateView):
    """View for scan_result.html."""

    template_name = "ocr/scan_result.html"

    def get_context_data(self, **kwargs):
        """Get context data.

        Args:
          **kwargs: Additional keyword argument.

        Returns:
          scan_result.html with context of detected text from image.
        """
        gsc_source_uri = (
            "gs://"
            + os.getenv("GS_MEDIA_BUCKET_NAME")
            + "/documents/"
            + kwargs["filename"]
        )
        gcs_destination_uri = (
            "gs://" + "scan_result" + "/documents/" + kwargs["filename"]
        )
        return {"ocr_text": async_detect_document(gsc_source_uri, gcs_destination_uri)}


def async_detect_document(gcs_source_uri, gcs_destination_uri):
    """OCR with PDF/TIFF as source files on GCS.

    Args:
      gcs_source_uri: Source URI of image.
      gcs_destination_uri: Destination URI of the scanned result.

    Returns:
      The detected text from image.
    """
    # Supported mime_types are: 'application/pdf' and 'image/tiff'
    mime_type = "image/tiff"

    # How many pages should be grouped into each json output file.
    batch_size = 2

    client = vision.ImageAnnotatorClient()

    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

    gcs_source = vision.GcsSource(uri=gcs_source_uri)
    input_config = vision.InputConfig(gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size
    )

    async_request = vision.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config, output_config=output_config
    )

    operation = client.async_batch_annotate_files(requests=[async_request])

    print("Waiting for the operation to finish.")
    operation.result(timeout=420)

    # Once the request has completed and the output has been
    # written to GCS, we can list all the output files.
    storage_client = storage.Client()

    match = re.match(r"gs://([^/]+)/(.+)", gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name)

    # List objects with the given prefix.
    blob_list = list(bucket.list_blobs(prefix=prefix))
    print("Output files:")
    for blob in blob_list:
        print(blob.name)

    # Process the first output file from GCS.
    # Since we specified batch_size=2, the first response contains
    # the first two pages of the input file.
    output = blob_list[0]

    json_string = output.download_as_string()
    response = json.loads(json_string)

    # The actual response for the first page of the input file.
    first_page_response = response["responses"][0]
    annotation = first_page_response["fullTextAnnotation"]

    # Here we print the full text from the first page.
    # The response contains more information:
    # annotation/pages/blocks/paragraphs/words/symbols
    # including confidence scores and bounding boxes
    print("Full text:\n")
    return annotation["text"]
