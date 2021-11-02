from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from WhatToEatToday import settings
from core.views import *

urlpatterns = [
    path('scrap/', ScrapView.as_view(),  name='scrap'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)