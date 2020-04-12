from django.urls import path

from core.views import *

urlpatterns = [
    path('packages/', PackageList.as_view(), name='package-list'),
    path('scrap_status/', ScrapView.as_view(), name='scrap_status'),
]
