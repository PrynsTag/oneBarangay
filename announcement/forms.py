"""Create your announcement forms here."""
from datetime import datetime

import pytz
from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from one_barangay.widgets import CkeditorWidget

FEATURED_CHOICES = (
    (True, "Featured"),
    (False, "Not Featured"),
)

CATEGORIES_OPTIONS = (
    ("covid-19", "COVID-19"),
    ("political", "Political"),
    ("environmental", "Environmental"),
)


class AnnouncementBaseForm(forms.Form):
    """Base form for announcement."""

    error_css_class = "is-invalid"
    required_css_class = "required"

    user_id = forms.CharField(
        label="User I.D.",
        label_suffix="",
        widget=forms.HiddenInput(
            attrs={
                "readonly": True,
                "class": "form-control text-black",
            }
        ),
    )
    author = forms.CharField(
        label="Author",
        label_suffix="",
        widget=forms.HiddenInput(
            attrs={
                "readonly": True,
                "class": "form-control text-black",
            }
        ),
    )
    photo_url = forms.URLField(
        label="Profile Picture",
        label_suffix="",
        widget=forms.HiddenInput(
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

    categories = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(attrs={"class": "form-select"}), choices=CATEGORIES_OPTIONS
    )

    featured = forms.ChoiceField(
        label_suffix="",
        initial=False,
        widget=forms.RadioSelect(attrs={"class": "form-checkbox list-unstyled"}),
        choices=FEATURED_CHOICES,
    )


class AnnouncementCreateForm(AnnouncementBaseForm):
    """Create form for announcement."""

    creation_date = forms.DateTimeField(
        label_suffix="",
        widget=forms.HiddenInput(attrs={"readonly": True, "class": "form-control text-black"}),
    )

    def __init__(self, *args, request, **kwargs):
        """Initialize AnnouncementCreateForm attributes."""
        super().__init__(*args, **kwargs)

        user_session = request.session.get("user")
        if user_session is not None:
            name = user_session.get("display_name")

            self.fields["author"].initial = name if name else user_session.get("first_name")
            self.fields["user_id"].initial = user_session.get("user_id")
            self.fields["photo_url"].initial = user_session.get("photo_url")

        self.fields["creation_date"].initial = datetime.now(tz=pytz.timezone("Asia/Manila"))

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

        if thumbnail is None:
            raise ValidationError("This field is required!")
        else:
            if not thumbnail.content_type.startswith("image"):
                raise ValidationError("File is not image.")

        return thumbnail


class AnnouncementEditForm(AnnouncementCreateForm):
    """Edit form for announcement."""

    updated = forms.DateTimeField(
        label="updated",
        label_suffix="",
        widget=forms.HiddenInput(attrs={"readonly": True, "class": "form-control text-black"}),
    )
    thumbnail_name = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, announcement, **kwargs):
        """Initialize AnnouncementEditForm attributes."""
        super().__init__(*args, **kwargs)

        self.fields["title"].initial = announcement["title"]
        self.fields["body"].initial = announcement["body"]
        self.fields["creation_date"].initial = announcement["creation_date"]
        self.fields["categories"].initial = announcement["categories"]
        self.fields["featured"].initial = announcement["featured"]
        self.fields["thumbnail_name"].initial = announcement["thumbnail_name"]
        self.fields["updated"].initial = datetime.now()
