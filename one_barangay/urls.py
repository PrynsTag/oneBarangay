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
from django.urls import include, path

urlpatterns = [
    path("barangay-admin/ocr/", include("ocr.urls")),
    path("", include("app.urls")),
    path("barangay-admin/dashboard", include("data_viz.urls")),
    path("", include("authentication.urls")),
    path("barangay-admin/user_management/", include("user_management.urls")),
    path("barangay-admin/user_profile/", include("user_profile.urls")),
    path("barangay-admin/announcement/", include("announcement.urls")),
    path("barangay-admin/bulk-sched/", include("bulk_sched.urls")),
    path("barangay-admin/complaint/", include("complaint.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    # path("barangay-admin/user-management", include("user-management.urls")),
]
