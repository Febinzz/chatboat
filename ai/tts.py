import edge_tts
import uuid
from pathlib import Path


AUDIO_DIR = Path("frontend/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


async def text_to_speech(text):
    filename = f"{uuid.uuid4()}.mp3"
    output_path = AUDIO_DIR / filename

    voice = "en-US-AriaNeural"

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(output_path))

    return f"/audio/{filename}"