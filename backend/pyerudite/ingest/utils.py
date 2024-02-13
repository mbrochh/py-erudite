"""Utility functions for the ingest app."""

import datetime
import hashlib
import os

import yt_dlp
from django.conf import settings
from faster_whisper import WhisperModel

from pyerudite.utils import get_slugified_filename


def download_audio(
    video_url=None,
    audio_path=None,
):
    """
    Download audio from video.

    :video_url: URL of the video.
    :audio_path: Path to the folder that contains the audio files.

    :returns: Filename of the audio.

    """
    if audio_path is None:
        audio_path = os.path.join(settings.MEDIA_ROOT, "ingest/audio")

    filename = hashlib.sha256(video_url.encode()).hexdigest()
    outtmpl = os.path.join(audio_path, filename + ".%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        output_file_path = ydl.prepare_filename(info_dict)

    filename, extension = get_slugified_filename(output_file_path)
    new_file_path = os.path.join(audio_path, f"{filename}{extension}")
    os.rename(output_file_path, new_file_path)
    return new_file_path


def transcribe_audio(audio_file_path=None, transcripts_path=None):
    """
    Transcribe audio file using Whisper model.

    :audio_path: Path to read audio file.
    :transcript_path: Path to the transcripts folder.

    :returns: Filename of the transcript.

    """
    if transcripts_path is None:
        transcripts_path = os.path.join(
            settings.MEDIA_ROOT, "ingest/transcripts"
        )

    model_size = "base"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(audio_file_path, beam_size=5)
    transcript = []
    for segment in segments:
        transcript.append(segment.text)

    filename, extension = get_slugified_filename(audio_file_path)
    transcript_file_path = os.path.join(transcripts_path, f"{filename}.txt")

    if not os.path.exists(transcripts_path):
        os.makedirs(transcripts_path)

    with open(transcript_file_path, "w") as f:
        f.write("\n".join(transcript))

    return transcript_file_path
