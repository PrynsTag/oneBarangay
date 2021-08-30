"""oneBarangay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon/favicon.ico")),
    ),
    path(
        "humans.txt",
        TemplateView.as_view(
            template_name="main/humans.txt", content_type="text/plain"
        ),
    ),
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="main/robots.txt", content_type="text/plain"
        ),
    ),
    path("barangay-admin/", include("ocr.urls")),
    path("", include("app.urls")),
    # path("resident/", include("resident.urls")),
    # path("secretary/", include("secretary.urls")),
]
