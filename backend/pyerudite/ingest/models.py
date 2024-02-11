"""
Models for the ingest app.

"""

from django.db import models

INGEST_STATUS = (
    ("pending", "Pending"),
    ("in_progress", "In Progress"),
    ("completed", "Completed"),
    ("failed", "Failed"),
    ("cancelled", "Cancelled"),
)

INGEST_SOURCES = (("youtube", "Youtube"),)


class IngestFromSource(models.Model):
    """
    Model for storing the source from which the data is to be ingested.

    :status: The status of the ingest job.
    :source_type: The type of the source. For now only "youtube".
    :source_url: The URL of the source.
    :created_at: The time at which the source was added.

    """

    status = models.CharField(
        max_length=100, default="pending", choices=INGEST_STATUS
    )
    source_type = models.CharField(max_length=100, choices=INGEST_SOURCES)
    source_url = models.URLField()
    title = models.CharField(max_length=1024)
    authors = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
