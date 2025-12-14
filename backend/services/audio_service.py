"""Audio Service - Text-to-speech and audio processing."""

from gtts import gTTS
from pydub import AudioSegment

from ..config import AUDIO_DIR


def text_to_audio(text: str, index: int, video_id: str) -> str:
    """Convert text to speech and save as audio file."""
    audio_path = AUDIO_DIR / f"audio_{video_id}_{index}.flac"
    
    if text and text.strip():
        tts = gTTS(text)
    else:
        tts = gTTS("The scene continues.")
    
    tts.save(str(audio_path))
    print(f"[text_to_audio] Saved: {audio_path}")
    return str(audio_path)


def get_audio_duration(index: int, video_id: str) -> float:
    """Get duration of audio file in seconds."""
    audio_path = AUDIO_DIR / f"audio_{video_id}_{index}.flac"
    audio = AudioSegment.from_file(str(audio_path))
    return len(audio) / 1000.0


def merge_audio_files(video_id: str, output_path: str):
    """Merge all audio files for a video."""
    audio_files = sorted(AUDIO_DIR.glob(f"audio_{video_id}_*.flac"))
    
    if not audio_files:
        raise ValueError("No audio files found")
    
    merged = AudioSegment.from_file(str(audio_files[0]))
    for af in audio_files[1:]:
        merged += AudioSegment.from_file(str(af))
    
    merged.export(output_path, format="mp3")
    print(f"[merge_audio_files] Created: {output_path}")
