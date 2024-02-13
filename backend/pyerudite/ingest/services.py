"""Services for the ingest app."""

from . import utils


def summarize_video(ingest_obj):
    """
    Summarize the video.

    :ingest_obj: The IngestFromSource object.

    :returns: The updated IngestFromSource object.

    """
    ingest_obj.status = "in_progress"
    ingest_obj.save()

    video_url = ingest_obj.source_url
    audio_file_path = utils.download_audio(video_url=video_url)

    ingest_obj.audio_path = audio_file_path
    ingest_obj.save()

    transcript_file_path = utils.transcribe_audio(
        audio_file_path=audio_file_path
    )
    ingest_obj.transcript_path = transcript_file_path
    ingest_obj.save()

    ingest_obj.status = "completed"
    ingest_obj.save()

    return ingest_obj
