import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclib
import requests
import openai
from dotenv import load_dotenv
import os
import pyautogui
import time

ttsx = pyttsx3.init()
load_dotenv(dotenv_path="D:\Programming\Python ChapterWise Notes\Mega project\.env")

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
newsapi = os.getenv("eb08ee999c80486da11f45868f60805e")

print(f"Loaded API Key: {openai.api_key}") 

def speak(text):
    ttsx.say(text)
    ttsx.runAndWait()
    print(f'Speak: {text}') 

def aiProcess(command):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": command}]
    )
    return response['choices'][0]['message']['content']

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
            speak(f"opening{song}")
            time.sleep(6)
            pyautogui.leftClick(960,940)
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
       

        command = input("Type here or (Exit)")
        if(command.lower()=="friday"):
            speak("Friday is Active...Yeah, how are you Sahil?") 
            # =input("Enter commands: ")      
        processcommand(command) 
        print(command)
        if command.lower() in ["exit", "quit"]:
            speak("Goodbye!")
            break
         
        