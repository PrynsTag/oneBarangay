"""Recognize and extract forms."""
import os
from statistics import fmean

from azure.ai.formrecognizer.aio import FormRecognizerClient, FormTrainingClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()


class RecognizeCustomFormsSampleAsync:
    """Class to recognize forms in async mode."""

    async def recognize_custom_forms(self, custom_model_id, filename):
        """Extract text from custom form.

        Args:
          custom_model_id: The trained custom model id.
          filename: The filename of the document that will be scanned.

        Returns:
          The header for the table and the extracted text.
        """
        endpoint = os.environ["AZURE_FORM_RECOGNIZER_ENDPOINT"]
        key = os.environ["AZURE_FORM_RECOGNIZER_KEY"]
        model_id = os.getenv("CUSTOM_TRAINED_MODEL_ID", custom_model_id)

        async with FormRecognizerClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        ) as form_recognizer_client:

            # Make sure your form's type is included in the
            # list of form types the custom model can recognize
            form_url = (
                "https://storage.googleapis.com/"
                + os.getenv("GS_MEDIA_BUCKET_NAME")
                + "/documents/"
                + filename
            )
            poller = await form_recognizer_client.begin_recognize_custom_forms_from_url(
                model_id=model_id, form_url=form_url, include_field_elements=True
            )
            forms = await poller.result()
            table = []
            header = {}
            for _, form in enumerate(forms):
                count = 0
                row = {}
                for name, field in form.fields.items():
                    if count >= 3:
                        for value in field.value:
                            for i, val in value.to_dict()["value"].items():
                                data = val["value_data"]

                                # Condition for "No Data"
                                if data:
                                    words = data["field_elements"]
                                    # Condition for multiple word result
                                    if len(words) > 1:
                                        word_list = [word["text"] for word in words]
                                        confidence_list = [word["confidence"] for word in words]
                                        slug_name = (
                                            val["name"]
                                            .lower()
                                            .replace(" ", "_")
                                            .replace("(", "")
                                            .replace(")", "")
                                        )
                                        row[slug_name] = {
                                            "text": " ".join(word_list),
                                            "confidence": round(fmean(confidence_list), 3),
                                        }
                                    else:
                                        slug_name = (
                                            val["name"]
                                            .lower()
                                            .replace(" ", "_")
                                            .replace("(", "")
                                            .replace(")", "")
                                        )
                                        row[slug_name] = {
                                            "text": words[0]["text"],
                                            "confidence": words[0]["confidence"],
                                        }
                                else:
                                    slug_name = (
                                        val["name"]
                                        .lower()
                                        .replace(" ", "_")
                                        .replace("(", "")
                                        .replace(")", "")
                                    )
                                    row[slug_name] = {
                                        "text": data,
                                        "confidence": data,
                                    }

                                if i == "REMARKS":
                                    table.append(row)
                                    row = {}
                    else:
                        slug_name = (
                            name.lower().replace(" ", "_").replace("(", "").replace(")", "")
                        )
                        header[slug_name] = {
                            "text": field.value,
                            "confidence": field.confidence,
                        }
                    count += 1
            return header, table


async def form_recognizer_runner(filename):
    """Runner for the form recognizer.

    Args:
      filename: The filename of the document to be scanned

    Returns:
      The form header and the table scanned.
    """
    sample = RecognizeCustomFormsSampleAsync()
    model_id = None
    if os.getenv("CONTAINER_SAS_URL"):
        endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
        key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

        if not endpoint or not key:
            raise ValueError("Please provide endpoint and API key to run the samples.")

        form_training_client = FormTrainingClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )
        async with form_training_client:
            model = await (
                await form_training_client.begin_training(
                    os.getenv("CONTAINER_SAS_URL"), use_training_labels=True
                )
            ).result()
            model_id = model.model_id
        return await sample.recognize_custom_forms(model_id, filename)
