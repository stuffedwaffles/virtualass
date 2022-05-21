from __future__ import unicode_literals
from dataclasses import dataclass
import speech_recognition as sr
from time import time
from datetime import datetime
import os
from gtts import gTTS
import requests, json
import mpyg321
import keyboard
import os.path
from playsound import playsound
import json 
import requests
import random
import python_weather
import asyncio
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
import psutil
from plyer import notification
import spotipy
import webbrowser
import smtplib
import transformers
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
 
 
english_bot = ChatBot("computer", storage_adapter="chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(english_bot)
trainer.train("chatterbot.corpus.english")
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I am listening...")
        audio = r.listen(source)
    data = ""
    try:
        data = r.recognize_google(audio).lower()
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition did not understand audio")
        data = "not audio"
    except sr.RequestError as e:
        print("Request Failed; {0}".format(e))
        data = "not audio"
    return data
    

def respond(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='hi', slow=False)
    tts.save("speech.mp3")
    try:
        playsound("speech.mp3",True)
        os.remove("speech.mp3")
    except PermissionError:
        pass

 
 
listening = True
while listening == True:
    data = listen()
    respond(str(english_bot.get_response(data)))