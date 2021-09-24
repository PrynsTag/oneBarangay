"""Required File to Deploy to App Engine."""
import os

import uvicorn

from one_barangay import local_settings
from one_barangay.asgi import application

app = application

if __name__ == "__main__":
    os.environ["FIRESTORE_DATASET"] = "rbi"
    os.environ["FIRESTORE_EMULATOR_HOST"] = "127.0.0.1:8080"
    os.environ["FIRESTORE_EMULATOR_HOST_PATH"] = "127.0.0.1:8080/firestore"
    os.environ["FIRESTORE_HOST"] = "http://127.0.0.1:8080"
    os.environ["FIRESTORE_PROJECT_ID"] = "onebarangay-malanday"

    if os.getenv("GAE_ENV", "").startswith("standard"):
        # production
        uvicorn.run(
            "main:app",
            port=os.getenv("PORT"),
            host="127.0.0.1",
            workers=1,
        )
    else:
        local_settings.STATICFILES_STORAGE = (
            "storages.backends.gcloud.GoogleCloudStorage"
        )
        local_settings.DEFAULT_FILE_STORAGE = (
            "django.core.files.storage.FileSystemStorage"
        )
        local_settings.STATIC_URL = "https://storage.googleapis.com/{}/".format(
            local_settings.GS_STATIC_BUCKET_NAME
        )
        local_settings.MEDIA_URL = "https://storage.googleapis.com/{}/".format(
            local_settings.GS_MEDIA_BUCKET_NAME
        )

        uvicorn.run(
            "main:app",
            port=8000,
            reload=True,
            access_log=True,
            host="127.0.0.1",
            workers=4,
        )
