# Create your views here.
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader


def index(request):
    context = {}
    context["segment"] = "index"

    html_template = loader.get_template("index.html")
    return HttpResponse(html_template.render(context, request))


def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split("/")[-1]
    context["segment"] = load_template

    html_template = loader.get_template(load_template)
    return HttpResponse(html_template.render(context, request))
