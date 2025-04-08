import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import pyautogui
import pyjokes

import sys

# Initialize the TTS engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Use female voice
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

# Speak text aloud
def speak(audio) -> None:
    engine.say(audio)
    engine.runAndWait()

# Tell the current time
def time() -> None:
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    speak("The current time is")
    speak(current_time)
    print("The current time is", current_time)

# Tell the current date
def date() -> None:
    now = datetime.datetime.now()
    speak("The current date is")
    speak(f"{now.day} {now.strftime('%B')} {now.year}")
    print(f"The current date is {now.day}/{now.month}/{now.year}")

# Greet the user
def wishme() -> None:
    speak("Welcome back, sir!")
    print("Welcome back, sir!")

    hour = datetime.datetime.now().hour
    if 4 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 16:
        speak("Good afternoon!")
    elif 16 <= hour < 24:
        speak("Good evening!")
    else:
        speak("Good night, see you tomorrow.")

    assistant_name = load_name()
    speak(f"{assistant_name} at your service. Please tell me how may I assist you.")
    print(f"{assistant_name} at your service. Please tell me how may I assist you.")

# Take a screenshot
def screenshot() -> None:
    img = pyautogui.screenshot()
    img_path = os.path.expanduser("~/Pictures/screenshot.png")
    img.save(img_path)
    speak(f"Screenshot saved as {img_path}.")
    print(f"Screenshot saved as {img_path}.")

# Listen to user's voice and convert it to text
def takecommand() -> str | None:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            speak("Timeout occurred. Please try again.")
            return None

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(query)
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
    except Exception as e:
        speak(f"An error occurred: {e}")
        print(f"Error: {e}")
    return None

# Play music
def play_music(song_name=None) -> None:
    song_dir = os.path.expanduser("~/Music")
    if not os.path.exists(song_dir):
        speak("Music folder not found.")
        return

    songs = os.listdir(song_dir)
    if song_name:
        songs = [song for song in songs if song_name.lower() in song.lower()]

    if songs:
        song = random.choice(songs)
        os.startfile(os.path.join(song_dir, song))
        speak(f"Playing {song}.")
        print(f"Playing {song}.")
    else:
        speak("No song found.")
        print("No song found.")

# Set assistant name
def set_name() -> None:
    speak("What would you like to name me?")
    name = takecommand()
    if name:
        with open("assistant_name.txt", "w") as file:
            file.write(name)
        speak(f"Alright, I will be called {name} from now on.")
    else:
        speak("Sorry, I couldn't catch that.")

# Load assistant name
def load_name() -> str:
    try:
        with open("assistant_name.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Jarvis"

# Search Wikipedia
def search_wikipedia(query: str) -> None:
    speak("Searching Wikipedia...")
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
        print(results)
    except wikipedia.DisambiguationError as e:
        speak("There are multiple results for your query. Please be more specific.")
        print("Disambiguation error:", e.options)
    except wikipedia.PageError:
        speak("Sorry, I couldn't find anything matching your query.")
    except Exception as e:
        speak("An error occurred while searching Wikipedia.")
        print(f"Wikipedia Error: {e}")

# Main program execution
if __name__ == "_main_":
    wishme()
    while True:
        query = takecommand()
        if query is None:
            continue

        if "time" in query:
            time()
        elif "date" in query:
            date()
        elif "wikipedia" in query:
            search_wikipedia(query.replace("wikipedia", "").strip())
        elif "play music" in query:
            play_music()
        elif "screenshot" in query:
            screenshot()
        elif "set name" in query:
            set_name()
        elif "joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)
            print(joke)
        elif "exit" in query or "quit" in query or "stop" in query:
            speak("Goodbye sir, have a great day!")
            sys.exit()
        else:
            speak("Sorry, I didn't understand that.")