"""Routing Request to Views of OCR Pages."""
import asyncio
import json
import logging
import os
from datetime import datetime

import pytz
from django.contrib import messages
from django.core.cache import cache
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import FormView, TemplateView
from dotenv import load_dotenv
from google.api_core.exceptions import InvalidArgument

from ocr.dummy_data import RBIDummy
from ocr.firestore_model import FirestoreModel
from ocr.form_recognizer import form_recognizer_runner
from ocr.forms import UploadForm
from ocr.scripts import Script
from one_barangay.scripts.storage_backends import AzureStorageBlob

load_dotenv()

logger = logging.getLogger(__name__)


# TODO: Use Django Forms for displaying html forms.
class FileUploadView(FormView):
    """View for file upload."""

    form_class = UploadForm
    template_name = "ocr/file_upload.html"

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
        # TODO: Refactor OCR Files UI for redundant UI.
        dict_files = [json.loads(file) for file in request.POST.getlist("fileData")]

        request.session["files"] = self.script.format_file_upload_card(dict_files)

        for file in files:
            default_storage.save(file.name, file)

        return HttpResponse(request.session["files"])


# Todo: Fix settings-box.html.
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


# Todo: Fix File Card UI.
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


# TODO: Change color of feedback depending on confidence level.
class ScanResultView(TemplateView):
    """View for scan_result.html."""

    template_name = "ocr/scan_result.html"

    def get_context_data(self, **kwargs):
        """Get context data and run form recognizer.

        Args:
          **kwargs: Additional keyword argument (Filename).

        Returns:
          : scan_result.html with context of detected text from table image.
        """
        ocr = cache.get("ocr")
        if ocr is None:
            ocr = asyncio.run(form_recognizer_runner(kwargs["filename"]))
            cache.set("ocr", ocr, timeout=None)
            logger.warning("OCR result is not cached!")

        else:
            logger.info("OCR result is cached!")

        scanned_file_index = next(
            (
                idx
                for idx, dictionary in enumerate(self.request.session["files"])
                if dictionary["name"] == kwargs["filename"]
            ),
            None,
        )

        if scanned_file_index is not None:
            del self.request.session["files"][scanned_file_index]
            self.request.session.modified = True

            default_storage.delete(kwargs["filename"])

        return {"ocr_header": ocr[0], "ocr_text": ocr[1]}


# TODO: Add regex checking in input fields.
class SaveScanResultView(FormView):
    """View for file upload."""

    template_name = "ocr/scan_result.html"

    def __init__(self):
        """Initialize SaveScanResultView class variables."""
        self.firestore = FirestoreModel()
        self.script = Script()

    def post(self, request, *args, **kwargs):
        """Get context data and run form recognizer.

        Args:
          **kwargs: Additional keyword argument (Filename).
          request:
          *args:

        Returns:
          : scan_result.html with context of detected text from table image.
        """
        house_num = request.POST.get("house_num")
        created_at = datetime.now(tz=pytz.timezone("Asia/Manila")).isoformat()
        address = request.POST.get("address")
        date_accomplished = request.POST.get("date")
        last_name = request.POST.getlist("last_name")
        fist_name = request.POST.getlist("fist_name")
        middle_name = request.POST.getlist("middle_name")
        ext = request.POST.getlist("ext")
        birth_place = request.POST.getlist("birth_place")
        birth_date = request.POST.getlist("birth_date")
        sex = request.POST.getlist("sex")
        civil_status = request.POST.getlist("civil_status")
        citizenship = request.POST.getlist("citizenship")
        monthly_income = request.POST.getlist("monthly_income")
        remarks = request.POST.getlist("remarks")

        family_member_dictionary = {}
        for data in zip(
            last_name,
            fist_name,
            middle_name,
            ext,
            birth_place,
            birth_date,
            sex,
            civil_status,
            citizenship,
            monthly_income,
            remarks,
        ):
            family_member_dictionary[data[1]] = {
                "last_name": data[0],
                "first_name": data[1],
                "middle_name": data[2],
                "ext": data[3],
                "birth_place": data[4],
                "birth_date": data[5],
                "sex": data[6],
                "civil_status": data[7],
                "citizenship": data[8],
                "monthly_income": data[9],
                "remarks": data[10],
            }

        my_data = {
            "house_num": house_num,
            "created_at": created_at,
            "address": address,
            "date_accomplished": date_accomplished,
            "family_members": family_member_dictionary,
        }

        try:
            formatted_data = self.script.format_firestore_data([my_data])
            if os.getenv("GAE_ENV", "").startswith("standard"):
                azure_storage = AzureStorageBlob()
                json_data = azure_storage.append_to_json_data(formatted_data["rows"])
                azure_storage.upload_json_data(json_data)
            else:
                self.script.append_to_local_json_file(formatted_data)

            self.firestore.store_rbi(my_data)

            logger.info("RBI Document saved!")
            messages.add_message(request, messages.SUCCESS, "RBI Document is saved!")

        except InvalidArgument as e:
            logger.exception("RBI document not saved! %s", e)
            messages.add_message(request, messages.ERROR, "RBI document not saved!")

        return redirect("ocr_files")


# TODO: Add custom view for profiling.
class RBITableView(TemplateView):
    """View for rbi_table.html."""

    template_name = "ocr/rbi_table.html"

    def get_context_data(self, **kwargs):
        """Get json file url.

        Get the json file to display RBI table.
        Args:
          **kwargs: Keyword arguments.

        Returns:
          The url for json file.
        """
        if os.getenv("GAE_ENV", "").startswith("standard"):
            url = AzureStorageBlob().file_url
        else:
            # run ./simple_cors_server.py
            url = "http://127.0.0.1:9000/rbi_data.json"

        return {"url": url}


class DummyRBIView(FormView):
    """View for rbi_dummy.html."""

    form_class = UploadForm
    template_name = "ocr/rbi_dummy.html"

    def post(self, request, *args, **kwargs):
        """POST method to render dummy rbi.

        Args:
          request: The URL request.
          *args: Additional arguments.
          **kwargs: Additional keyword arguments.

        Returns:
          The rbi_dummy.html along with the generated dummy list.
        """
        generated_dummy_list = []
        dummy_count = int(request.POST["dummyCount"])

        firestore = FirestoreModel()
        script = Script()
        azure_storage = AzureStorageBlob()

        for _ in range(dummy_count):
            dummy_data = RBIDummy().create_dummy_rbi()
            formatted_data = script.format_firestore_data([dummy_data])

            generated_dummy_list += formatted_data["rows"]

            if os.getenv("GAE_ENV", "").startswith("standard"):
                json_data = azure_storage.append_to_json_data(formatted_data["rows"])
                azure_storage.upload_json_data(json_data)
            else:
                script.append_to_local_json_file(formatted_data)

            firestore.store_rbi(dummy_data)

        return render(request, self.template_name, {"generated_dummy": generated_dummy_list})
