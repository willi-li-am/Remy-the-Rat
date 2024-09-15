from flask import Flask
from flask_socketio import SocketIO
import queue
import threading
import os
from openai import OpenAI
import speech_recognition as sr
from dotenv import load_dotenv
from datetime import datetime
from audio import AudioPlayer
from video import VideoPlayer
from robot import move_robot

def takePhoto(): pass
def askChatGPT(context, command, photo): pass
def replayAudio(audio_path): pass
def getTimeToRespond(audio_path): pass
def moveRemy(audio_length): pass

class Remy():
    def __init__(self) -> None:
        # Flask and SocketIO initialization
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)

        # Register Socket.IO event handlers
        self.register_socketio_events()

        # Other initialization
        self.context = []
        self.command_queue = queue.Queue()
        self.audio_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.question_event = threading.Event()
        self.audio_player = AudioPlayer()
        self.video_player = VideoPlayer()
        self.handler_thread = None
        self.listener_thread = None
        self.transcribe_thread = None
        self.conversation = []

        # Load environment variables from .env file
        load_dotenv()

        # Get OpenAI API key from environment variables
        self.api_key = os.getenv('OPENAI_API_KEY')

        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)

        # Start the command handler, listener, and transcribe threads
        self.start()

        # Start the Flask-SocketIO server
        self.run_socketio_server()

    def register_socketio_events(self):
        @self.socketio.on('connect')
        def handle_connect():
            print("Client connected")

        @self.socketio.on('disconnect')
        def handle_disconnect():
            print("Client disconnected")

        # @self.socketio.on('moveremy')
        # def handle_moveremy(data):
        #     print(f"Received audio_length: {data['audio_length']}")
        #     moveRemy(data['audio_length'])
        #     # Respond back to the client
        #     self.socketio.emit('moveremy_response', {'status': 'success', 'message': 'Audio processed'})

    def run_socketio_server(self):
        # Start the Flask-SocketIO server in a separate thread
        server_thread = threading.Thread(target=self.socketio.run, args=(self.app,), kwargs={'host': '0.0.0.0', 'port': 5000})
        server_thread.start()

    def respondToCommand(self, response: str) -> None:
        time = None
        print("response:", response)
        audio_path = self.text_to_audio(response)
        if audio_path:
            time = self.audio_player.get_audio_length(audio_path)
            self.audio_player.play(audio_path, should_delete=True)
            move_robot(time)

    def sendCommand(self, command: str) -> None:
        print("command:", command)
        photo = self.video_player.capture_frame_as_base64()
        response = self._remy_gpt(" ".join(self.context), command)
        self.conversation.append({
            "img": photo,
            "question": command,
            "answer": response
        })
        self.context.append("Client: " + command)
        self.context.append("Remy: " + response)
        self.respondToCommand(response)

    def command_handler(self):
        while True:
            command = self.command_queue.get()
            if command is None:
                print("Received stop signal.")
                break
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
                    audio = recognizer.listen(source, phrase_time_limit=5)
                    self.audio_queue.put(audio.get_wav_data())
                except sr.UnknownValueError:
                    print("Could not understand audio")
                except KeyboardInterrupt:
                    print("Stopping...")
                    self.audio_queue.put(None)
                    self.transcribe_thread.join()
                    break

    def transcribe_audio(self):
        while True:
            audio_data = self.audio_queue.get()
            if audio_data is None:
                break

            try:
                with open("temp_audio.wav", "wb") as f:
                    f.write(audio_data)

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

                if "what's up" in text:
                    self.question_event.set()
                    self.audio_player.play("./chime.mp3")

                os.remove("temp_audio.wav")

            except Exception as e:
                print(f"An error occurred: {str(e)}")

    def text_to_audio(self, text, subfolder="generated_audio"):
        subfolder_path = "./" + subfolder
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        speech_file_path = subfolder_path + "/" + f"remy_gpt_output_audio_{timestamp}.mp3"

        response = self.client.audio.speech.create(
            model="tts-1",
            voice="echo",
            input=text
        )

        response.stream_to_file(speech_file_path)
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
                {"role": "system", "content": "You are Remy the rat from Ratatouille..."},
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
