import queue
import threading
import time
def takePhoto(): pass
def askChatGPT(context, command, photo): pass
def replayAudio(audio_path): pass
def getTimeToRespond(audio_path): pass
def moveRemy(audio_length): pass

class Remy():
    def __init__(self) -> None:
        self.context = [] # TODO: make a function that turns context into a string of User and Remy
        self.command_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.handler_thread = None

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
        print(command)
        self.context.append(command)
        photo = takePhoto()
        response = askChatGPT(self.context, command, photo)
        self.context.append(response)
        self.respondToCommand(response)

    def listen(self):
        """Listen for commands and process them. Stop when signaled."""
        try:
            while True:
                command = self.command_queue.get()
                if command is None:  # 'None' signals the thread to stop
                    print("Received stop signal.")
                    break

                # Process the command
                if command:
                    self.sendCommand(command)

        except KeyboardInterrupt:
            print("Stopping...")
            self.command_queue.put(None) 
            self.handler_thread.join()
            return  
    
    def start(self):
        self.handler_thread = threading.Thread(target=self.listen)
        self.handler_thread.start()
        #add listener thread here?
        self.listen()
    def add(self, command):
        self.command_queue.put(command)

if __name__ == '__main__':
    remy = Remy()
    remy.add("hi")
    remy.start()
