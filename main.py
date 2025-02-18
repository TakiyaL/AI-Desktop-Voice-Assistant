import speech_recognition as sr
import webbrowser
import pywhatkit
import wikipedia
import os
import datetime
import pyjokes
import pyautogui
from Voice import *
import google.generativeai as genai

# Configure Google Gemini API
genai.configure(api_key="AIzaSyBBF5wppFXSqZdP2Ffi2x08zMCwlgldeE4")
model = genai.GenerativeModel("gemini-1.5-flash")


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Understanding...")
        query = recognizer.recognize_google(audio,language="en-in")
        print("==> You said:", query)
    except Exception as e:
        print("Say That Again....")
        return "None"
    return query

def greetMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Good Morning,sir")
    elif hour >12 and hour<=18:
        speak("Good Afternoon ,sir")
    else:
        speak("Good Evening,sir")

    speak("Please tell me, How can I help you ?")

def searchGoogle(query):
    if "google" in query:
        import wikipedia as googleScrap
        query = query.replace("jarvis","")
        query = query.replace("google search","")
        query = query.replace("google","")
        speak("This is what I found on google")

        try:
            pywhatkit.search(query)
            result = googleScrap.summary(query,1)
            speak(result)

        except:
            speak("No speakable output available")

def searchYoutube(query):
    if "youtube" in query:
        speak("This is what I found for your search!") 
        query = query.replace("youtube search","")
        query = query.replace("youtube","")
        query = query.replace("jarvis","")
        web  = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(web)
        pywhatkit.playonyt(query)
        speak("Done, Sir")

def searchWikipedia(query):
    if "wikipedia" in query:
        speak("Searching from wikipedia....")
        query = query.replace("wikipedia","")
        query = query.replace("search wikipedia","")
        query = query.replace("jarvis","")
        results = wikipedia.summary(query,sentences = 2)
        speak("According to wikipedia..")
        print(results)
        speak(results)

if __name__ == '__main__':
     # Initialize chat with history
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": "Hello"},
            {"role": "model", "parts": "Great to meet you. What would you like to know?"},
        ]
    )
    
    print('Welcome to Jarvis AI')
    speak("Welcome back Sir")
    
    while True:
        query = listen().lower()
        
        if not query:
            continue
         # Send user input to Gemini
        response = chat.send_message(query, stream=True)
        
        # Collect and speak the AI's response
        ai_response = ""
        for chunk in response:
            ai_response += chunk.text
        
        print("\n")
        speak(ai_response)
        
        if "Jarvis" in query or "wake up" in query:
            greetMe()

        if "play my music" in query:
           musicPath = "C:/Users/lenix/Downloads/Guns_N_Roses_-_Sweet_Child_O_Mine.mp3"
           os.system(f"start {musicPath}")

        if "the time" in query:
            strfTime = datetime.datetime.now().strftime("%H:%M")
            speak(f"Sir, the time is {strfTime}")    
                        
        elif "joke" in query:
            joke=pyjokes.get_joke()
            print(joke)
            speak(joke)
        
        elif "google" in query:           
            searchGoogle(query)
        
        elif "youtube" in query:           
            searchYoutube(query)
        
        elif "wikipedia" in query:          
            searchWikipedia(query)

        elif "open" in query:   
            query = query.replace("open","")
            query = query.replace("jarvis","")
            pyautogui.press("super")
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press("enter")       
                        
        elif "shut down" in query or "shutdown" in query or "Quit" in query or "Exit" in query:
            speak("Shutting down,sir")
            exit()




