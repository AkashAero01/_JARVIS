import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import os 
import yt_dlp
import sys
import datetime
import subprocess
from requests import get


# Initialize recognizer and engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to handle TTS
def speak(text):
    engine.say(text)
    engine.runAndWait()

def play_music(query):
    search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(search_url)

    # Optionally download and play the first result
    with yt_dlp.YoutubeDL({"format": "bestaudio"}) as ydl:
        result = ydl.extract_info(f"ytsearch:{query}", download=False)
        if result['entries']:
            video_url = result['entries'][0]['webpage_url']
            webbrowser.open(video_url)
        

def wish_user():
    """Function to wish user based on time"""
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Sir!")

def app_open(app_name):
    try:
        subprocess.Popen(app_name,shell=True)
        speak(f"opening {app_name}")
    except FileNotFoundError:
        speak(f"Sorry, I couldn't find {app_name} on your system.")
    except Exception as e:
        speak(f"An error occurred while trying to open {app_name}: {e}")


def shutdown_pc():
    speak("Are you sure you want to shut down the computer?")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            response = recognizer.recognize_google(audio).lower()
            
            if "yes" in response:
                speak("Shutting down the computer. Goodbye, sir!")
                os.system("shutdown /s /t 5")  # Shuts down the computer after 5 seconds
            else:
                speak("Shutdown cancelled.")
        except sr.UnknownValueError:
            speak("I couldn't understand your response. Shutdown cancelled.")
        except sr.RequestError as e:
            speak(f"Speech recognition service error: {e}")
        except Exception as e:
            speak(f"An error occurred: {e}")

                
# Function to search Google and respond with results
def google_search(query):
    """Open Google search for the given query in a web browser."""
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    speak(f"Searching Google for {query}.")
    webbrowser.open(search_url)

# Function to process commands
def process_cmd(command):
    command = command.lower()
    if "open google" in command:
        webbrowser.open("https://google.com")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
    elif "open music" in command:
        webbrowser.open("https://open.spotify.com/")
    elif "open jethalal" in command:
        webbrowser.open("https://www.youtube.com/results?search_query=tmkoc+old+episodes")
    elif command.startswith("play"): 
        song = command
        play_music(song)
    elif "search" in command:
        query = command.replace("search", "").strip()
        google_search(query)    
    elif "shutdown" in command:
        speak("shutting down. Goodbye sir!")
        sys.exit()
    elif "time" in command:
        time = datetime.datetime.now().strftime("%H:%M")
        speak(time)
    elif "app" in command:
        app_name=command[5:-4].strip()
        app_open(app_name)
    elif "turn off the pc" in command:
        shutdown_pc()
    elif "ip" in command:
        ip=get('https://api.ipify.org').text
        speak(f"your ip adress is: {ip}")
    else:
        speak("Sorry, I didn't understand that command.")

# Main function to handle wake word and commands
def listen_and_respond():
    with sr.Microphone() as source:
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")

        while True:
            try:
                # Listen for the wake word
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                word = recognizer.recognize_google(audio)

                if "jarvis" in word.lower():
                    speak("Yes sir")
                    print("Listening for your command...")

                    # Listen for the command
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    print(f"Command recognized: {command}")
                    process_cmd(command)

                else:
                    print(f"Heard '{word}' but did not detect the wake word.")

            except sr.UnknownValueError:
                print("Could not understand audio. Please try again.")
            except sr.RequestError as e:
                print(f"Speech recognition service error: {e}")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                # Small pause to avoid overwhelming the microphone
                time.sleep(0.5)



if __name__ == "__main__":

        speak("Intializing jarvis...")
        listen_and_respond()



