from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from ai.tts import text_to_speech
from fastapi.responses import FileResponse
from pathlib import Path
import tempfile

from ai.stt import speech_to_text
from ai.llm import get_response

app = FastAPI(title="Elderly Voice Companion")
app.mount("/audio", StaticFiles(directory="frontend/audio"), name="audio")

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND = BASE_DIR / "frontend" / "index.html"


@app.get("/")
def home():
    return FileResponse(FRONTEND)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/speech")
async def speech(file: UploadFile = File(...)):

    audio_data = await file.read()

    with tempfile.NamedTemporaryFile(
        suffix=".webm",
        delete=False
    ) as temp:

        temp.write(audio_data)
        audio_path = temp.name

    # Speech → Text
    user_text = speech_to_text(audio_path)

    # Text → AI Response
    ai_response = get_response(user_text)

    # AI Response → Speech
    audio_url = await text_to_speech(ai_response)

    return {
        "text": user_text,
        "response": ai_response,
        "audio": audio_url
    }