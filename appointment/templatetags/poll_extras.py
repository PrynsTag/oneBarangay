"""Appointment poll extras."""
import json

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="js")
def js(obj):
    """Convert django template data into javascript.

    Args:
      obj: Data in object

    Returns:
        Javascript data format.
    """
    return mark_safe(json.dumps(obj))
