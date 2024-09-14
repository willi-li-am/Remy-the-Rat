import speech_recognition as sr

def listen_for_phrase_pocketsphinx(target_phrase):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Adjusting for ambient noise. Please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening for the phrase...")

        while True:
            try:
                # Listen for audio
                audio = recognizer.listen(source)
                # Recognize speech using pocketsphinx
                text = recognizer.recognize_sphinx(audio).lower()
                print("You said:", text)  # Print what was recognized

                if target_phrase.lower() in text:
                    print("You said Hey Remy!")
            
            except sr.UnknownValueError:
                print("Could not understand audio")
                continue
            except sr.RequestError:
                print("Could not request results from PocketSphinx service.")
                break

if __name__ == "__main__":
    listen_for_phrase_pocketsphinx("hey")
