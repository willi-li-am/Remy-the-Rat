#do some flask shit

from flask import Flask, request
from robot import remy
from pydub import AudioSegment

app = Flask(__name__) 

@app.route('/move_remy', methods=['GET'])
def move_remy(): 
    audio_path = request.args.get('audio_path')
    audio = AudioSegment.from_file(audio_path)
    audio_length = len(audio) / 1000.0
    remy.fast_chopping(audio_length)


if __name__ == "__main__": 
    app.run("127.0.0.1", port=5000)