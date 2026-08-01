# Jarvis — Desktop Voice Assistant

A voice-controlled desktop assistant built in Python. Listens for spoken commands, transcribes them locally using OpenAI's Whisper model, and responds with synthesized speech.

## Features

- **Voice recognition** — powered by [Whisper](https://github.com/openai/whisper), running fully offline/local after the model downloads once
- **Text-to-speech** — spoken responses via `pyttsx3`
- **Web commands** — open YouTube, open Google, search the web ("search for cats")
- **Time** — "what time is it"
- **Weather** — live weather lookup by city via the OpenWeatherMap API ("weather in Lahore")
- **App control** — open local apps by voice: Notepad, Calculator, Paint, Chrome, Spotify, Settings, WhatsApp
- **To-do list** — add, list, and clear tasks, saved locally to a JSON file so they persist between runs
- **Exit command** — "exit" / "quit" / "stop listening" shuts it down cleanly
- **Error handling** — gracefully handles no-speech timeouts, unrecognized audio, network issues, and unexpected errors without crashing

## Tech stack

- Python 3
- `speech_recognition` — microphone capture
- `openai-whisper` — offline speech-to-text
- `pyttsx3` — offline text-to-speech
- `requests` — weather API calls
- `webbrowser`, `subprocess`, `os`, `json`, `datetime` — standard library, for commands and storage

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/ali4xk/JarvisProject.git
cd JarvisProject
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install ffmpeg
Whisper requires `ffmpeg` to be installed and available on your system PATH.

- Windows: `winget install "FFmpeg (Essentials Build)"`
- Or download manually from [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/)

Verify with:
```bash
ffmpeg -version
```

### 5. Set your OpenWeatherMap API key
Get a free key at [openweathermap.org/api](https://openweathermap.org/api), then set it as an environment variable.

Windows (PowerShell):
```powershell
setx OPENWEATHER_API_KEY "your_key_here"
```
Restart your terminal after setting this for it to take effect.

### 6. Run it
```bash
python main.py
```
The first run will download the Whisper model (~150MB) — this only happens once.

## Voice commands

| Command | Action |
|---|---|
| "open youtube" | Opens YouTube in your browser |
| "open google" | Opens Google in your browser |
| "what time is it" | Speaks the current time |
| "search for [query]" | Opens a Google search for the query |
| "weather in [city]" | Speaks the current weather for that city |
| "open notepad / calculator / paint / chrome / spotify / settings / whatsapp" | Launches the app |
| "add task [task]" | Adds a task to your to-do list |
| "my tasks" | Lists all saved tasks |
| "clear tasks" | Clears the to-do list |
| "exit" / "quit" / "stop listening" | Shuts down |

## Notes

- Some app paths (Spotify, WhatsApp) in `main.py` are set to a common default install location and may need adjusting for your specific machine.
- This is an offline-first build: recognition (Whisper), speech (pyttsx3), and app control all run locally with no per-request internet calls — only the weather and web search commands need an internet connection.

## Developed by Muhammad Ali (@ali4xk)
