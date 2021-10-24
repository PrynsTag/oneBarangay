"""Django settings for one_barangay project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import io
import os
from pathlib import Path

import sentry_sdk
from dotenv import load_dotenv
from google.cloud import secretmanager
from sentry_sdk.integrations.django import DjangoIntegration

from one_barangay.scripts.service_account import firestore_auth, gcloud_auth

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env_file = os.path.join(BASE_DIR, ".env")

if os.path.isfile(env_file):
    # Use a local secret file, if provided
    load_dotenv(env_file)

elif os.environ.get("GOOGLE_PROJECT_ID", None):  # noqa: SIM106
    # Pull secrets from Secret Manager
    project_id = os.environ.get("SECRET_MANAGER_PROJECT_ID")
    settings_name = os.environ.get("SETTINGS_NAME")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"

    client = secretmanager.SecretManagerServiceClient()
    payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

    load_dotenv(stream=io.StringIO(payload))
else:
    raise Exception("No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found.")

firebase_app = firestore_auth("settings")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", os.getenv("APP_ENGINE_ALLOWED_HOST")]

SESSION_ENGINE = "django.contrib.sessions.backends.file"

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

# Application definition
INSTALLED_APPS = [
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "one_barangay",
    "app",
    "authentication",
    "appointment",
    "ocr",
    "user_profile",
    "services",
    "django.contrib.sessions",
    "data_viz",
    "user_management",
    "announcement",
    "bulk_sched",
    "complaint",
    "ckeditor",
    "ckeditor_uploader",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

LOGGING_CONFIG = None

ROOT_URLCONF = "one_barangay.urls"
TEMPLATE_DIR = os.path.join(BASE_DIR, "one_barangay", "templates")  # ROOT dir for templates

# EMAIL API https://docs.sendgrid.com/for-developers/sending-email/django
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = "apikey"  # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = os.getenv("SENDGRID_API_KEY")
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# CKEDITOR WYSIWYG Text Editor https://github.com/django-ckeditor/django-ckeditor
CKEDITOR_BASEPATH = "/ckeditor/ckeditor/"
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_RESTRICT_BY_DATE = True
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_FORCE_JPEG_COMPRESSION = True
CKEDITOR_IMAGE_QUALITY = 90
CKEDITOR_UPLOAD_PATH = "media/"
CKEDITOR_JQUERY_URL = "https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js"

CKEDITOR_CONFIGS = {
    "default": {
        "skin": "moono",
        # "skin": "office2013",
        "toolbar_Basic": [["Source", "-", "Bold", "Italic"]],
        "toolbar_YourCustomToolbarConfig": [
            {
                "name": "document",
                "items": ["Source", "-", "Save", "NewPage", "Preview", "Print", "-", "Templates"],
            },
            {
                "name": "clipboard",
                "items": [
                    "Cut",
                    "Copy",
                    "Paste",
                    "PasteText",
                    "PasteFromWord",
                    "-",
                    "Undo",
                    "Redo",
                ],
            },
            {"name": "editing", "items": ["Find", "Replace", "-", "SelectAll"]},
            {
                "name": "forms",
                "items": [
                    "Form",
                    "Checkbox",
                    "Radio",
                    "TextField",
                    "Textarea",
                    "Select",
                    "Button",
                    "ImageButton",
                    "HiddenField",
                ],
            },
            "/",
            {
                "name": "basicstyles",
                "items": [
                    "Bold",
                    "Italic",
                    "Underline",
                    "Strike",
                    "Subscript",
                    "Superscript",
                    "-",
                    "RemoveFormat",
                ],
            },
            {
                "name": "paragraph",
                "items": [
                    "NumberedList",
                    "BulletedList",
                    "-",
                    "Outdent",
                    "Indent",
                    "-",
                    "Blockquote",
                    "CreateDiv",
                    "-",
                    "JustifyLeft",
                    "JustifyCenter",
                    "JustifyRight",
                    "JustifyBlock",
                    "-",
                    "BidiLtr",
                    "BidiRtl",
                    "Language",
                ],
            },
            {"name": "links", "items": ["Link", "Unlink", "Anchor"]},
            {
                "name": "insert",
                "items": [
                    "Image",
                    "Flash",
                    "Table",
                    "HorizontalRule",
                    "Smiley",
                    "SpecialChar",
                    "PageBreak",
                    "Iframe",
                ],
            },
            "/",
            {"name": "styles", "items": ["Styles", "Format", "Font", "FontSize"]},
            {"name": "colors", "items": ["TextColor", "BGColor"]},
            {"name": "tools", "items": ["Maximize", "ShowBlocks"]},
            {"name": "about", "items": ["About"]},
            "/",  # put this to force next toolbar on new line
            {
                "name": "yourcustomtools",
                "items": [
                    # put the name of your editor.ui.addButton here
                    "Preview",
                    "Maximize",
                ],
            },
        ],
        "toolbar": "YourCustomToolbarConfig",  # put selected toolbar config here
        "toolbarGroups": [{"name": "document", "groups": ["mode", "document", "doctools"]}],
        "height": 291,
        "width": "100%",
        "filebrowserWindowHeight": 725,
        "filebrowserWindowWidth": 940,
        "toolbarCanCollapse": True,
        "mathJaxLib": "//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML",
        "removePlugins": "exportpdf",
        "tabSpaces": 4,
        "extraPlugins": ",".join(
            [
                "uploadimage",  # the upload image feature
                # your extra plugins here
                "div",
                "autolink",
                "autoembed",
                "embedsemantic",
                "autogrow",
                "devtools",
                "widget",
                "lineutils",
                "ajax",
                "clipboard",
                "dialog",
                "dialogui",
                "elementspath",
            ]
        ),
    }
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "one_barangay.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Manila"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "one_barangay", "static"),
    os.path.join(BASE_DIR, "authentication", "static"),
    os.path.join(BASE_DIR, "ocr", "static"),
    os.path.join(BASE_DIR, "services", "static"),
    os.path.join(BASE_DIR, "data_viz", "static"),
    os.path.join(BASE_DIR, "user_profile", "static"),
    os.path.join(BASE_DIR, "user_management", "static"),
    os.path.join(BASE_DIR, "announcement", "static"),
    os.path.join(BASE_DIR, "bulk_sched", "static"),
    os.path.join(BASE_DIR, "complaint", "static"),
]

STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
DEFAULT_FILE_STORAGE = "one_barangay.scripts.storage_backends.GoogleCloudMediaStorage"

GS_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
GS_CREDENTIALS = gcloud_auth()

GS_MEDIA_BUCKET_NAME = os.getenv("GS_MEDIA_BUCKET_NAME")
GS_STATIC_BUCKET_NAME = os.getenv("GS_STATIC_BUCKET_NAME")
GS_BUCKET_NAME = GS_PROJECT_ID

STATIC_URL = f"https://storage.googleapis.com/{GS_STATIC_BUCKET_NAME}/"
MEDIA_URL = f"https://storage.googleapis.com/{GS_MEDIA_BUCKET_NAME}/"

GS_DEFAULT_ACL = "publicRead"
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Sentry SDK
sentry_sdk.init(  # Proper Sentry Declaration pylint: disable=abstract-class-instantiated
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)
