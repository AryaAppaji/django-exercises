"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.contrib import admin
from django.urls import path
from firstapp import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/docs", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path("get-data/", views.get_data, name="get_data"),
    path("post-data/", views.post_data, name="post_data"),
    path("send-email/", views.send_email_to_user, name="send_email_to_user"),
    path("generate-qrcode/", views.generate_qrcode, name="generate_qrcode"),
    path("generate-barcode/", views.generate_barcode, name="generate_barcode"),
]
