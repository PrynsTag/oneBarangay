"""Routing Request to Views of OCR."""
from django.http import HttpResponse
from django.template import loader


def ocr_pages(request):
    """Fetch OCR HTML Pages.

    Args:
      request: The requested URL.

    Returns:
      : The necessary OCR page requested in the URL.
    """
    # Pick out the html file name from the url. And load that templates.
    # ex. barangay-admin/ocr/file-upload = file-upload
    load_template = request.path.split("/")[-1]
    html_template = loader.get_template(load_template)

    return HttpResponse(html_template.render({"segment": load_template}, request))
