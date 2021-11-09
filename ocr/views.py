"""Routing Request to Views of OCR Pages."""
import asyncio
import copy
import os
import random
import re
from datetime import date, datetime, timedelta
from typing import Union
from urllib.parse import urlparse

from dateutil import parser
from dateutil.parser import ParserError
from django.contrib import messages
from django.core.cache import cache
from django.core.files.storage import default_storage
from django.forms import formset_factory
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
from google.api_core.exceptions import NotFound

from ocr.form_recognizer import form_recognizer_runner
from ocr.forms import OcrEditForm, OcrFamilyForm, OcrHouseForm, OcrUploadForm
from one_barangay.local_settings import logger
from one_barangay.mixins import ContextPageMixin, FormInvalidMixin
from one_barangay.settings import firebase_app, firestore_db
from one_barangay.templatetags.custom_template_tags import get_formset_field_name


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

            if request.session.get("files"):
                request.session["files"] += file_data
            else:
                request.session["files"] = file_data

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
    form_class = OcrFamilyForm
    success_url = reverse_lazy("ocr:upload")
    title = "OCR Result"
    sub_title = "Page for ocr result."
    segment = "ocr"
    error_message = "You got it wrong!"

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        context = super().get_context_data(**kwargs)

        # For displaying RBI in HTML.
        context["document_type"] = os.path.splitext(kwargs["filename"])[1]
        context["document_url"] = default_storage.url(kwargs["filename"])
        context["document_name"] = kwargs["filename"]
        context["client_id"] = os.getenv("ADOBE_CLIENT_ID")

        context["first_row"] = ["last_name", "first_name", "middle_name", "ext"]
        context["second_row"] = ["place_of_birth", "date_of_birth", "gender", "civil_status"]
        context["third_row"] = ["citizenship", "monthly_income", "remarks"]
        context["house_data_field"] = ["house_num", "address", "date_accomplished"]

        return context

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """GET request to display OCR scan result.

        Args:
          request: The URL request.
          **args: Additional arguments.
          **kwargs: Additional keyword arguments.

        Returns:
          The context data with OCR result.
        """
        context = self.get_context_data(**kwargs)

        if os.getenv("GAE_ENV", "").startswith("standard"):
            ocr_result = asyncio.run(form_recognizer_runner(kwargs["filename"]))
        else:
            # For Local Testing
            ocr_result = cache.get("ocr")
            if ocr_result is None:
                ocr_result = asyncio.run(form_recognizer_runner(kwargs["filename"]))
                cache.set("ocr", ocr_result, timeout=None)
                logger.warning("OCR result is not cached!")

            else:
                logger.info("OCR result is cached!")

        family_initial = []
        family_confidence = []
        house_initial = {}
        house_confidence = {}

        for family_data in ocr_result[1]:
            monthly_income = family_data["monthly_income"]["text"]
            date_of_birth = re.sub(r"\s", "", family_data["date_of_birth"]["text"])
            family_initial.append(
                {
                    "last_name": family_data["last_name_apelyido"]["text"],
                    "first_name": family_data["first_name_pangalan"]["text"],
                    "middle_name": family_data["middle_name"]["text"],
                    "ext": family_data["ext"]["text"],
                    "date_of_birth": parser.parse(date_of_birth).strftime("%B %d, %Y"),
                    "place_of_birth": family_data["place_of_birth"]["text"],
                    "gender": family_data["sex_m_or_f"]["text"],
                    "civil_status": family_data["civil_status"]["text"],
                    "citizenship": family_data["citizenship"]["text"],
                    "monthly_income": int(re.sub(r"\D", "", monthly_income)),
                    "remarks": family_data["remarks"]["text"],
                }
            )
            family_confidence.append(
                {
                    "last_name": family_data["last_name_apelyido"]["confidence"],
                    "first_name": family_data["first_name_pangalan"]["confidence"],
                    "middle_name": family_data["middle_name"]["confidence"],
                    "ext": family_data["ext"]["confidence"],
                    "place_of_birth": family_data["place_of_birth"]["confidence"],
                    "date_of_birth": family_data["date_of_birth"]["confidence"],
                    "gender": family_data["sex_m_or_f"]["confidence"],
                    "civil_status": family_data["civil_status"]["confidence"],
                    "citizenship": family_data["citizenship"]["confidence"],
                    "monthly_income": family_data["monthly_income"]["confidence"],
                    "remarks": family_data["remarks"]["confidence"],
                }
            )
        house_initial["address"] = ocr_result[0]["address"]["text"]
        house_initial["date_accomplished"] = ocr_result[0]["date"]["text"]
        house_initial["house_num"] = ocr_result[0]["household_no."]["text"]

        house_confidence["address"] = ocr_result[0]["address"]["confidence"]
        house_confidence["date_accomplished"] = ocr_result[0]["date"]["confidence"]
        house_confidence["house_num"] = ocr_result[0]["household_no."]["confidence"]

        formset = formset_factory(OcrFamilyForm, extra=0)
        family_form = formset(initial=family_initial)

        house_form = OcrHouseForm(initial=house_initial)

        for field in house_form:
            field_name = field.html_name
            if field_name in ["address", "date_accomplished", "house_num"]:
                field_confidence = (
                    round(float(house_confidence.get(field_name)) * 100, 2)
                    if house_confidence.get(field_name)
                    else 0.0
                )
                if field_confidence <= 66.0:
                    field.field.widget.attrs["class"] += " is-invalid text-danger"
                else:
                    field.field.widget.attrs["class"] += " is-valid text-success"

                field.help_text = str(field_confidence)

        for form, confidence in zip(family_form, family_confidence):
            for field in form:
                field_name = get_formset_field_name(field.html_name)
                field_confidence = (
                    round(float(confidence.get(field_name)) * 100, 2)
                    if confidence.get(field_name)
                    else 0.0
                )
                if field_confidence <= 66.0:
                    field.field.widget.attrs["class"] += " is-invalid text-danger"
                else:
                    field.field.widget.attrs["class"] += " is-valid text-success"

                field.help_text = str(field_confidence)

        if "family_form" not in context:
            context["family_form"] = family_form
        if "house_form" not in context:
            context["house_form"] = house_form

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        """POST request to handle RBI submission.

        Args:
          request: The URL request.
          **args: Additional arguments.
          **kwargs: Additional keyword arguments.

        Returns:
          The invalid or valid family and house form.
        """
        family_data = copy.deepcopy(request.POST.dict())
        filename = kwargs["filename"]
        house_data = {
            "region": family_data.pop("region"),
            "province": family_data.pop("province"),
            "city": family_data.pop("city"),
            "barangay": family_data.pop("barangay"),
            "house_num": family_data.pop("house_num"),
            "address": family_data.pop("address"),
            "date_accomplished": family_data.pop("date_accomplished"),
            "creation_date": family_data.pop("creation_date"),
        }
        house_form = OcrHouseForm(house_data)
        family_formset = formset_factory(OcrFamilyForm, extra=0)
        family_form = family_formset(request.POST)

        if family_form.is_valid() and house_form.is_valid():
            remove(request.session, filename)
            default_storage.delete(filename)
            return self.form_valid(family_form, house_form)
        else:
            return self.form_invalid(family_form, house_form)

    def form_valid(self, family_form, house_form):
        """Call when OcrFamilyForm and OcrHouseForm is VALID.

        Save the valid form in firestore.
        Args:
          family_form: The submitted OcrFamilyForm.
          house_form: The submitted OcrHouseForm.

        Returns:
          The valid OcrFamilyForm and OcrHouseForm submitted.
        """
        # TODO: Add street address.
        house_data = house_form.cleaned_data

        date_accomplished = house_data["date_accomplished"]
        house_data["date_accomplished"] = datetime(
            date_accomplished.year,
            date_accomplished.month,
            date_accomplished.day,
        )

        # Add house data to rbi collection
        rbi_ref = firestore_db.collection("rbi").document(house_data["house_num"])
        rbi_ref.set(house_data, merge=True)

        family_col = rbi_ref.collection("family")
        family_list_docs = list(family_col.stream())

        # Check if family sub-collection exists
        if family_list_docs:
            for form in family_form:
                family_doc = family_col.document()
                family_data = form.cleaned_data

                # Convert date to datetime.
                date_of_birth = family_data["date_of_birth"]
                family_data["date_of_birth"] = datetime(
                    date_of_birth.year,
                    date_of_birth.month,
                    date_of_birth.day,
                )

                first_name_query = family_col.where(
                    "first_name", "==", family_data["first_name"]
                ).get()[0]
                birth_date_query = family_col.where(
                    "date_of_birth", "==", family_data["date_of_birth"]
                ).get()[0]

                # Add family data to family sub-collection
                if first_name_query.exists and birth_date_query.exists:
                    family_col.document(first_name_query.id).update(family_data)
                else:
                    family_data["member_id"] = family_doc.id
                    family_doc.set(family_data)

        else:
            for form in family_form:
                family_doc = family_col.document()
                family_data = form.cleaned_data

                date_of_birth = family_data["date_of_birth"]
                family_data["date_of_birth"] = datetime(
                    date_of_birth.year,
                    date_of_birth.month,
                    date_of_birth.day,
                )

                family_data["member_id"] = family_doc.id
                family_doc.set(family_data)

        messages.success(self.request, "RBI Document Saved!")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, family_form, house_form):
        """Call when OcrFamilyForm and OcrHouseForm is INVALID.

        Display errors in the form.
        Args:
          family_form: The submitted OcrFamilyForm.
          house_form: The submitted OcrHouseForm.

        Returns:
          The invalid OcrFamilyForm and OcrHouseForm submitted.
        """
        for form in family_form:
            for field in form.errors:
                form[field].field.widget.attrs["class"] += " is-invalid"

        for field in house_form.errors:
            house_form[field].field.widget.attrs["class"] += " is-invalid"

        messages.error(self.request, "RBI form invalid! Please fix the errors in the form!")
        return self.render_to_response(
            self.get_context_data(
                family_form=family_form,
                house_form=house_form,
                filename=self.kwargs["filename"],
            )
        )


class OcrHomeView(TemplateView):
    """View for rbi_table.html."""

    template_name = "ocr/home.html"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """GET request to display rbi collection to ocr home.

        Args:
          request: The URL request.
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
            try:
                birth_date_dt = parser.parse(family_member["birth_date"])
            # FIXME: Add server validation in ocr.
            except ParserError:
                birth_date_dt = datetime.now() - timedelta(days=random.randrange(365, 9999))

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
