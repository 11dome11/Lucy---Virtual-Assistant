import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import pyjokes
import datetime 
import webbrowser
import subprocess
import winsound
import os
import requests
import psutil 

listener= sr.Recognizer()
engine= pyttsx3.init()
voices=engine.getProperty("voices")
engine.setProperty('voice', voices[0].id)
engine.setProperty("rate", 165)
engine.say('Sono Lucy, cosa posso fare per te?')
engine.runAndWait()

def talk(text):  
    engine.say(text)
    engine.runAndWait()
    
def take_command():
        with sr.Microphone() as source:
            print("Sto ascoltando...")
            voice= listener.record(source,duration=3)
            command= listener.recognize_google(voice, language="it-IT")
            command= command.lower()
            if 'lucy' in command:
                command = command.replace('lucy', '')

        return command
    
def get_weather(city):
    weather_key= "768f0e227a4f91db43e5ed9d29f1499b"
    url= "http://api.openweathermap.org/data/2.5/weather"
    params= {"appid":weather_key, "q":city, "units":"metric", "lang":"it"}
    response = requests.get(url,params=params)
    weather= response.json()
    format_response(weather)

def format_response(weather):
    try:
        condition = weather["weather"][0]["description"]
        temperature = weather["main"]["temp"] 
        temperature = int(temperature)
        humidity = weather ["main"]["humidity"]
        wind = weather["wind"]["speed"]
        wind= int(wind)
        final_str= "Condizioni: {}, Temperatura: {} gradi, Umidità: {}%, Vento: {} chilometri orari". format(condition,temperature,humidity,wind)
    except:
        final_str= "Non sono riuscita a trovare le informazioni"
    talk(final_str)

def note(text):
    date= datetime.datetime.now()
    file_name= str(date).replace(":","-") + "-note.txt"
    with open(file_name,"w") as f:
        f.write(text)
    subprocess.Popen(["notepad.exe", file_name])

def sveglia(text):
    alarm=text
    alarm=alarm.strftime('%H:%M:%S')
    talk('Sveglia impostata')
    print('Sveglia impostata')
    while True:
        now=datetime.datetime.now().time().replace(microsecond=0).strftime('%H:%M:%S')
        if alarm==now:
            winsound.PlaySound("alarmclock.wav", winsound.SND_ASYNC)
            break
        
def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result
            
#MAIN
def run_lucy():
    command= take_command()
    print(command)
    if "una canzone" in command:
        talk("Quale canzone?")
        song=take_command()
        talk(song)
        print(song)
        pywhatkit.playonyt(song)
    elif "meteo" in command:
        talk("Quale città?")
        città=take_command()
        print(città)
        get_weather(città)
    elif "spegni" in command:
        os.system("shutdown /s /t 1")
    elif "riavvia" in command:
        os.system("shutdown /r /t 1")
    elif "batteria" in command:
        battery= psutil.sensors_battery()
        percent= battery.percent
        percent= str(percent)
        per= percent + "per cento"
        talk(per)
    elif "chi è" in command:
        wikipedia.set_lang("it")
        person= command.replace("chi è","")
        info= wikipedia.summary(person,2)
        talk(info)
        print(info)
    elif "che cos'è" in command:
        wikipedia.set_lang("it")
        thing= command.replace("che cos'è","")
        info2= wikipedia.summary(thing,2)
        talk(info2)
        print(info2)
    elif "jokes" in command:
        talk(pyjokes.get_joke())
    elif "ore" in command:
        time= datetime.datetime.now().strftime('%H:%M') 
        print(time)
        talk(time)
    elif "giorno" in command:
        giorno= datetime.date.today().strftime("%d/%m/%Y")
        talk(giorno)
        print(giorno)
    elif "cerca su google" in command:
        talk('Cosa devo cercare?')
        search=take_command()
        print(search)
        url= "https://www.google.com/search?q=" + search
        webbrowser.get().open(url)
    elif "cerca un luogo" in command:
        talk('Quale luogo?')
        luogo=take_command()
        print(luogo)
        url= "https://www.google.nl/maps/place/" + luogo +"/&amp"
        webbrowser.get().open(url)
    elif "scrivi una nota" in command:
        talk('Cosa vuoi che scriva?')
        nota=take_command()
        note(nota)
    elif "apri google chrome" in command:
        subprocess.Popen(['C:\Program Files (x86)\Google\Chrome\Application\chrome.exe', '-new-tab'])
    elif "imposta una sveglia" in command:
        talk('A che ora?')
        orario=take_command()
        orario = orario.replace('alle', '')
        orario_x= datetime.datetime.strptime(orario, " %H:%M").time()
        print(orario_x)
        sveglia(orario_x)
    elif "ciao " or "buonasera" or "buondì" in command:
        talk("Ciao, dimmi")
        run_lucy()
    else:
        talk('Perfavore ripeti il comando')
        run_lucy()

run_lucy()


