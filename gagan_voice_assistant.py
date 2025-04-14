import customtkinter as ctk
import threading
import pyttsx3
import speech_recognition as sr
import pywhatkit
import datetime
import wikipedia
import pyjokes

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Speak Function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Command Handling
def process_command(command):
    command = command.lower()

    if 'play' in command:
        song = command.replace('play', '').strip()
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)

    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The current time is {current_time}")

    elif 'who is' in command or 'what is' in command:
        try:
            person = command.replace('who is', '').replace('what is', '').strip()
            info = wikipedia.summary(person, sentences=2)
            speak(info)
        except:
            speak("Sorry, I couldn't find that info.")

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        speak(joke)

    elif 'search' in command:
        query = command.replace('search', '').strip()
        speak(f"Searching for {query}")
        pywhatkit.search(query)

    elif 'exit' in command or 'close' in command:
        speak("Goodbye! Shutting down.")
        app.destroy()

    else:
        speak("Sorry, I didn't understand. Please repeat, or contact my master Gagan Chaudhary.")

# Voice Input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.configure(text="🎧 Listening...", text_color="lightgreen")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5)
            status_label.configure(text="⚙️ Processing...", text_color="yellow")
            command = recognizer.recognize_google(audio)
            print(f"Recognized: {command}")
            command_label.configure(text=f"🗣️ Command: {command}")
            process_command(command)
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand. Please repeat.")
        except sr.RequestError:
            speak("Speech service is down. Please check your internet.")
        except Exception as e:
            speak("Something went wrong.")
            print("Error:", e)

# Wake Word Listener
def wake_word_listener():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    while True:
        with mic as source:
            status_label.configure(text="🎙️ Say 'Hey Gagan' to activate...", text_color="#80bfff")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio).lower()
            print("Heard:", text)
            if "hey gagan" in text:
                speak("Yes, I'm listening...")
                listen()
        except:
            continue

# Threading to avoid GUI freeze
def start_thread():
    threading.Thread(target=listen).start()

# GUI Setup
app = ctk.CTk()
app.title("🎙️ Gagan Voice Assistant")
app.geometry("650x520")
ctk.set_appearance_mode("light")  # Use light mode for relaxed feel
ctk.set_default_color_theme("blue")  # calm blue tones

# Styling Fonts
title_font = ("Segoe UI", 28, "bold")
label_font = ("Segoe UI", 16)
command_font = ("Segoe UI", 14)

# Title Label
title_label = ctk.CTkLabel(app, text="✨ Gagan Voice Assistant", font=title_font, text_color="#0066cc")
title_label.pack(pady=25)

# Status
status_label = ctk.CTkLabel(app, text="Click Start to begin...", font=label_font, text_color="#333333")
status_label.pack(pady=12)

# Command Output
command_label = ctk.CTkLabel(app, text="🗣️ Command: ", font=command_font, text_color="#444444")
command_label.pack(pady=8)

# Start Listening Button
start_btn = ctk.CTkButton(app, text="🎧 Start Listening", command=start_thread, width=180, height=40, corner_radius=15, font=("Segoe UI", 14))
start_btn.pack(pady=20)

# Launch wake word listener in background
threading.Thread(target=wake_word_listener, daemon=True).start()

# Initial Voice Greeting
def welcome_voice():
    speak("Hello! I am Gagan, your voice assistant. Click Start and give me a command.")

# Start welcome voice after GUI appears
app.after(1000, welcome_voice)

app.mainloop()
