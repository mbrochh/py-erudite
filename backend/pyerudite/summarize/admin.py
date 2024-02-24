"""Admin classes for the summarize app."""

from django.contrib import admin
from django.utils.safestring import mark_safe

from . import models


class SummarizeFromIngestAdmin(admin.ModelAdmin):
    """Admin class for the SummarizeFromIngest model."""

    list_display = (
        "id",
        "status",
        "source_url",
        "source_title",
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
    raw_id_fields = ("ingest_obj",)
    readonly_fields = (
        "source_title",
        "source_url",
        "summary",
    )

    def source_title(self, obj):
        return obj.ingest_obj.title

    def source_url(self, obj):
        return mark_safe(
            f"<a href='{obj.ingest_obj.source_url}'>{obj.ingest_obj.source_url}</a>"
        )

    def summary(self, obj):
        with open(obj.summary_path.path, "r") as file:
            summary = file.read()
        return summary


admin.site.register(models.SummarizeFromIngest, SummarizeFromIngestAdmin)
