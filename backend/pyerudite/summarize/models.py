"""Models for the summarize app."""

from django.db import models

SUMMARY_STATUS = (
    ("pending", "Pending"),
    ("in_progress", "In Progress"),
    ("completed", "Completed"),
    ("failed", "Failed"),
    ("cancelled", "Cancelled"),
)


class SummarizeFromIngest(models.Model):
    """
    A model for summarizing text from an IngestFromSource object.

    :ingest_obj: The IngestFromSource object.
    :summary: The summary file.
    :created_at: The time at which the summary was created.

    """

    status = models.CharField(
        max_length=100, default="pending", choices=SUMMARY_STATUS
    )
    ingest_obj = models.ForeignKey(
        "ingest.IngestFromSource",
        on_delete=models.CASCADE,
        related_name="summaries",
    )
    summary_path = models.FileField(upload_to="summarize/summaries")
    input_tokens = models.IntegerField(blank=True, null=True)
    output_tokens = models.IntegerField(blank=True, null=True)
    input_cost = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    output_cost = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
