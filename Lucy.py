import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime 
import webbrowser
import subprocess
import winsound
import os
import requests
import psutil 
import pyautogui as pg
from feel_it import EmotionClassifier
from google_trans_new import google_translator
import re
import urllib.request
import tkinter as tk
import time as tm
import sys

def start():
    global listener
    listener= sr.Recognizer()
    global engine
    engine= pyttsx3.init()
    voices=engine.getProperty("voices")
    engine.setProperty('voice', voices[0].id)
    engine.setProperty("rate", 165)
    engine.say('Sono Lucy, cosa posso fare per te?')
    engine.runAndWait()
    run_lucy()
    
def again():
    while True:
        tm.sleep(2)
        talk("Posso aiutarti ancora?")
        run_lucy()

def talk(text):  
    engine.say(text)
    engine.runAndWait()

def non_ascolto():
    label.config(text="")
    app.update()
    
def take_command(wam=False, tim=False, wan=False):
        label.config(padx=0,pady=0,text="Sto ascoltando\n\U0001F60A",font=("Courier",9))
        app.update()
        with sr.Microphone() as source:
            if wam:
                voice= listener.record(source,duration=6)
                command= listener.recognize_google(voice, language="it-IT")
                command= command.lower()
                if 'lucy' in command:
                    command = command.replace('lucy','')
            elif wan:
                t = {'uno':'1','due':'2','tre':'3','quattro':'4','cinque':'5',
                     'sei':'6','sette':'7',
                     'otto':'8','nove':'9'}
                voice= listener.record(source,duration=7)
                command= listener.recognize_google(voice, language="it-IT")
                for i in t:
                    if (i==command):
                        command=t[i]
                command=command.replace(" ","")
            elif tim:
                t = {'uno':1,'due':2,'tre':3,'quattro':4,'cinque':5,'sei':6,'sette':7,
                     'otto':8,'nove':9,'dieci':10,'undici':11,'dodici':12,'tredici':13,
                     'quattordici':14,'quindici':15,'sedici':16,'diciassette':17,
                     'diciotto':18,'diciannove':19,'venti':20}
                voice= listener.record(source,duration=4)
                command= listener.recognize_google(voice, language="it-IT")
                for i in t:
                    if (i==command):
                        command=t[i]
            else:
                voice= listener.record(source,duration=4)
                command= listener.recognize_google(voice, language="it-IT")
                command= command.lower()
                if 'lucy' in command:
                    command = command.replace('lucy','')
            non_ascolto()
        return command

def emotions(text):
    emo=text
    emoclass= EmotionClassifier()
    pred= emoclass.predict([emo])
    sens=pred[0]
    translator= google_translator()
    trad= translator.translate(sens, lang_src="en", lang_tgt="it")
    final= "Credo tu stia provando" + trad
    return final
    
def get_weather(city):
    weather_key= "768f0e227a4f91db43e5ed9d29f1499b"
    url= "http://api.openweathermap.org/data/2.5/weather"
    params= {"appid":weather_key, "q":city, "units":"metric", "lang":"it"}
    response = requests.get(url,params=params)
    weather= response.json()
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
    return final_str

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
    while True:
        now=datetime.datetime.now().time().replace(microsecond=0).strftime('%H:%M:%S')
        if alarm==now:
            winsound.PlaySound("alarmclock.wav", winsound.SND_ASYNC)
            break

def run_lucy():
    command= take_command()
    if "canzone" in command:
        talk("Quale canzone?")
        song=take_command()
        label.config(text=song,font=("Courier", 9))
        app.update()
        talk(song)
        song = song.replace(' ','+')
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + song)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        webbrowser.get().open("https://www.youtube.com/watch?v=" + video_ids[0])
        non_ascolto()
    elif "meteo" in command:
        talk("Quale città?")
        città=take_command()
        label.config(text=città,font=("Courier", 9))
        app.update()
        previsioni=get_weather(città)
        talk(previsioni)
        non_ascolto()
    elif "spegni" in command:
        label.config(text="\U0001F44B"+"\U0001F44B"+"\U0001F44B",font=("Courier", 9))
        app.update()
        tm.sleep(1)
        app.destroy()
        os.system("shutdown /s /t 1")
    elif "riavvia" in command:
        label.config(text="\U0001F44B"+"\U0001F44B"+"\U0001F44B",font=("Courier", 9))
        app.update()
        tm.sleep(1)
        app.destroy()
        os.system("shutdown /r /t 1")
    elif "batteria" in command:
        battery= psutil.sensors_battery()
        percent= battery.percent
        percent= str(percent)
        per= percent + "per cento"
        label.config(text=percent+"%",font=("Courier", 9))
        app.update()
        talk(per)
        non_ascolto()
    elif "timer" in command:
        talk("Di quanti minuti?")
        mi= take_command(tim=True)
        talk("Timer impostato")
        mi= mi*60
        i=0
        while mi>i:
            i+=1
            tm.sleep(1)
        winsound.PlaySound("alarmclock.wav", winsound.SND_ASYNC)
    elif "messaggio" in command:
        now=datetime.datetime.now().time()
        talk("Cosa vuoi scrivere?")
        mess=take_command(wam=True)
        talk("dimmi il numero")
        num= take_command(wan=True)
        print(type(num))
        print(num)
        pywhatkit.sendwhatmsg("+39" + num, mess, int(now.hour), int(now.minute)+2)
        width,height = pg.size()
        pg.click(width/2,height/2)
        pg.press("enter")
    elif "chi è" in command:
        wikipedia.set_lang("it")
        person= command.replace("chi è","")
        info= wikipedia.summary(person,2)
        label.config(text=person,font=("Courier", 9))
        app.update()
        talk(info)
        non_ascolto()
    elif "che cos'è" in command:
        wikipedia.set_lang("it")
        thing= command.replace("che cos'è","")
        info2= wikipedia.summary(thing,2)
        label.config(text=person,font=("Courier", 9))
        app.update()
        talk(info2)
        non_ascolto()
    elif "ore" in command:
        time= datetime.datetime.now().strftime('%H:%M') 
        label.config(text=time,font=("Courier", 9))  	
        app.update() 
        talk(time)
        non_ascolto()
    elif "giorno" in command:
        giorno= datetime.date.today().strftime("%d/%m/%Y")
        label.config(text=giorno,font=("Courier", 9))  	
        app.update() 
        talk(giorno)
        non_ascolto()
    elif "cerca su google" in command:
        talk('Cosa devo cercare?')
        search=take_command()
        label.config(text=search,font=("Courier", 9))  	
        app.update() 
        url= "https://www.google.com/search?q=" + search
        webbrowser.get().open(url)
        non_ascolto()
    elif "luogo" in command:
        talk('Quale luogo?')
        luogo=take_command()
        label.config(text=luogo,font=("Courier", 9))  	
        app.update() 
        url= "https://www.google.nl/maps/place/" + luogo +"/&amp"
        webbrowser.get().open(url)
        non_ascolto()
    elif "scrivi una nota" in command:
        talk('Cosa vuoi che scriva?')
        nota=take_command()
        note(nota)
    elif "apri google chrome" in command:
        subprocess.Popen(['C:\Program Files (x86)\Google\Chrome\Application\chrome.exe', '-new-tab'])
    elif "sveglia" in command:
        talk('A che ora?')
        orario=take_command()
        orario = orario.replace('alle', '')
        orario_x= datetime.datetime.strptime(orario, " %H:%M").time()
        label.config(text=orario_x,font=("Courier", 9))  	
        app.update() 
        sveglia(orario_x)
        non_ascolto()
    elif "emozioni" in command:
        talk("Ok , proviamo")
        emoz=take_command()
        respon=emotions(emoz)
        visual=respon.replace("Credo tu stia provando","")
        label.config(text=visual,font=("Courier", 9))  	
        app.update()
        talk(respon)
        non_ascolto()
    elif "chiuditi" in command:
        label.config(text="\U0001F44B"+"\U0001F44B"+"\U0001F44B",font=("Courier", 9))
        app.update()
        talk("Ok , ciao")
        app.destroy()
        sys.exit()
    elif "no" in command:
        label.config(text="\U0001F44B"+"\U0001F44B"+"\U0001F44B",font=("Courier", 9))
        app.update()
        talk("Ok , ciao")
        app.destroy()
        sys.exit()
    elif "ciao" in command:
        label.config(text="\U0001F60A"+"\U0001F60A"+"\U0001F60A",font=("Courier", 9))  	
        app.update()                  
        talk("Ciao, dimmi")
        run_lucy()
    else:
        label.config(text="\U0001F914"+"\U0001F914"+"\U0001F914",font=("Courier", 9))  	
        app.update()
        talk('Perfavore ripeti il comando')
        run_lucy()

app = tk.Tk()
app.title("Lucy by @11dome11")
app.geometry("790x580")
sfondo= tk.PhotoImage(file="sfondo.png")
app.iconbitmap('C:/Users/DOMENICO/dome/Python/SCRIPT/Lucy/robot.ico')
background= tk.Label(app, image=sfondo)
background.place(relheight=1, relwidth=1)
global label
label= tk.Label(app,padx=0,pady=0, text="",fg='Black',bg='white',relief="raised")
label.configure(width=24, height=4)
label.place(relx = 0.12,rely = 0.4,anchor = 'center')
button = tk.Button(app, text='START',fg='Black',bg='grey',command=lambda:[start(),again()],relief="raised",activebackground="grey")
button.configure(width=10, height=2)
button.place(relx = 0.1,rely = 0.1,anchor = 'center')
label1= tk.Label(app,text="LUCY \n AI Virtual Assistant",fg='blue',bg='Black',relief="raised",font=("Courier",10))
label1.configure(width=24, height=4)
label1.place(relx = 0.85,rely = 0.9,anchor = 'center')

app.mainloop()






