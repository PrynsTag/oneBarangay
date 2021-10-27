"""Custom template tags."""
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
