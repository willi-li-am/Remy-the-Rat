import os
from openai import OpenAI
import speech_recognition as sr
from dotenv import load_dotenv
import threading
import queue

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Create a queue for audio chunks
audio_queue = queue.Queue()

def transcribe_audio():
    while True:
        audio_data = audio_queue.get()
        if audio_data is None:
            break

        try:
            # Save the audio to a temporary file
            with open("temp_audio.wav", "wb") as f:
                f.write(audio_data)
            
            # Open the temporary file and transcribe using Whisper
            with open("temp_audio.wav", "rb") as audio_file:
                response = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            
            text = response.text.lower()
            print("You said:", text)

            # Check for the target phrase
            if "what's up" in text:
                print("=======================")
                print("WHAT'S UP WAKE UP WORD!")
                print("=======================")

            # Remove the temporary file
            os.remove("temp_audio.wav")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

def listen_for_phrase_whisper():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Start the transcription thread
    transcribe_thread = threading.Thread(target=transcribe_audio)
    transcribe_thread.start()

    with microphone as source:
        print("Adjusting for ambient noise. Please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening for the phrase...")

        while True:
            try:
                # Listen for audio with a shorter phrase time limit
                audio = recognizer.listen(source, phrase_time_limit=2)
                
                # Add the audio data to the queue
                audio_queue.put(audio.get_wav_data())

            except sr.UnknownValueError:
                print("Could not understand audio")
            except KeyboardInterrupt:
                print("Stopping...")
                audio_queue.put(None)  # Signal the transcribe thread to stop
                transcribe_thread.join()
                break

if __name__ == "__main__":
    listen_for_phrase_whisper()