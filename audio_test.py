from audio import AudioPlayer
import time

audio_player = AudioPlayer()

audio_player.play("./chime.mp3")
audio_player.play("./chime.mp3")
audio_player.play("./chime.mp3")
time.sleep(10)

audio_player.stop()