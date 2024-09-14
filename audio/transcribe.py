from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=api_key)

# Create the 'generated_files' directory if it doesn't exist
output_dir = Path(__file__).parent / "generated_files"
output_dir.mkdir(exist_ok=True)

# Open the audio file for transcription
audio_file = open("files/60_seconds.mp3", "rb")

# Create transcription using Whisper
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
)

# Get the transcription text and prepare the text to speak
transcription_text = transcription.text
text_to_speak = "transcription test " + transcription_text

# Print the initial transcription
print("Initial Transcription:", transcription_text)

# Save the transcription to a file
transcription_file_path = output_dir / "transcription.txt"
with open(transcription_file_path, "w") as file:
    file.write(transcription_text)

# Path to save the speech file
speech_file_path = output_dir / "speech2.mp3"

# Create speech using the Alloy voice
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=text_to_speak
)

# Save the speech to the file using the correct method
response.stream_to_file(speech_file_path)

# Notify user of the saved file
print(f"Speech saved to: {speech_file_path}")
