# speech_to_text_translate.py
import requests
import json
from config import SAARAS_API_KEY

def speech_to_text_translate(audio_file_path, source_language="ml-IN", target_language="en-IN"):
    url = "https://api.sarvam.ai/speech-to-text-translate"  # Updated to match your log
    headers = {"API-Subscription-Key": SAARAS_API_KEY}

    try:
        with open(audio_file_path, "rb") as f:
            audio_bytes = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    data = {
        "source_language": source_language,
        "target_language": target_language,
        "model": "saaras:v1",
        "translate" : True
    }

    # Ensure the file is correctly included in the files parameter
    files = {
        "file": (audio_file_path, open(audio_file_path, "rb"), "audio/wav")
    }

    try:
            response = requests.post(url, headers=headers, data=data, files=files)
            response.raise_for_status()  # Ensure the request was successful
            result = response.json()
            transcript = result.get("transcript", "")
            if not transcript:
                print("No transcript found in response")
                return None
            return transcript
    except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None