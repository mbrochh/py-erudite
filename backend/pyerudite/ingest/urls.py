from django.urls import path

from .views import ingest_view

urlpatterns = [
    path('', ingest_view, name='ingest_view'),
]

