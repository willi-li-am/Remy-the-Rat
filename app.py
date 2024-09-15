#do some flask shit

from flask import Flask, request
from robot import remy
from pydub import AudioSegment
from pathlib import Path

app = Flask(__name__) 

@app.route('/move_remy', methods=['POST'])
def move_remy(): 
    audio_length = request.args.get('audio_length')
    if not audio_length: 
        return '', 400
    audio_length = float(audio_length)
    remy.fast_chopping(audio_length)
    return '', 204


if __name__ == "__main__": 
    app.run("127.0.0.1", port=5000)