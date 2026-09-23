import requests


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "qwen2.5:3b"


def get_response(user_text, conversation_history=None):

    prompt = f"""
You are a friendly voice companion for an elderly person.

Be warm, patient and conversational.
Use simple language.
Do not give complicated or very long answers.

The user said:
{user_text}

Reply naturally as their companion.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    return response.json()["response"].strip()