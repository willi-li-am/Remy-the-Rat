import pygame
import time
import threading
import queue

class AudioPlayer:
    def __init__(self):
        self.is_running = True
        self.playback_queue = queue.Queue()
        self.playback_thread = threading.Thread(target=self._playback_worker, daemon=True)
        self.playback_thread.start()
        self.is_playing = True

    def _playback_worker(self):
        """Worker thread that continuously checks for audio to play."""
        pygame.mixer.init()  # Initialize the mixer in the main thread
        print("initialized mixer")
        while self.is_running:
            try:
                # Block until there is an audio file to play
                audio = self.playback_queue.get(timeout=0.1)  # Wait for audio to be queued
                audio_path = audio['audio']
                should_delete = audio['should_delete']
                pygame.mixer.music.load(audio_path)
                print('audio loaded')
                pygame.mixer.music.play()
                print('audio_played')

                # Wait until the music finishes playing before proceeding
                while pygame.mixer.music.get_busy():
                    time.sleep(0.2)
                
                if should_delete:
                    #TODO add delete function here
                    pass
    
            except queue.Empty:
                continue  # If no audio is in the queue, keep waiting

    def stop(self):
        self.is_running = False
        self.playback_thread.join()  # Ensure thread finishes

    def play(self, audio_path, should_delete = False):
        """Add audio to the queue to be played."""
        self.playback_queue.put({
            "audio": audio_path,
            "should_delete": should_delete
        })
