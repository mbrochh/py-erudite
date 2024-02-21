"""Services for the summarize app."""

import openai
from django.conf import settings

from pyerudite.utils import get_slugified_filename

from . import prompts, utils


def summarize_text(summarize_obj=None):
    """
    Summarize the text from an IngestFromSource object.

    :summarize_obj: The SummarizeFromIngest object.

    """
    text_path = summarize_obj.ingest_obj.transcript_path.path
    title = summarize_obj.ingest_obj.title
    chunks, total_token_count = utils.split_text(
        text_path=text_path, title=title
    )

    summaries = utils.summarize_chunks(chunks=chunks, title=title)

    filename, extension = get_slugified_filename(file_path=text_path)

    summarize_obj = utils.save_summaries(
        summarize_obj=summarize_obj,
        summaries=summaries,
        filename=filename,
    )
    return summarize_obj
