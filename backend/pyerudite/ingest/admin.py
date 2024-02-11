"""Admin classes for the ingest app."""

from django.contrib import admin

from . import models


class IngestFromSourceAdmin(admin.ModelAdmin):
    """Admin class for the IngestFromSource model."""

    list_display = (
        "id",
        "status",
        "source_type",
        "source_url",
        "title",
        "authors",
        "created_at",
    )
    list_filter = ("status", "source_type")
    search_fields = ("source_url", "title", "authors")


admin.site.register(models.IngestFromSource, IngestFromSourceAdmin)
