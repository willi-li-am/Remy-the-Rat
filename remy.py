import queue
import threading
import time
import os
from openai import OpenAI
import speech_recognition as sr
from dotenv import load_dotenv
import threading
import queue

def takePhoto(): pass
def askChatGPT(context, command, photo): pass
def replayAudio(audio_path): pass
def getTimeToRespond(audio_path): pass
def moveRemy(audio_length): pass

class Remy():
    def __init__(self) -> None:
        self.context = [] # TODO: make a function that turns context into a string of User and Remy
        self.command_queue = queue.Queue()
        self.audio_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.question_event = threading.Event()
        self.handler_thread = None
        # Load environment variables from .env file
        load_dotenv()

        # Get OpenAI API key from environment variables
        self.api_key = os.getenv('OPENAI_API_KEY')

        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)

    def respondToCommand(self, response: str) -> None:
        """
        We want this to play response audio, move remy arms
        """
        time = getTimeToRespond(response)
        replayAudio(response)
        moveRemy(time)
        

    def sendCommand(self, command: str) -> None:
        """
        We want to send the voice command to chatgpt + video/photo for more context
        """
        print("command:", command)
        self.context.append(command)
        photo = takePhoto()
        response = askChatGPT(self.context, command, photo)
        self.context.append(response)
        self.respondToCommand(response)

    def command_handler(self):
        """Listen for commands and process them. Stop when signaled."""

        while True:
            command = self.command_queue.get()
            if command is None:  # 'None' signals the thread to stop
                print("Received stop signal.")
                break

            # Process the command
            if command:
                self.sendCommand(command)

    def listen_audio(self):
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        with microphone as source:
            print("Adjusting for ambient noise. Please wait...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening for the phrase...")

            while True:
                try:
                    # Listen for audio with a shorter phrase time limit
                    audio = recognizer.listen(source, phrase_time_limit=5)
                    
                    # Add the audio data to the queue
                    self.audio_queue.put(audio.get_wav_data())

                except sr.UnknownValueError:
                    print("Could not understand audio")
                except KeyboardInterrupt:
                    print("Stopping...")
                    self.audio_queue.put(None)  # Signal the transcribe thread to stop
                    self.transcribe_thread.join()
                    break

    def transcribe_audio(self):
        while True:
            audio_data = self.audio_queue.get()
            if audio_data is None:
                break

            try:
                # Save the audio to a temporary file
                with open("temp_audio.wav", "wb") as f:
                    f.write(audio_data)

                # Open the temporary file and transcribe using Whisper
                with open("temp_audio.wav", "rb") as audio_file:
                    response = self.client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file
                    )
                
                text = response.text.lower()
                print(text)

                if (self.question_event.is_set()):
                    self.question_event.clear()
                    self.command_queue.put(text)
                    
                # Check for the target phrase
                if "what's up" in text:
                    self.question_event.set()
                    # play DA DING

                # Remove the temporary file
                os.remove("temp_audio.wav")

            except Exception as e:
                print(f"An error occurred: {str(e)}")

    
    def start(self):
        try:
            self.handler_thread = threading.Thread(target=self.command_handler)
            self.listener_thread = threading.Thread(target=self.listen_audio)
            self.transcribe_thread = threading.Thread(target=self.transcribe_audio)
            self.handler_thread.start()
            self.listener_thread.start()
            self.transcribe_thread.start()
        except KeyboardInterrupt:
            print("Stopping...")
            self.command_queue.put(None) 
            self.audio_queue.put(None)
            self.listener_thread.join()
            self.transcribe_thread.join()
            self.handler_thread.join()
            return  

    def add(self, command):
        self.command_queue.put(command)

if __name__ == '__main__':
    remy = Remy()
    remy.start()
