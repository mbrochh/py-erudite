"""
Management command to set IngestFromSource objects with status `in_progress`
back to `pending`.

This is needed when the container was stopped while the ingest process was
running so that these aborted jobs get queued again.

"""

import os

from django.core.management.base import BaseCommand
from ingest.models import IngestFromSource

from pyerudite.utils import timestamp


class Command(BaseCommand):
    help = (
        "Reset IngestFromSource objects with status `in_progress` back to"
        " `pending`."
    )

    def handle(self, *args, **options):
        """
        Handle the command.

        """
        self.stdout.write(
            f"{timestamp()} -"
             " Resetting in_progress IngestFromSource objects."
        )
        IngestFromSource.objects.filter(status="in_progress").update(
            status="pending"
        )
