import speech_recognition as sr
import webbrowser
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening.....")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(command)
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Recognition error; {0}".format(e))
        return ""

def handle_command(command):
    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https:/switching from sphinx/youtube.com")
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif command == "":
        pass
    else:
        speak("I did not understand that command")

if __name__ == "__main__":
    speak("Initializing Jarvis")
    while True:
        command = listen()
        handle_command(command)