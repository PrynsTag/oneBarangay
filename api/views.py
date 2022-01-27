"""Create your api views here."""
import asyncio
import os

import pandas as pd
from django.core.cache import cache
from django.http import JsonResponse

# Create your views here.
from django.templatetags.static import static
from firebase_admin import messaging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import NotificationSerializer, NpEncoder
from ocr.form_recognizer import form_recognizer_runner
from one_barangay.local_settings import logger
from one_barangay.settings import firebase_app, firestore_db


class OcrApiView(APIView):
    """Get the OCR result."""

    def get(self, request, filename):
        """GET request to get the scan result.

        Args:
          request: The URL Request.
          filename: The name of the file to be scanned.

        Returns:
          A 2-element list containing text and confidence level.
        """
        if os.getenv("GAE_ENV", "").startswith("standard"):
            ocr_result = asyncio.run(form_recognizer_runner(filename))
        else:
            # For Local Testing
            ocr_result = cache.get("ocr")
            if ocr_result is None:
                ocr_result = asyncio.run(form_recognizer_runner(filename))
                cache.set("ocr", ocr_result, timeout=None)
                logger.warning("OCR result is not cached!")

            else:
                logger.info("OCR result is cached!")

        return JsonResponse({"house_data": [ocr_result[0]], "family_data": ocr_result[1]}, safe=False)


class DataVizApiView(APIView):
    """Get the data viz data."""

    def get(self, request):
        """Generate statistics based from RBI JSON file.

        Args:
          request: The URL Request.

        Returns:
          A dictionary containing keys for processed data.
        """
        # ### Initial Setup
        rbi_docs = firestore_db.collection("rbi").stream()
        data = {"rows": []}
        for rbi in rbi_docs:
            family_docs = firestore_db.collection("rbi").document(rbi.id).collection("family").stream()
            for family in family_docs:
                data["rows"].append(rbi.to_dict() | family.to_dict())

        df = pd.DataFrame(data["rows"])

        # ### Convert Dates to Datetime
        df["birth_date"] = pd.to_datetime(df["date_of_birth"], errors="coerce", format="%B %d, %Y")
        df["date_accomplished"] = pd.to_datetime(df["date_accomplished"], errors="coerce", format="%Y-%m-%d", utc=True)

        # ### Convert Monthly Income to Int
        try:
            df["monthly_income"] = (
                df["monthly_income"]
                .str.replace(",", "", regex=False)
                .str.replace(" ", "", regex=False)
                .str.replace(".", "", regex=False)
                .str.replace("$", "", regex=False)
            )
            df["monthly_income"] = pd.to_numeric(df["monthly_income"])
        except ValueError as e:
            mask = pd.to_numeric(df["monthly_income"], errors="coerce").isna()
            not_converted = df.loc[mask, "monthly_income"].tolist()
            logger.exception(e)
            logger.exception("Not Converted: %s", not_converted)
        finally:
            df["monthly_income"] = pd.to_numeric(df["monthly_income"], errors="coerce", downcast="float")
            df["monthly_income"].fillna(0, inplace=True)

        # ### Create Age Groups Given Age
        # #### Calculate Age From Birth Date
        now = pd.Timestamp.now()
        df["age"] = (now - df["birth_date"]).astype("<m8[Y]")
        df["age"] = df["age"].astype("Int64")

        # #### Calculate Age Groups
        bins = [0, 2, 4, 13, 20, 110]
        labels = ["Infant", "Toddler", "Kid", "Teen", "Adult"]
        df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=False)

        age_group_labels = df["age_group"].value_counts().index.values.tolist()
        age_group_values = df["age_group"].value_counts().values.tolist()

        # ### Number of Citizenship per Category
        citizenship_labels = df.groupby("citizenship").size().index.values.tolist()
        citizenship_values = df.groupby("citizenship").size().values.tolist()

        # ### Number of Civil Status per Category
        civil_status_labels = df.groupby("civil_status").size().index.values.tolist()
        civil_status_values = df.groupby("civil_status").size().values.tolist()

        # ### Average Family Members in A house
        house_members_avg = df["house_num"].value_counts().mean().astype(int)

        # ### Social Class Given Monthly Income
        bins = [0, 7890, 15780, 31560, 78900, 118350, 157800, 200000, 500000]
        labels = [
            "Not Applicable",
            "Poor",
            "Low Income",
            "Lower Middle Income",
            "Middle Middle Income",
            "Upper Middle Income",
            "Upper Income",
            "Rich",
        ]
        df["social_class"] = pd.cut(df["monthly_income"], bins=bins, labels=labels, right=False)

        social_class_labels = df["social_class"].value_counts().index.values.tolist()
        social_class_values = df["social_class"].value_counts().values.tolist()

        # ### Number of RBI in Database
        num_recorded_rbi = len(df.groupby("house_num").sum().index.values.tolist())

        # ### Average Salary per Person
        person_avg_salary = df[df["monthly_income"] != 0]["monthly_income"].mean().astype("int")

        # ### Average Salary per Household
        household = df.groupby(["house_num"])["monthly_income"].sum()
        household_avg_salary = household.values.mean().astype("int")

        data = {
            "age_group": {"labels": age_group_labels, "values": age_group_values},
            "citizenship": {"labels": citizenship_labels, "values": citizenship_values},
            "civil_status": {"labels": civil_status_labels, "values": civil_status_values},
            "house_members": {"avg": house_members_avg},
            "rbi": {"count": num_recorded_rbi},
            "avg_salary": {"person": person_avg_salary, "household": f"{household_avg_salary:,}"},
            "social_class": {"labels": social_class_labels, "values": social_class_values},
            "total_population": {"values": f"{len(df.index):,}"},
        }

        return JsonResponse(data, encoder=NpEncoder)


class SendNotification(APIView):
    """Get the OCR result."""

    def post(self, request):
        """POST request to send notification.

        Args:
          request: The URL Request.

        Returns:
          A response object for success or fail.
        """
        serializer = NotificationSerializer(data=request.data)

        if serializer.is_valid():
            title = serializer.data["title"]
            body = serializer.data["body"]
            registration_token = serializer.data["token"]

            icon = static("/assets/img/favicon/favicon.ico")

            message_data = {
                "title": title,
                "body": body,
                "icon": static("/assets/img/favicon/favicon.ico"),
                "requireInteraction": "true",
            }

            message = messaging.Message(
                notification=messaging.Notification(title=title, body=body, image=icon),
                data=message_data,
                token=registration_token,
            )
            messaging.send(message, app=firebase_app)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
