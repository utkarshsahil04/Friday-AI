import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclib
import requests
import openai as OpenAI
from dotenv import load_dotenv
import os

reco = sr.Recognizer()
ttsx = pyttsx3.init()
load_dotenv(dotenv_path="D:\Programming\Python ChapterWise Notes\Mega project\.env")

load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")
newsapi = os.getenv("eb08ee999c80486da11f45868f60805e")

# print(f"Loaded API Key: {openai.api_key}")  # Ensure this is not 'None'

def speak(text):
    ttsx.say(text)
    ttsx.runAndWait()
    print(f'Speak: {text}')

def aiProcess(command):
    client = OpenAI(api_key="",
    )
    print(client)

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content

def processcommand(c):
    if "open google" in c.lower():
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "open amazon" in c.lower():
        speak("Opening Amazon")
        webbrowser.open("https://amazon.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ", 1)[1]
        link = musiclib.music.get(song)
        if link:
            webbrowser.open(link)
            speak(f'playing {song}') 
        else:
            speak(f"Sorry, I couldn't find the song {song}.")
    elif "news" in c.lower():
        r = requests.get(
            f"https://newsapi.org/v2/everything?q=tesla&from=2024-09-28&sortBy=publishedAt&apiKey={newsapi}"
        )
        if r.status_code == 200:
            data = r.json()
            titles = [article["title"] for article in data.get("articles", [])]
            speak("Here are the top news headlines: " + ", ".join(titles))
        else:
            speak(f"Failed to fetch data. Status code: {r.status_code}")
    else:
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Hello, There")
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            try:
                audio = reco.listen(source)
                word = reco.recognize_google(audio)
                if word.lower() == "friday":
                    speak("Yeah, how are you Sahil?")
                    print("Friday is Active...")
                    audio = reco.listen(source)
                    command = reco.recognize_google(audio)
                    print(command)
                    processcommand(command)
                if word.lower() in ["exit", "quit"]:
                    speak("Goodbye!")
                    break
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand that.")
            except sr.RequestError as e:
                print(f"Google API request failed: {e}")
            except Exception as e:
                print(f"Error: {e}")
