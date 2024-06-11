from speak import speak
from listen import listen
from utils import get_time, get_date, get_weather
from datautils import save_data, load_data
import spacy
import os
import json


nlp = spacy.load("en_core_web_sm")


def greet():
    speak("Hello sir, how can I assist you today?")

def shutdown():
    speak("Shutting down. Goodbye!")

def process_command(command):
    doc = nlp(command)
    if any(token.lemma_ in ["time", "clock"] for token in doc):
        return "time"
    elif any(token.lemma_ in ["date", "day"] for token in doc):
        return "date"
    elif any(token.lemma_ in ["weather", "forecast"] for token in doc):
        for ent in doc.ents:
            if ent.label_ == "GPE":
                return ("weather", ent.text)
        return "ask_city"
    elif any(token.lemma_ in ["info", "data", "save", "retrieve", "load"] for token in doc):
        if any(token.lemma_ in ["save"] for token in doc):
            return "save"
        elif any(token.lemma_ in ["retrieve", "load"] for token in doc):
            return "load"
    elif any(token.lemma_ in ["stop", "shutdown", "shut down" "off"] for token in doc):
        return "shutdown"
    else:
        return "unknown"

def main():
    greet()
    while True:
        command = listen()
        if command is None: #keeps listening till commanded
            continue
        intent = process_command(command) #processes verbal input
        
        #util functions
        if intent == "time": 
            speak(f"The current time is {get_time()}")
        elif intent == "date":
            speak(f"Today's date is {get_date()}")
        elif intent == "ask_city":
            speak("Which city?")
            city = listen()
            if city:
                weather_info = get_weather(city)
                speak(weather_info)
        elif isinstance(intent, tuple) and intent[0] == "weather":
            city = intent[1]
            weather_info = get_weather(city)
            speak(weather_info)
            
        #data util functions
        elif intent == "save":
            speak("which file")
            filename = listen()
            speak("What do you want me to save")
            datatype = listen()
            speak("What " + str(datatype) + "do you want me to save?")
            datavalue = listen()
            if os.path.exists(filename):
                with open(filename, 'r') as file:
                    data = json.load(file)
                data[datatype] = datavalue
                save_data(data, filename)
            else:
                datatemp = {}
                datatemp[datatype] = datavalue
                save_data(datatemp, filename)
            speak("Data saved successfully.")
        elif intent == "load":
            speak("which file")
            filename = listen()
            load_data(filename)
            speak()
            
        #shutdown function
        elif intent == "shutdown":
            shutdown()
            break
        
        #if no function
        else:
            speak("Sorry, I cannot help with that yet.")

if __name__ == "__main__":
    main()