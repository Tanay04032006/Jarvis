import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import spotipy
from spotipy.oauth2 import SpotifyOAuth

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis Sir. Please tell me how may I help you")


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"
    return query


def send_email(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()


if __name__ == "__main__":
    wish_me()
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope='user-library-read user-read-playback-state user-modify-playback-state',
        client_id='b4bd271aefe64cd198a89e9de34fdea9',
        client_secret='0f7096192d01482d896b6ad0c4a645c4',
        redirect_uri='http://localhost:8888/callback',
    ))

    while True:
        query = take_command().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'play music' in query:
            music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {str_time}")

        elif 'open code' in query:
            code_path = "C:\\Users\\Haris\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(code_path)

        elif 'email to harry' in query:
            try:
                speak("What should I say?")
                email_content = take_command()
                to_email = "harryyouremail@gmail.com"
                send_email(to_email, email_content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send this email")

        elif 'play song on spotify' in query:
            try:
                speak("Sure! What's the name of the song?")
                song_name = take_command().lower()

                results = sp.search(q=song_name, type='track', limit=1)

                if results['tracks']['items']:
                    track_uri = results['tracks']['items'][0]['uri']
                    sp.start_playback(uris=[track_uri])
                    speak(f"Playing {song_name} on Spotify!")
                else:
                    speak(f"Sorry, I couldn't find {song_name} on Spotify.")

            except Exception as e:
                print(e)
                speak("Sorry, there was an error playing the song on Spotify.")
        elif 'stop' in query:
            break

