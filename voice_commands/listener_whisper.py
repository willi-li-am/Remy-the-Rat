import os
from openai import OpenAI
import speech_recognition as sr
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def listen_for_phrase_whisper(target_phrase):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Adjusting for ambient noise. Please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening for the phrase...")

        while True:
            try:
                # Listen for audio
                audio = recognizer.listen(source)
                
                # Save the audio to a temporary file
                with open("temp_audio.wav", "wb") as f:
                    f.write(audio.get_wav_data())
                
                # Open the temporary file and transcribe using Whisper
                with open("temp_audio.wav", "rb") as audio_file:
                    response = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file
                    )
                
                text = response.text.lower()
                print("You said:", text)  # Print what was recognized

                if target_phrase.lower() in text:
                    print(f"You said {target_phrase}!")

                # Remove the temporary file
                os.remove("temp_audio.wav")

            except sr.UnknownValueError:
                print("Could not understand audio")
                continue
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                break

if __name__ == "__main__":
    listen_for_phrase_whisper("hey remy")

