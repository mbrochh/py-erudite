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

INGEST_SOURCES = (("youtube", "Youtube"), ("webpage", "Webpage"))


class IngestFromSource(models.Model):
    """
    Model for storing the source from which the data is to be ingested.

    :status: The status of the ingest job.
    :source_type: The type of the source. For now only "youtube".
    :source_url: The URL of the source.
    :title: The title of the source (ie the title of the Youtube video).
    :authors: Comma separated list of authors of the source (ie the Youtube
      channel name and the names of people that speak in that video). NOTE:
      There should be no spaces after the commas, so that the list can be
      interpreted by the csv module. Example: `Author1,Author2,"Author3, Dr"`.
    :audio_path: The path to the audio file.
    :transcript_path: The path to the transcript file.
    :created_at: The time at which the source was added.

    """

    status = models.CharField(
        max_length=100, default="pending", choices=INGEST_STATUS
    )
    source_type = models.CharField(max_length=100, choices=INGEST_SOURCES)
    source_url = models.URLField()
    title = models.CharField(max_length=1024, blank=True)
    authors = models.CharField(max_length=1024, blank=True)
    audio_path = models.FileField(upload_to="ingest/audio/", blank=True)
    transcript_path = models.FileField(
        upload_to="ingest/transcripts/", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
