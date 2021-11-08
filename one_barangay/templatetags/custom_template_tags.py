"""Custom template tags."""
import re

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def replace_single_quotes(quoted_string):
    """Replace single quote to double quote in string.

    Args:
      quoted_string: The single quoted string to replace.

    Returns:
      The double quoted string.
    """
    return quoted_string.replace("'", '"')


@register.filter
def get_item(dictionary, key):
    """Get key in dictionary.

    Args:
      dictionary: The dictionary you want to get the value.
      key: The key of the dictionary you want to get the value.

    Returns:
      The dictionary value.
    """
    return round(float(dictionary.get(key)) * 100, 2) if dictionary.get(key) else 0.0


@register.filter
@stringfilter
def get_formset_field_name(field_name):
    """Get the field name of a formset.

    Args:
      field_name: The formset field name you want to extract

    Returns:
      The extracted field name without prefix.
    """
    return re.sub(r"form-\d+-", "", field_name)
