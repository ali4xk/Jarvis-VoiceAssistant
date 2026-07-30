import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime
import requests
import os

recognizer = sr.Recognizer()
WEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")

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
        speak("I am having trouble connecting to the internet")
        return ""

def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if response.status_code != 200:
            return f"I could not find weather for {city}"

        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        return f"It is currently {temp} degrees Celsius with {description} in {city}"
    except requests.exceptions.RequestException:
        return "I could not reach the weather service"

def handle_command(command):
    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "what time" in command or "current time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")
    elif "search for" in command:
        query = command.split("search for", 1)[1].strip()
        if query:
            speak(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            speak("What do you want me to search for?")
    elif "weather in" in command:
        city = command.split("weather in", 1)[1].strip()
        if city:
            speak(get_weather(city))
        else:
            speak("Which city do you want the weather for?")
    elif "exit" in command or "quit" in command or "stop listening" in command or "bye" in command:
        speak("Goodbye")
        return False
    elif command == "":
        pass
    else:
        speak("I did not understand that command")
    return True

if __name__ == "__main__":
    speak("Initializing Jarvis")
    running = True
    while running:
        try:
            command = listen()
            running = handle_command(command)
        except KeyboardInterrupt:
            print("Shutting down.")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            speak("Something went wrong, but I am still running")