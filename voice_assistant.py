import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser


# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set speaking speed
engine.setProperty("rate", 170)


def speak(text):
    """Convert text to speech and print it."""
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


def listen():
    """Listen to the user's voice and convert it into text."""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

        except sr.WaitTimeoutError:
            speak("I did not hear anything. Please try again.")
            return ""

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print("You:", command)
        return command.lower()

    except sr.UnknownValueError:
        speak("Sorry, I could not understand your voice. Please repeat.")
        return ""

    except sr.RequestError:
        speak("Sorry, the speech recognition service is unavailable.")
        return ""


def tell_date():
    """Tell today's date."""
    today = datetime.datetime.now()
    date = today.strftime("%d %B %Y")
    speak("Today's date is " + date)


def tell_time():
    """Tell the current time."""
    current_time = datetime.datetime.now()
    time = current_time.strftime("%I:%M %p")
    speak("The current time is " + time)


def web_search(topic):
    """Search the web for the requested topic."""
    speak("Searching the web for " + topic)
    url = "https://www.google.com/search?q=" + topic.replace(" ", "+")
    webbrowser.open(url)


def process_command(command):
    """Process the user's command."""

    if command == "":
        return True

    # Greeting
    if "hello" in command or "hi" in command:
        speak("Hello! How can I help you?")

    # Current time
    elif "time" in command:
        tell_time()

    # Current date
    elif "date" in command:
        tell_date()

    # Web search
    elif command.startswith("search"):
        topic = command.replace("search", "", 1).strip()

        if topic:
            web_search(topic)
        else:
            speak("Please tell me what you want me to search.")

    # Exit
    elif "exit" in command or "stop" in command or "bye" in command:
        speak("Goodbye! Have a nice day.")
        return False

    # Unknown command
    else:
        speak("Sorry, I don't understand that command.")

    return True


def main():
    """Start the voice assistant."""

    speak("Hello! I am your voice assistant.")
    speak("You can say hello, ask for the time or date, or say search followed by a topic.")

    while True:
        command = listen()

        if not process_command(command):
            break


if __name__ == "__main__":
    main()