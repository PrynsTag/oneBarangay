"""Create your announcement forms here."""
from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.utils.text import slugify

from one_barangay.widgets import CkeditorWidget


class AnnouncementBaseForm(forms.Form):
    """Base form for announcement."""

    error_css_class = "is-invalid"
    required_css_class = "required"

    uid = forms.CharField(
        label="User I.D.",
        label_suffix="",
        widget=forms.TextInput(
            attrs={
                "readonly": True,
                "class": "form-control text-black",
            }
        ),
    )
    author = forms.CharField(
        label="Author",
        label_suffix="",
        widget=forms.TextInput(
            attrs={
                "readonly": True,
                "class": "form-control text-black",
            }
        ),
    )
    photo_url = forms.URLField(
        label="Profile Picture",
        label_suffix="",
        widget=forms.TextInput(
            attrs={
                "readonly": True,
                "class": "form-control text-black",
            }
        ),
    )
    title = forms.CharField(
        label="Title",
        max_length=150,
        min_length=5,
        label_suffix="",
        widget=forms.TextInput(attrs={"class": "form-control text-black"}),
    )

    thumbnail = forms.ImageField(
        required=False, widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )

    body = forms.CharField(widget=CkeditorWidget)

    OPTIONS = (
        ("covid-19", "COVID-19"),
        ("political", "Political"),
        ("environmental", "Environmental"),
    )
    categories = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(attrs={"class": "form-select"}), choices=OPTIONS
    )


class AnnouncementCreateForm(AnnouncementBaseForm):
    """Create form for announcement."""

    created = forms.DateTimeField(
        label="created",
        label_suffix="",
        widget=forms.DateTimeInput(attrs={"readonly": True, "class": "form-control text-black"}),
    )

    def __init__(self, *args, request, **kwargs):
        """Initialize AnnouncementCreateForm attributes."""
        super().__init__(*args, **kwargs)

        user_session = request.session.get("user")
        if user_session is not None:
            name = user_session.get("display_name")

            self.fields["author"].initial = name if name else user_session.get("first_name")
            self.fields["uid"].initial = user_session.get("uid")
            self.fields["photo_url"].initial = user_session.get("photo_url")

        self.fields["created"].initial = datetime.now()

    def clean(self):
        """Customize cleaning for form fields."""
        cleaned_data = super().clean()
        cleaned_data = {key: value for key, value in cleaned_data.items() if value}
        return cleaned_data

    def clean_date(self):
        """Clean date form field."""
        date = self.cleaned_data.get("date")

        if not date:
            date = datetime.now().strftime("%B %d, %Y %H:%M:%S")
        else:
            date = date.strftime("%B %d, %Y %H:%M:%S")

        return date

    def clean_title(self):
        """Clean title form field."""
        title = self.cleaned_data.get("title")

        if len(title) < 5:
            raise ValidationError("You need to have at least 5 characters for your title!")

        if not title:
            raise ValidationError("You need to supply a title for your announcement!")
        else:
            self.cleaned_data["announcement_id"] = slugify(title)

        return title

    def clean_thumbnail(self):
        """Clean thumbnail form field."""
        thumbnail = self.cleaned_data.get("thumbnail")
        announcement_id = self.cleaned_data.get("announcement_id")

        if thumbnail:
            if not thumbnail.content_type.startswith("image"):
                raise ValidationError("File is not image.")

            default_storage.save(announcement_id, thumbnail)
            thumbnail = default_storage.url(announcement_id)

        return thumbnail


class AnnouncementEditForm(AnnouncementCreateForm):
    """Edit form for announcement."""

    updated = forms.DateTimeField(
        label="updated",
        label_suffix="",
        widget=forms.DateTimeInput(attrs={"readonly": True, "class": "form-control text-black"}),
    )

    def __init__(self, *args, announcement, **kwargs):
        """Initialize AnnouncementEditForm attributes."""
        super().__init__(*args, **kwargs)

        self.fields["title"].initial = announcement["title"]
        self.fields["body"].initial = announcement["body"]
        self.fields["created"].initial = announcement["created"]
        self.fields["categories"].initial = announcement["categories"]
        self.fields["updated"].initial = datetime.now()
