import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime
import requests
import subprocess
import os
import json
import whisper

recognizer = sr.Recognizer()
WEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")
TASKS_FILE = "tasks.json"
TEMP_AUDIO_FILE = "temp_audio.wav"

whisper_model = whisper.load_model("base")

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

    with open(TEMP_AUDIO_FILE, "wb") as f:
        f.write(audio.get_wav_data())

    try:
        result = whisper_model.transcribe(TEMP_AUDIO_FILE, fp16=False)
        command = result["text"].strip().lower()
        print(command)
        return command
    except Exception as e:
        print(f"Whisper error: {e}")
        return ""
    finally:
        if os.path.exists(TEMP_AUDIO_FILE):
            os.remove(TEMP_AUDIO_FILE)

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

APPS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "spotify": r"C:\Users\LENOVO\AppData\Local\Microsoft\WindowsApps\Spotify.exe",
}

def open_app(app_name):
    if app_name == "settings":
        try:
            os.startfile("ms-settings:")
            return "Opening Settings"
        except OSError:
            return "I could not open Settings"

    if app_name == "whatsapp":
        try:
            os.startfile("shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App")
            return "Opening WhatsApp"
        except OSError:
            return "I could not open WhatsApp"

    exe = APPS.get(app_name)
    if not exe:
        return f"I do not know how to open {app_name}"
    try:
        subprocess.Popen(exe)
        return f"Opening {app_name}"
    except FileNotFoundError:
        return f"I could not find {app_name} on this computer"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def add_task(task_text):
    tasks = load_tasks()
    tasks.append(task_text)
    save_tasks(tasks)
    return f"Added task: {task_text}"

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        return "You have no tasks"
    if len(tasks) == 1:
        return f"You have one task: {tasks[0]}"
    task_list = ", ".join(tasks)
    return f"You have {len(tasks)} tasks: {task_list}"

def clear_tasks():
    save_tasks([])
    return "All tasks cleared"

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
    elif "open notepad" in command:
        speak(open_app("notepad"))
    elif "open calculator" in command:
        speak(open_app("calculator"))
    elif "open paint" in command:
        speak(open_app("paint"))
    elif "open chrome" in command:
        speak(open_app("chrome"))
    elif "open spotify" in command:
        speak(open_app("spotify"))
    elif "open whatsapp" in command:
        speak(open_app("whatsapp"))
    elif "open settings" in command:
        speak(open_app("settings"))
    elif "add task" in command:
        task_text = command.split("add task", 1)[1].strip()
        if task_text:
            speak(add_task(task_text))
        else:
            speak("What is the task?")
    elif "my tasks" in command or "list tasks" in command:
        speak(list_tasks())
    elif "clear tasks" in command:
        speak(clear_tasks())
    elif "exit" in command or "quit" in command or "stop listening" in command:
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