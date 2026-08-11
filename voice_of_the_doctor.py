# Step1: Create API keys

# Step2: Create Client and send request
from deepgram import DeepgramClient
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DOCTOR_AUDIO = BASE_DIR / "doctor_response.mp3"
def convert_text_to_doctor_audio(text, output_filepath=DEFAULT_DOCTOR_AUDIO):
    from io import BytesIO
    from pydub import AudioSegment

    deepgram_api_key = os.environ.get("DEEPGRAM_API_KEY")

    if not deepgram_api_key:
        raise ValueError("Missing DEEPGRAM_API_KEY in .env")

    deepgram = DeepgramClient(api_key=deepgram_api_key)

    # Deepgram allows a maximum of 2000 characters per request.
    max_chars = 1900

    # Split the response into chunks without cutting words.
    chunks = []
    remaining_text = text.strip()

    while len(remaining_text) > max_chars:
        split_at = remaining_text.rfind(" ", 0, max_chars)

        if split_at == -1:
            split_at = max_chars

        chunks.append(remaining_text[:split_at].strip())
        remaining_text = remaining_text[split_at:].strip()

    if remaining_text:
        chunks.append(remaining_text)

    # Generate audio for each chunk.
    combined_audio = AudioSegment.empty()

    for chunk in chunks:
        audio = deepgram.speak.v1.audio.generate(
            text=chunk,
            model=os.environ.get("DEEPGRAM_TTS_MODEL", "aura-2-thalia-en"),
            encoding="mp3",
        )

        audio_bytes = b"".join(audio)

        chunk_audio = AudioSegment.from_file(
            BytesIO(audio_bytes),
            format="mp3"
        )

        combined_audio += chunk_audio

    # Save the final combined audio.
    output_filepath = Path(output_filepath)

    combined_audio.export(
        output_filepath,
        format="mp3"
    )

    return output_filepath

import subprocess
import platform
def play_audio(audio_filepath):
    audio_filepath = str(audio_filepath)

    if platform.system() == "Darwin":
        subprocess.run(["afplay", audio_filepath], check=False)
    elif platform.system() == "Windows":
        os.startfile(audio_filepath)
    else:
        subprocess.run(["xdg-open", audio_filepath], check=False)


"""text = "Hi, my name is AI with Hassan, who are you?. I am very happy."
api_key = os.environ.get("DEEPGRAM_API_KEY")
deepgram = DeepgramClient(api_key=api_key)
audio = deepgram.speak.v1.audio.generate(
    text=text,
    model="aura-2-thalia-en",
    encoding="mp3",
)
# Step3: Save audio
from pathlib import Path

audio_file="test-output.mp3"
audio_path = Path(__file__).with_name(audio_file)
with audio_path.open("wb") as file:
    for chunk in audio:
        file.write(chunk)

# Step4: Play audio
import platform
import subprocess


if platform.system() == "Darwin":  # macOS
    subprocess.run(["afplay", str(audio_path)])
elif platform.system() == "Windows":
    os.startfile(audio_path)
else:  # Linux
    subprocess.run(["xdg-open", str(audio_path)])"""


