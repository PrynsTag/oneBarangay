"""Custom media widgets."""
from django import forms
from django.templatetags.static import static


class DatePickerWidget(forms.DateInput):
    """Datepicker custom widget."""

    class Media:
        """Media files for Datepicker widget."""

        css = {
            "all": (static("/assets/vendor/xdsoft-datepicker/dist/xdsoft-datepicker.min.css"),)
        }
        js = (
            static("/assets/vendor/jquery/dist/jquery.min.js"),
            static("/assets/vendor/xdsoft-datepicker/dist/xdsoft-datepicker.min.js"),
        )


class DropzoneWidget(forms.ClearableFileInput):
    """Dropzone drag-and-drop custom widget."""

    class Media:
        """Media files for Dropzone widget."""

        css = {
            "all": (
                static("/assets/vendor/dropzonejs/dist/dropzone.min.css"),
                static("/ocr/css/style.css"),
            ),
        }
        js = (
            static("/assets/vendor/dropzonejs/dist/dropzone.min.js"),
            static("/ocr/js/upload_file.js"),
        )
