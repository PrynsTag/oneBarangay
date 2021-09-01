from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def add(request):
    return render(request, "bulk_sched/add_bulk.html")


# def add(response):
#     return HttpResponse("HIII")
