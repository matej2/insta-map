"""insta_map URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import os

from django.conf.urls import url
from django.contrib import admin

from insta_map.views import infoView
from location.views import location_list
from photo.views import locationPhotoView, photo_list
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', locationPhotoView,name="location-photos"),
    path('info', infoView, name="info"),
    path('photos', photo_list, name="photos"),
    path('locations', location_list, name="photos")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
