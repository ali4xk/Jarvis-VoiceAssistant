import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime

recognizer = sr.Recognizer()
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening.....")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            print("No speech detected")
            return ""

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
        webbrowser.open("https://youtube.com")
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "search for" in command:
        query = command.split("search for", 1)[1].strip()
        if query:
            speak(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            speak("What do you want me to search for?")
    elif "what time" in command or "current time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")
    elif command == "":
        pass
    else:
        speak("I did not understand that command")

if __name__ == "__main__":
    speak("Initializing Jarvis")
    while True:
        command = listen()
        handle_command(command)