"""Admin classes for the summarize app."""

from django.contrib import admin
from django.template.defaultfilters import linebreaksbr
from django.utils.safestring import mark_safe

from pyerudite.utils import clean_title

from . import models, utils


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
            lines = file.readlines()

        authors_list = utils.get_authors_list(obj.ingest_obj.authors)
        title = clean_title(obj.ingest_obj.title)

        token_count = obj.input_tokens or 0 + obj.output_tokens or 0
        cost = obj.input_cost or 0 + obj.output_cost or 0
        result = f"Summarized [[{title}]]<br /><br />"
        result += "<textarea style='width:100%; height:300px;'>\n"
        result += f"---\n"
        result += f"source: {obj.ingest_obj.source_url}\n"
        if authors_list:
            result += f"authors:\n"
            for author in authors_list:
                result += f'  - "[[{author}]]"\n'
        result += f"gpt-token-count: {token_count}\n"
        result += f"summary-cost: {cost}\n"
        result += "second-brain: true\n"
        result += f"---\n"
        result += "\n"
        result += "# Summary\n"
        for line in lines:
            result += f"{line}"
        result += "</textarea>"
        return mark_safe(result)


admin.site.register(models.SummarizeFromIngest, SummarizeFromIngestAdmin)
