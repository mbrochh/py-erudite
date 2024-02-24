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
    readonly_fields = ("transcript",)

    def transcript(self, obj):
        with open(obj.transcript_path.path, "r") as file:
            transcript = file.read()
        return transcript


admin.site.register(models.IngestFromSource, IngestFromSourceAdmin)
