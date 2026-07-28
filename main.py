import speech_recognition as sr
import webbrowser
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()



if __name__== "__main__":
    while True:
        speak("Initializing Jarvis......")
        #Listen for the word Jarvis
        #obtain audio from microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening.....")
            audio = r.listen(source)

        #recoginze speech using Sphinx
        try:
            command = r.recognize_sphinx(audio)
            print(command)
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".fromat(e))
