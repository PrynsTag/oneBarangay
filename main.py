"""Required File to Deploy to App Engine."""
import os

import uvicorn

from one_barangay.asgi import application

app = application

if __name__ == "__main__":
    os.environ["FIRESTORE_DATASET"] = "rbi"
    os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8000"
    os.environ["FIRESTORE_EMULATOR_HOST_PATH"] = "localhost:8000/firestore"
    os.environ["FIRESTORE_HOST"] = "http://localhost:8000"
    os.environ["FIRESTORE_PROJECT_ID"] = "onebarangay-malanday"

    if os.getenv("GAE_ENV", "").startswith("standard"):
        # production
        uvicorn.run(
            app,
            port=os.getenv("PORT"),
            host="127.0.0.1",
            workers=1,
        )
    else:
        uvicorn.run(
            "main:app",
            port=8000,
            reload=True,
            access_log=False,
            host="127.0.0.1",
            workers=1,
        )
