from faster_whisper import WhisperModel

def transcribe_audio(audio_path, transcript_path):
    """
    Transcribe audio file using Whisper model.

    :audio_path: Path to read audio file.
    :transcript_path: Path to save transcript.

    :returns: Filename of the transcript.

    """
    model_size = "base"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(audio_path, beam_size=5)
    transcript = []
    for segment in segments:
        transcript.append(segment.text)
    
    with open(transcript_path, "w") as f:
        f.write(" ".join(transcript))

    return transcript_path