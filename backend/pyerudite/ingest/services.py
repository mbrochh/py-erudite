"""Services for the ingest app."""

from summarize.models import SummarizeFromIngest

from . import utils


def fetch_webpage(ingest_obj):
    """
    Fetches a webpage and creates a SummarizeFromIngest object.

    :ingest_obj: The IngestFromSource object.

    :returns: The updated IngestFromSource object.

    """
    ingest_obj.status = "in_progress"
    ingest_obj.save()

    webpage_url = ingest_obj.source_url
    transcript_file_path = utils.extract_text_from_webpage(
        webpage_url=webpage_url
    )
    ingest_obj.transcript_path = transcript_file_path
    ingest_obj.status = "completed"
    ingest_obj.save()

    SummarizeFromIngest.objects.create(ingest_obj=ingest_obj)

    return ingest_obj


def transcribe_video(ingest_obj):
    """
    Transcribes a video and creates a SummarizeFromIngest object.

    :ingest_obj: The IngestFromSource object.

    :returns: The updated IngestFromSource object.

    """
    ingest_obj.status = "in_progress"
    ingest_obj.save()

    video_url = ingest_obj.source_url
    audio_file_path, title = utils.download_audio(video_url=video_url)
    ingest_obj.title = title
    ingest_obj.audio_path = audio_file_path
    ingest_obj.save()

    transcript_file_path = utils.transcribe_audio(
        audio_file_path=audio_file_path
    )
    ingest_obj.transcript_path = transcript_file_path
    ingest_obj.save()

    ingest_obj.status = "completed"
    ingest_obj.save()

    SummarizeFromIngest.objects.create(ingest_obj=ingest_obj)

    return ingest_obj
