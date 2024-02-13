"""Admin classes for the summarize app."""

from django.contrib import admin

from . import models


class SummarizeFromIngestAdmin(admin.ModelAdmin):
    """Admin class for the SummarizeFromIngest model."""

    list_display = (
        "status",
        "input_tokens",
        "output_tokens",
        "input_cost",
        "output_cost",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = (
        "ingest_obj__source_url",
        "ingest_obj__title",
        "ingest_obj__authors",
    )


admin.site.register(models.SummarizeFromIngest, SummarizeFromIngestAdmin)
