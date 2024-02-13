"""
Management command to work off IngestFromSource objects with status `pending`.

"""

import os

from django.core.management.base import BaseCommand
from ingest.models import IngestFromSource
from ingest.utils import download_audio, transcribe_audio


class Command(BaseCommand):
    help = "Works off IngestFromSource objects with status `pending`."
    lock_file_path = "/artefacts/tmp/run_ingest.lock"

    def handle(self, *args, **options):
        """
        Handle the command.

        """
        if os.path.exists(self.lock_file_path):
            self.stdout.write(
                self.style.ERROR(f"Lock file `{self.lock_file_path}` exists.")
            )
            return

        try:
            with open(self.lock_file_path, "w") as lock_file:
                lock_file.write("locked")

            self._handle()

        finally:
            os.remove(self.lock_file_path)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Lock file `{self.lock_file_path}` removed."
                    " Process completed."
                )
            )

    def _handle(self):
        sources = IngestFromSource.objects.filter(status="pending")
        for source in sources:
            source.status = "in_progress"
            source.save()
            audio_path = download_audio(source.source_url, source.audio_path)
