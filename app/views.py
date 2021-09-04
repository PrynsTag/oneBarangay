"""Create your App views here."""
from django.http import HttpResponse
from django.template import loader


def index(request):
    """Fetch index.html for App.

    Args:
      request: The URL Request.

    Returns:
      The index.html of App.
    """
    html_template = loader.get_template("index.html")

    return HttpResponse(html_template.render({"segment": "index"}, request))


def pages(request):
    """Fetch Pages other than index.html.

    Args:
      request: The URL Request.

    Returns:
      The requested HTML File.
    """
    # Pick out the html file name from the url. And load that templates.
    # ex. barangay-admin/ocr/file-upload = file-upload
    load_template = request.path.split("/")[-1]
    html_template = loader.get_template(load_template)

    return HttpResponse(html_template.render({"segment": load_template}, request))
