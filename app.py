def takePhoto(): pass
def askChatGPT(): pass
def replayAudio(): pass
def getTimeToRespond(): pass
def moveRemy(): pass

class Remy():
    def __init__(self) -> None:
        context = [] # TODO: make a function that turns context into a string of User and Remy

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
        self.context.append(command)
        photo = takePhoto()
        response = askChatGPT(self.context, command, photo)
        self.context.append(response)
        self.respondToCommand(response)

if __name__ == '__main__':
    pass