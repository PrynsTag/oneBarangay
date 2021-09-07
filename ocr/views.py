"""Routing Request to Views of OCR Pages."""
import json
import os
import re

from django.shortcuts import render
from django.views import View
from dotenv import load_dotenv
from google.cloud import storage, vision

from ocr.forms import UploadForm

load_dotenv()


class FileUploadView(View):
    """View for file upload."""

    def get(self, request):
        """Get request from file upload.

        Args:
          request: The URL request.

        Returns:
          The file_upload.html along with context to display form.
        """
        form = UploadForm()
        return render(
            request=request,
            template_name="ocr/file_upload.html",
            context={"form": form},
        )

    def post(self, request):
        """Post request from file upload.

        Args:
          request: The URL request.

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


def scan_file(request):
    """Fetch OCR HTML Pages.

    Args:
      slug: the filename slugify
      request: The URL Request.

    Returns:
      Renders ocr_files.html.
    """
    return render(request=request, template_name="ocr/ocr_files.html")


def scan_result(request, name):
    """Fetch the uploaded files for scanning.

    Args:
      request: The URL Request.

    Returns:
      The scan_file.html page requested in the URL.
    """
    gsc_source_uri = "gs://" + os.getenv("GS_MEDIA_BUCKET_NAME") + "/documents/" + name
    gcs_destination_uri = "gs://" + "scan_result" + "/documents/" + name
    return render(
        context={
            "ocr_text": async_detect_document(gsc_source_uri, gcs_destination_uri)
        },
        request=request,
        template_name="ocr/scan_result.html",
    )


def async_detect_document(gcs_source_uri, gcs_destination_uri):
    """OCR with PDF/TIFF as source files on GCS."""
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
