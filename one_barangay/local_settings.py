"""Django settings for one_barangay project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import ast
import base64
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from google.oauth2 import service_account

from one_barangay.scripts.service_account import firestore_auth

load_dotenv()

# Decode credential to JSON
decoded_bytes = base64.b64decode(str(os.getenv("GOOGLE_STORAGE_CREDENTIALS")))
decoded_str = str(decoded_bytes, "utf-8")
GS_CREDENTIALS = service_account.Credentials.from_service_account_info(
    ast.literal_eval(decoded_str)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# For Logging
logger = logging.getLogger(__name__)

firebase_app = firestore_auth("local_settings")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost", os.getenv("APP_ENGINE_ALLOWED_HOST")]

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

# Application definition
INSTALLED_APPS = [
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "one_barangay",
    "app",
    "authentication",
    "ocr",
    "user_profile",
    "data_viz",
    "user_management",
    "announcement",
    "bulk_sched",
    "complaint",
    "ckeditor",
    "ckeditor_uploader",
    "appointment",
    "services",
    "crispy_forms",
    "crispy_bootstrap5",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [
            "redis://127.0.0.1:6379/1",
            "redis://127.0.0.1:6380/1",
        ],
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.ShardClient",
            "COMPRESSOR": "django_redis.compressors.lz4.Lz4Compressor",
            "PARSER_CLASS": "redis.connection.HiredisParser",
        },
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

# Static app dirs automatically finds it by AppDirectoriesFinder
# https://docs.djangoproject.com/en/3.1/ref/settings/#staticfiles-finders
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "frontend", "build"),
]

GS_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
GS_MEDIA_BUCKET_NAME = os.getenv("GS_MEDIA_BUCKET_NAME")
GS_STATIC_BUCKET_NAME = GS_PROJECT_ID
GS_BUCKET_NAME = GS_PROJECT_ID

if os.getenv("GAE_ENV", "").startswith("standard"):
    STATIC_URL = f"https://storage.googleapis.com/{GS_STATIC_BUCKET_NAME}/"
    MEDIA_URL = f"https://storage.googleapis.com/{GS_MEDIA_BUCKET_NAME}/"
    STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    DEFAULT_FILE_STORAGE = "one_barangay.scripts.storage_backends.GoogleCloudMediaStorage"

else:
    STATIC_URL = "/static/"
    MEDIA_URL = "http://127.0.0.1:9000/media/"  # Run ./simple_cors_server.py
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

GS_DEFAULT_ACL = "publicRead"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
