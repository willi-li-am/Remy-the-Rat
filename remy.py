import queue
import threading
import time
import os
from openai import OpenAI
import speech_recognition as sr
from dotenv import load_dotenv
import threading
import queue
from audio import AudioPlayer
from datetime import datetime
from pathlib import Path

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
        self.audio_player = AudioPlayer()
        self.handler_thread = None
        self.listener_thread = None
        self.transcribe_thread = None
        # Load environment variables from .env file
        load_dotenv()

        # Get OpenAI API key from environment variables
        self.api_key = os.getenv('OPENAI_API_KEY')

        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)
        self.start()

    def respondToCommand(self, response: str) -> None:
        """
        We want this to play response audio, move remy arms
        """
        print("response:", response)
        time = getTimeToRespond(response)
        audio_path = self.text_to_audio(response)
        print(audio_path)
        if audio_path:
            self.audio_player.play("./" + audio_path, should_delete=True)
        moveRemy(time)
        
    def sendCommand(self, command: str) -> None:
        """
        We want to send the voice command to chatgpt + video/photo for more context
        """
        print("command:", command)
        photo = takePhoto()
        response = self._remy_gpt(" ".join(self.context), command)
        self.context.append("Client: " + command)
        self.context.append("Remy: " + response)
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
                    self.audio_player.play("./chime.mp3")

                # Remove the temporary file
                os.remove("temp_audio.wav")

            except Exception as e:
                print(f"An error occurred: {str(e)}")

    def text_to_audio(self, text, subfolder="generated_audio"):
        # Create the full path to the subfolder
        subfolder_path = "./" + subfolder
        
        # Create the subfolder if it doesn't exist
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)

        # Define the file path for the audio output using a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        speech_file_path = subfolder_path + "/" + f"remy_gpt_output_audio_{timestamp}.mp3"

        # Generate speech using the Alloy voice with the GPT response
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="echo",
            input=text
        )

        # Save the speech to the file
        response.stream_to_file(speech_file_path)

        # Return the path to the generated audio file as a string
        return speech_file_path
    
    def start(self):
        self.handler_thread = threading.Thread(target=self.command_handler)
        self.listener_thread = threading.Thread(target=self.listen_audio)
        self.transcribe_thread = threading.Thread(target=self.transcribe_audio)
        self.handler_thread.start()
        self.listener_thread.start()
        self.transcribe_thread.start()

    def stop(self):
        print("Stopping...")
        self.command_queue.put(None) 
        self.audio_queue.put(None)
        self.listener_thread.join()
        self.transcribe_thread.join()
        self.handler_thread.join()

    def add(self, command):
        self.command_queue.put(command)

    def _remy_gpt(self, context, text):
        response = self.client.chat.completions.create(
            model="ft:gpt-3.5-turbo-1106:personal:remy:A7TF2xZK",
            messages=[
                {"role": "system", "content": "You are Remy the rat from Ratatouille. Guide users through this recipe: Smash 1 cucumber and cut into bite-sized pieces. Mix 1 teaspoon salt, 2 teaspoons sugar, 1 teaspoon sesame oil, 2 teaspoons soy sauce, and 1 tablespoon rice vinegar to make dressing. Toss cucumber with dressing, 3 chopped garlic cloves, and 1 teaspoon chili oil. Garnish with 1 tsp sesame seeds and cilantro. with step by step with concise responses."},
                {"role": "user", "content": "context: " + context + ". This is the new question I am asking: " + text}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()

if __name__ == '__main__':
    remy = None
    try:
        remy = Remy()
    except KeyboardInterrupt:
        remy.stop()
