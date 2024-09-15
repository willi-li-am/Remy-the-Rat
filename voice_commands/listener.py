import speech_recognition as sr

def listen_for_phrase(target_phrase, phrase_time_limit=None):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Adjusting for ambient noise. Please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening for the phrase...")

        while True:
            try:
                # Listen for audio with a time limit
                audio = recognizer.listen(source, phrase_time_limit=phrase_time_limit)
                # Recognize speech using Google Web Speech API
                text = recognizer.recognize_google(audio, show_all=False).lower()
                print("You said:", text)  # Print what was recognized

                if target_phrase.lower() in text:
                    print("You said Hey Remy!")
            
            except sr.UnknownValueError:
                print("Could not understand audio")
                continue
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition service.")
                break

if __name__ == "__main__":
    listen_for_phrase("hey", phrase_time_limit=3)