"""one_barangay URL Configuration.

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
from django.conf.urls import url
from django.urls import include, path
from django.views.decorators.cache import cache_control
from django.views.generic import TemplateView

urlpatterns = [
    path("ocr/", include("ocr.urls")),
    path("", include("app.urls")),
    path("dashboard", include("data_viz.urls")),
    path("", include("authentication.urls")),
    path("user_management/", include("user_management.urls")),
    path("user_profile/", include("user_profile.urls")),
    path("announcement/", include("announcement.urls")),
    path("bulk-sched/", include("bulk_sched.urls")),
    path("complaint/", include("complaint.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    url(
        r"^service-worker.js",
        cache_control(max_age=2592000)(
            TemplateView.as_view(
                template_name="service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    path("appointment/", include("appointment.urls")),
    url(
        r"^firebase-messaging-sw.js",
        cache_control(max_age=2592000)(
            TemplateView.as_view(
                template_name="firebase-messaging-sw.js",
                content_type="application/javascript",
            )
        ),
        name="firebase-messaging-sw.js",
    ),
    path("api/", include("api.urls")),
]
