#do some flask shit

from flask import Flask
from robot import remy
from pydub import AudioSegment
from pathlib import Path

app = Flask(__name__) 

@app.route('/move_remy', methods=['GET'])
def move_remy(): 
    audio_path = Path(__file__).parent / "audio" / "generated_files" / "speech2.mp3"
    audio = AudioSegment.from_file(audio_path)
    audio_length = len(audio) / 1000.0
    remy.fast_chopping(audio_length)
    return '', 204


if __name__ == "__main__": 
    app.run("127.0.0.1", port=5000)