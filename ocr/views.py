"""Routing Request to Views of OCR Pages."""
import asyncio
import os
from datetime import date, datetime
from typing import Union
from urllib.parse import urlparse

import pytz
from django.contrib import messages
from django.core.cache import cache
from django.core.files.storage import default_storage
from django.http import (
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import redirect
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDict
from django.views.generic import FormView, TemplateView
from firebase_admin import firestore
from google.api_core.exceptions import InvalidArgument, NotFound

from ocr.form_recognizer import form_recognizer_runner
from ocr.forms import OcrEditForm, OcrResultForm, OcrUploadForm
from one_barangay.local_settings import logger
from one_barangay.mixins import ContextPageMixin, FormInvalidMixin
from one_barangay.settings import firebase_app


class OcrFileUploadView(ContextPageMixin, FormView):
    """View for file upload."""

    form_class = OcrUploadForm
    template_name = "ocr/file_upload.html"
    success_url = reverse_lazy("ocr:upload")
    title = "File Upload"
    sub_title = "Upload RBI documents for scanning."
    segment = "ocr"

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        files = [self.request.FILES[file] for file in self.request.FILES]
        kwargs.update({"files": MultiValueDict({"file_upload": files})})

        return kwargs

    def post(self, request, *args, **kwargs):
        """POST request to upload OCR form files.

        Args:
          request: The URL request.
          **args: Additional arguments.
          **kwargs: Additional keyword arguments.

        Returns:
          A JSONResponse for success and failure of upload.
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = [request.FILES[file] for file in request.FILES]

        file_data = []
        request.session["files"] = []
        if form.is_valid():
            for file in files:
                filename = default_storage.generate_filename(file.name)
                default_storage.save(filename, file)
                thumbnail_url = default_storage.url(filename)

                path = urlparse(thumbnail_url).path
                ext = os.path.splitext(path)[1]
                if ext == ".pdf":
                    thumbnail_url = static("/assets/img/default-pdf-image.jpg")

                file_data.append((filename, thumbnail_url))
            request.session["files"] += file_data

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Call when OcrUploadForm is INVALID.

        Args:
          form: The submitted OcrUploadForm.

        Returns:
          The invalid OcrUploadForm submitted.
        """
        for field in form.errors:
            form[field].field.widget.attrs["class"] += " is-invalid"

        messages.error(self.request, "Files not uploaded!")
        return JsonResponse({"error": form.errors.as_json()}, status=400)


def remove_file(request, filename):
    """Remove a OCR uploaded file.

    Args:
      request: The URL request.
      filename: The name of the file to be remove.

    Returns:
      A HTTPResponseRedirect to OCR upload page.
    """
    remove(request.session, filename)

    return redirect("ocr:upload")


# TODO: Change color of feedback depending on confidence level.
class OcrResultView(ContextPageMixin, FormView):
    """View for scan result of ocr."""

    template_name = "ocr/scan_result.html"
    form_class = OcrResultForm
    success_url = reverse_lazy("ocr:upload")
    title = "OCR Result"
    sub_title = "Page for ocr result."
    segment = "ocr"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """GET request to display OCR scan result.

        Args:
          request: The URL request.
          **args: Additional arguments.
          **kwargs: Additional keyword arguments.

        Returns:
          The context data with OCR result.
        """
        form_kwargs = self.get_form_kwargs()
        context = self.get_context_data(**kwargs)

        if os.getenv("GAE_ENV", "").startswith("standard"):
            ocr = asyncio.run(form_recognizer_runner(kwargs["filename"]))
        else:
            # For Local Testing
            ocr = cache.get("ocr")
            if ocr is None:
                ocr = asyncio.run(form_recognizer_runner(kwargs["filename"]))
                cache.set("ocr", ocr, timeout=None)
                logger.warning("OCR result is not cached!")

            else:
                logger.info("OCR result is cached!")

        context["ocr_header"] = ocr[0]
        context["ocr_text"] = ocr[1]

        form_kwargs["header"] = ocr[0]
        form_kwargs["ocr_result"] = ocr[1]

        # For displaying RBI in HTML.
        context["document_type"] = os.path.splitext(kwargs["filename"])[1]
        context["document_url"] = default_storage.url(kwargs["filename"])
        context["document_name"] = kwargs["filename"]
        context["client_id"] = os.getenv("ADOBE_CLIENT_ID")

        return self.render_to_response(context)


# TODO: Add regex checking in input fields.
class OcrSaveView(FormView):
    """View for file upload."""

    template_name = "ocr/scan_result.html"

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

        family_member_data = {}
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
            family_member_data[data[1]] = {
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

        family_data = {
            "house_num": house_num,
            "created_at": created_at,
            "address": address,
            "date_accomplished": date_accomplished,
        }

        try:
            db = firestore.client(app=firebase_app)
            db.collection("rbi").document(house_num).set(family_data, merge=True)
            (
                db.collection("rbi")
                .document(house_num)
                .collection("family")
                .document(house_num)
                .set(family_member_data, merge=True)
            )
            remove(self.request.session, request.POST["filename"])

            logger.info("RBI Document saved!")
            messages.add_message(request, messages.SUCCESS, "RBI Document is saved!")
        except InvalidArgument as e:
            logger.exception("RBI document not saved! %s", e)
            messages.add_message(request, messages.ERROR, "RBI document not saved!")

        return redirect("ocr:upload")


class OcrHomeView(TemplateView):
    """View for rbi_table.html."""

    template_name = "ocr/home.html"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """GET request to display rbi collection to ocr home.

        Args:
          **args: Additional arguments.
          **kwargs: Additional keyword arguments.

        Returns:
          The firestore rbi collection data.
        """
        context = self.get_context_data(**kwargs)

        db = firestore.client(app=firebase_app)
        docs = db.collection("rbi").stream()

        rbi = [doc.to_dict() for doc in docs]
        context["rbi"] = rbi

        return self.render_to_response(context)

    def get_context_data(self, **kwargs) -> dict:
        """Get context data to ocr home.

        Args:
          **kwargs: Keyword arguments.

        Returns:
          The dictionary data needed by ocr home.
        """
        context = super().get_context_data()

        context["segment"] = "ocr"
        context["title"] = "OCR"
        context["sub_title"] = "List of RBI in the database."
        context["id"] = "house_num"
        context["default_image"] = static("/assets/img/default-rbi-image.jpg")
        context["sort"] = [
            {"sortName": "creation_date", "sortOrder": "desc"},
            {"sortName": "house_num", "sortOrder": "asc"},
        ]

        return context


class OcrEditView(FormInvalidMixin, ContextPageMixin, FormView):
    """View for editing rbi."""

    template_name = "ocr/edit.html"
    form_class = OcrEditForm
    success_url = reverse_lazy("ocr:home")
    title = "OCR"
    sub_title = "List of RBI in the database."
    segment = "ocr"
    error_message = "RBI edit not successful! Please fix the errors displayed in the form!"

    def get_form_kwargs(self):
        """Pass house number data to OcrEditForm."""
        kwargs = super().get_form_kwargs()

        house_num = self.kwargs["house_num"]
        db = firestore.client(app=firebase_app)
        rbi = db.collection("rbi").document(house_num).get().to_dict()

        kwargs["rbi"] = rbi

        return kwargs

    def form_valid(self, form):
        """Call when OcrEditForm is VALID.

        Updates the rbi collection with the given house number.
        Args:
          form: The submitted OcrEditForm.

        Returns:
          The valid OcrEditForm submitted.
        """
        changed_fields = {}
        if form.has_changed():
            for field in form.changed_data:
                changed_fields[field] = form.cleaned_data[field]

        if changed_fields:
            db = firestore.client(app=firebase_app)
            try:
                # Update rbi collection.
                (
                    db.collection("rbi")
                    .document(form.cleaned_data["house_num"])
                    .update(changed_fields)
                )
            except NotFound:
                messages.info(
                    self.request,
                    f"RBI data not updated! NO RBI \
                    #${form.cleaned_data['house_num']} in the database!",
                )
                logger.info("[OcrEditView.form_valid] User data not updated!")

            changed_fields_name = [form.fields[key].label for key in changed_fields]
            messages.success(self.request, f"Edited {''.join(changed_fields_name)} successfully!")
            logger.info(
                "[OcrEditView.form_valid] Form successfully updated for fields %s.",
                "".join(changed_fields_name),
            )
        else:
            messages.info(self.request, "No change detected! Database is not updated.")
            logger.info("[OcrEditView.form_valid] No fields to updated!")

        messages.success(self.request, "")

        return super().form_valid(form)


class OcrDetailView(TemplateView):
    """View for single rbi."""

    template_name = "ocr/detail.html"

    def get(self, request, house_num, *args, **kwargs) -> HttpResponse:  # type: ignore
        """Get Request to ocr detail to display single rbi.

        Args:
          request: The URL request.
          house_num: The unique id of RBI.
          **args: Additional arguments.
          **kwargs: Additional keyword arguments.

        Returns:
          A single firestore rbi document.
        """
        context = self.get_context_data(**kwargs)

        db = firestore.client(app=firebase_app)
        family = db.collection("rbi").document(house_num).collection("family").get()

        clean_family = []
        for member in family:
            family_member = member.to_dict()

            # Calculate Age
            birth_date_dt = datetime.strptime(family_member["birth_date"], "%B %d, %Y")
            today = date.today()
            age = (
                today.year
                - birth_date_dt.year
                - ((today.month, today.day) < (birth_date_dt.month, birth_date_dt.day))
            )
            family_member["age"] = age

            clean_family.append(family_member)

        context["family"] = clean_family

        return self.render_to_response(context)

    def get_context_data(self, **kwargs) -> dict:
        """Get context data to ocr detail.

        Args:
          **kwargs: Additional keyword arguments.

        Returns:
          The dictionary data needed by ocr detail.
        """
        context = super().get_context_data()

        context["segment"] = "ocr"
        context["title"] = "Family"
        context["sub_title"] = "Information about family stored in RBI."

        return context


def delete(request, house_num) -> Union[HttpResponseRedirect, HttpResponsePermanentRedirect]:
    """Delete RBI in the table.

    Args:
      request: The URL Request.
      house_num: The unique id of RBI.

    Returns:
      Redirect to ocr home.
    """
    db = firestore.client(app=firebase_app)
    if house_num:
        try:
            docs = db.collection("rbi").document(house_num).collection("family").stream()
            for doc in docs:
                doc.reference.delete()

            db.collection("rbi").document(house_num).delete()
            messages.success(request, f"RBI with house number ${house_num} Deleted Successfully!")
            logger.info(request, "RBI with house number %s Deleted Successfully!", house_num)
        except NotFound:
            messages.error(request, f"RBI with house #${house_num} Not Found!")
            logger.info(request, "RBI with house #%s Not Found!", house_num)
        except ValueError as e:
            messages.error(request, f"Something when wrong {e}")
    else:
        messages.error(request, "NO house number Provided!")

    return redirect("ocr:home")


def remove(session, filename):
    """Get the index of the filename from session.

    Args:
      session: The session variable that contains the 'file' variable.
      filename: The name of the file to be deleted.

    Returns:
      None.
    """
    scanned_file_index = next(
        (idx for idx, file in enumerate(session["files"]) if file[0] == filename),
        None,
    )

    # Delete file from "session files" given index
    if scanned_file_index is not None:
        del session["files"][scanned_file_index]
        session.modified = True

        default_storage.delete(filename)
