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
    try:
        with sr.Microphone() as source:
            print("Sto ascoltando...")
            voice= listener.record(source,duration=3)
            command= listener.recognize_google(voice, language="it-IT")
            command= command.lower()
            if 'lucy' in command:
                command = command.replace('lucy', '')
                print(command)           
    except:
        pass
    return command

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
        else:
            pass
        
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
        pywhatkit.playonyt(song)
    elif "chi è" in command:
        wikipedia.set_lang("it")
        person= command.replace("chi è","")
        info= wikipedia.summary(person,2)
        talk(info)
    elif "che cos'è" in command:
        wikipedia.set_lang("it")
        thing= command.replace("che cos'è","")
        info2= wikipedia.summary(thing,2)
        talk(info2)
    elif "jokes" in command:
        talk(pyjokes.get_joke())
    elif "ore" in command:
        time= datetime.datetime.now().strftime('%H:%M') 
        print(time)
        talk(time)
    elif "giorno" in command:
        giorno= datetime.date.today().strftime("%d/%m/%Y")
        talk(giorno)
    elif "cerca su google" in command:
        talk('Cosa devo cercare?')
        search=take_command()
        url= "https://www.google.com/search?q=" + search
        webbrowser.get().open(url)
    elif "cerca un luogo" in command:
        talk('Quale luogo?')
        luogo=take_command()
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
    else:
        talk('Perfavore ripeti il comando')
        run_lucy()

run_lucy()


