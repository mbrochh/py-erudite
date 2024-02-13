"""
Management command to work off SummarizeFromIngest objects with status `pending`.

"""

import os

from django.core.management.base import BaseCommand
from summarize.models import SummarizeFromIngest
from summarize.services import summarize_text


class Command(BaseCommand):
    help = "Works off SummarizeFromIngest objects with status `pending`."
    lock_file_path = "/artefacts/tmp/"
    lock_file_name = "get_summaries.lock"

    def handle(self, *args, **options):
        """
        Handle the command.

        """
        if not os.path.exists(self.lock_file_path):
            os.makedirs(self.lock_file_path)

        lockfile_path = os.path.join(self.lock_file_path, self.lock_file_name)

        if os.path.exists(lockfile_path):
            self.stdout.write(
                self.style.ERROR(f"Lock file `{lockfile_path}` exists.")
            )
            return

        try:
            with open(lockfile_path, "w") as lock_file:
                lock_file.write("locked")

            self._handle()

        finally:
            os.remove(lockfile_path)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Lock file `{lockfile_path}` removed."
                    " Process completed."
                )
            )

    def _handle(self):
        jobs = SummarizeFromIngest.objects.filter(status="pending")
        for job in jobs:
            summarize_text(summarize_obj=job)
