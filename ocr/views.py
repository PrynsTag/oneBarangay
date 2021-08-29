# Create your views here.
from django.http import HttpResponse
from django.template import loader


def index(request):
    return HttpResponse("hello")


def ocr(request):
    context = {}
    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split("/")[-1]
    context["segment"] = load_template

    html_template = loader.get_template(load_template)
    return HttpResponse(html_template.render(context, request))
