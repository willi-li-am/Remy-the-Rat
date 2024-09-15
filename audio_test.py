from audio import AudioPlayer
import time

audio_player = AudioPlayer()

audio_player.play("./chime.mp3")
audio_player.play("./generated_audio/remy_gpt_output_audio_20240915_025629.wav")
audio_player.play("./chime.mp3")
time.sleep(10)

audio_player.stop()