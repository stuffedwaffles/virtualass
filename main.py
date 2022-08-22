from __future__ import unicode_literals
from dataclasses import dataclass
import speech_recognition as sr
import time
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
nlp = transformers.pipeline("conversational", 
                            model="microsoft/DialoGPT-medium")
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
 
 
#THOUGHTS
#connection reset error- what is it and why
# off option where you say stop listening and when that happens then a new variable stopped = true and listening still = true but stopped also = true so we can have a while stopped = true then dont do anything except listen for computer/wakeup call which can be part of a function and then when that happens stopped = false



english_bot = ChatBot("computer", storage_adapter="chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(english_bot)
trainer.train("chatterbot.corpus.english")


json_file_path = r"stuf\actual projects\asssecrets.json"

with open(json_file_path, 'r') as j:
     secrets = json.loads(j.read())


username = secrets["username"]
clientID = secrets["clientID"]
clientSecret = secrets["clientSecret"]
name = secrets["name"]
city = secrets["city"]

redirectURI = 'http://google.com/'
# Create OAuth Object
oauth_object = spotipy.SpotifyOAuth(clientID,clientSecret,redirectURI)
# Create token
token_dict = oauth_object.get_access_token()
token = token_dict['access_token']
# Create Spotify Object
spotifyObject = spotipy.Spotify(auth=token)
user = spotifyObject.current_user()


#notifications, meme?, open other apps, call people
responses = [
    {"patterns": ["Hi", "How are you", "Is anyone there?", "Hello", "Good day", "computer", "whats up"],
     "responses": ["Hello, thanks for visiting", "Good to see you again", "Hi there, how can I help?", "Whats up?!", "How can I help you today?", "How you doin?", "Whatcha need?", "I am computer!"],
    },
    {"tag":"bye",
     "patterns": ["Bye", "See you later", "Goodbye", "go away", "stop listening"],
     "responses": ["See you later, thanks for visiting", "Have a nice day", "Bye! Come back again soon.", "Computer, out!", "Signing off!", "To infinity and beyond!", "Thats all folks!"]
    },
    {
     "patterns": ["Thanks", "Thank you", "That's helpful"],
     "responses": ["Happy to help!", "Any time!", "My pleasure"]
    },
    {
     "patterns":["shut up", "you suck", "you're stupid", "you're an idiot", "you're dumb"],
     "responses":["Stop pushing my buttons!", "You're such a wet sock.", "Calling you stupid would be an insult to all the stupid people.", "Sharp as a marble, that one.", "Well I don't like you either.", "I hope you sleep on a twin sized mattress for the rest of your life."]
    },
    {
    "patterns": ["tell me a pick up line", "pick up line"],
    "responses":["you better call life support baby cause ive fallen for you and i cant get up", "are you helium cause you look high", "are you an endothermic reaction", "are you an overheating nuclear power plant cause youre looking pretty thermal", "you must be match fumes cause you take my breath away", "are you missing an electron because youre looking positively attractive", "theres a lot of elements on the periodic table but all i see is U and I", "hey baby id sacrifice my life for you like a charred nut on a paper clip","are you depleted plutonium because youre radioactive","hey you know my favorite element is uranium because its U", "are you uranium because i cant find you on ebay", "you must be the square root of negative one cause you cant be real", "cant help but notice youre the perfect person to have some dino nuggies with", "i might give up chicken for tofu but id never give you up", "roses are red, the copper two+ ion is blue, id love to have some dino nuggies with you", "to bean or not to bean", "So, did i ever tell you about that time I went backpacking in western Europe? Years ago, when I was backpacking across Western Europe. I was just outside Barcelona hiking in the foothills of Mount Tibidabo. I was at the end of this path and I came to a clearing and there was a lake, very secluded. And there were tall trees all around. It was dead silent. Gorgeous. And across the lake I saw…a beautiful woman…bathing herself…but she was crying…I hesitated, watching, struck by her beauty. And also by how her presence; the delicate curve of her back, the dark sweep of her hair, the graceful length of her limbs, even her tears, added to the majesty of my surroundings. I felt my own tears burning behind my eyes, not in sympathy, but in appreciation of such a perfect moment. She spied me before I could compose myself. But she didn't cry out. Instead our eyes held and she smiled, enigmatically, fresh tears still spilling down her cheeks. I was frozen. I knew nothing about this woman, and yet, as we stood on opposite sides of a pool of water, thousands of miles from my own home and everyone I had ever known, I felt the most intense connection. Not just to her, but to the earth, the sky, the water between us. And also to the entirety of mankind. As if she symbolized thousands of years of the human condition. I wanted to go to her, to comfort her, to probe this feeling of belonging I had never encountered before. But I couldn't. Because I knew that if I spoke, if she spoke, that moment would be ruined. And I knew I would need the memory of that moment to carry me through the inevitable dark patches throughout my life. And so I watched her lower her hand, turn, and slowly walk to the shore opposite me. The rest of her perfect form was gradually revealed to me, and I held my breath as I watched her disappear behind a copse of trees near the water. I didn't follow her, in fact I turned around. I knew there was nothing else we could experience together that would be more perfect than that moment...and it still remains the most profound experience of my life", "You're a flashlight in a dark room in the loneliest blackout", "are you mr rushins root beer cause you make me high", "my name is computer but you can call me.... anytime", "are you a toaster cause id love to take a bath with you", "did it hurt when you fell from the vending machine? cause you look like a snack", "if you were a planet, you'd be venus cause you're the hottest one in the solar system", "youre hotter than the bottom of my computer"]
    },
    {
    "patterns":["what can you do", "help", "what are your functions"],
    "responses":["You can ask me: my name, how I am, the time, pickup lines, jokes, the weather, to google something, to remind you to do something, the battery, to start a timer, start a stopwatch, play a song, open a browser, send an email, or say stop listening to turn me off. You can also talk to me!"]
    },
    {
    "patterns":["what is your name", "who are you", "what are you"],
    "responses":["I am computer!", "my name is computer", "I'm a computer for you to talk to"]
    }
]


reminders = {}

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I am listening... (hit ctrl+c or say stop listening to turn me off)")
        audio = r.listen(source)
    data = ""
    time.sleep(2)
    try:
        data = r.recognize_google(audio).lower()
        print("You said: " + data)
    except ConnectionResetError:
        print("Connection error.")
        data = "not audio"
    except sr.UnknownValueError:
        print("Google Speech Recognition did not understand audio")
        data = "not audio"
    # except sr.RequestErrror as e:
    #     print("Request Failed; {0}".format(e))
    #     data = "not audio"
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



def digital_assistant(data):

    for dictionary in responses:
        if data in dictionary["patterns"]:
            respond(random.choice(dictionary["responses"]))
        try:
            thing = type(dictionary["tag"])
            listening = False
        except:
            listening = True
    
    if "browser" in data:
        listening = True
        webbrowser.open("https://www.google.com/")
        respond("Browser opened!")
    
    elif "open" in data:
        listening = True
        data_l = data.split(" ")
        data_l.remove("open")
        app = "".join(data_l)
        try:
            os.system(f"{app}")
            respond(f"{app} opened.")
        except:
            respond("Sorry, I couldn't find that app. Try another one.")

    elif "time" in data and "what" in data:
        listening = True
        respond(str(datetime.now()))
    
    elif "joke" in data:
        listening = True
        subreddit = 'Jokes'
        limit = 100
        timeframe = 'month' #hour, day, week, month, year, all
        listing = 'top' # controversial, best, hot, new, random, rising, top

        try:
            base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
            request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
        except:
            print('An Error Occured')

        r = request.json()
        posts = []
        for post in r['data']['children']:
            x = post['data']['title']
            y = post['data']['selftext']
            posts.append({x:y})


        joke_answer = random.choice(posts)
        for k,v in joke_answer.items():
            respond(k)
            respond(v)

    
    elif "weather" in data:
        async def weather():
            # declare the client. format defaults to metric system (celcius, km/h, etc.)
            client = python_weather.Client(format=python_weather.IMPERIAL)
            # fetch a weather forecast from a city
            weather = await client.find(city)
            # returns the current day's forecast temperature (int)
            temp = weather.current.temperature
            # get the weather forecast for a few days
            respond("How many days of weather would you like to hear? ")
            while True:
                limit = listen()
                if limit == "not audio":
                    continue
                elif "stop" in limit:
                    return listening
                try:
                    int(limit)
                except ValueError:
                    continue
                else:
                    break
                    

            index = 0
            for forecast in weather.forecasts:
                index +=1
                if index == limit:
                        break
                date = str(forecast.date)
                sky = forecast.sky_text
                temp = forecast.temperature
                respond(f"{date}: sky forecast is {sky}, temp forecast is {temp}")
                if index == limit:
                    await client.close()
                    respond("Current temperature: " + temp)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(weather())
        listening = True


    
    elif "google" in data:
        listening = True
        data_l = data.split(" ")
        data_l.remove("google")
        query = "".join(data_l)
        query = urllib.parse.quote_plus(query)
        try:
            session = HTMLSession()
            response = session.get("https://www.google.co.uk/search?q=" + query)
        except requests.exceptions.RequestException as e:
            print(e)
        links = list(response.html.absolute_links)
        google_domains = ('https://www.google.', 
                        'https://google.', 
                        'https://webcache.googleusercontent.', 
                        'http://webcache.googleusercontent.', 
                        'https://policies.google.',
                        'https://support.google.',
                        'https://maps.google.')

        for url in links[:]:
            if url.startswith(google_domains):
                links.remove(url)

        css_identifier_result = ".tF2Cxc"
        css_identifier_title = "h3"
        # css_identifier_link = ".yuRUbf a"
        css_identifier_text = ".VwiC3b"
        results = response.html.find(css_identifier_result)
        output = []
        for result in results:
            try:
                item = {
                    'title': result.find(css_identifier_title, first=True).text,
                    # 'link': result.find(css_identifier_link, first=True).attrs['href'],
                    'text': result.find(css_identifier_text, first=True).text
                }
            except AttributeError:
                item = {
                    'title': result.find(css_identifier_title, first=True).text
                }
            
            output.append(item)
        respond("How many results would you like to hear? ")
        while True:
            limit = listen()
            if limit == "not audio":
                continue
            elif "stop" in limit:
                return listening
            try:
                int(limit)
            except ValueError:
                continue
            else:
                break
        index = 0
        for item in output:
            index +=1
            if index == limit:
                    break
            for key,value in item.items():
                respond(key)
                respond(value)
    
    elif "remind me" in data:
        listening = True
        respond("What do you need to be reminded? ")
        while True:
                reminder = listen()
                if reminder == "not audio":
                    continue
                else:
                    break
        time = datetime.now()
        reminders[reminder] = time.hour
        respond("Reminder added to the list! you will be reminded in an hour.")
    
    elif "battery" in data and "what" in data:
        listening = True
        battery = psutil.sensors_battery()
        percent = battery.percent
        plug = battery.power_plugged
        
        respond(f"Battery percentage is {percent}. Plugged in status: {plug}")
    
    elif "start timer" in data:
        import time
        listening = True
        respond("How long do you want your timer? Please respond with the number and then unit of time. ")
        while True:
                time_to_wait = listen()
                if time_to_wait == "not audio":
                    continue
                elif "stop" in time_to_wait:
                    return listening
                else:
                    break
        time_unit = time_to_wait.split(" ")
        unit = time_unit[1]
        time_to_wait = time_unit[0]
        respond(f"Timer for {time_to_wait} {unit} started.")
        if "min" in unit:
            time.sleep(60*time_to_wait)
        elif "h" in unit:
            time.sleep(60*60*time_to_wait)
        elif "sec" in unit:
            time.sleep(time_to_wait)
        
        respond("Ring ring! Timer over.")
    elif "stopwatch" in data:
        listening = True
        time_waited = 0
        respond("Stopwatch started. say stop to stop.")
        while True:
            if time_waited > 3600:
                respond("Stopwatch has been running too long and has been stopped.")
                break
            time.sleep(1)
            time_waited += 1
            data = listen()
            if data == "stop":
                if time_waited > 60:
                    time_waited = time_waited/60
                    respond(f"Stopwatch ran for {time_waited} minutes")
                else:
                    respond(f"Stopwatch ran for {time_waited} seconds")
                break
            else:
                continue

    elif "play song" in data:
        listening = True
        respond("What song would you like to play? ")
        while True:
                query = listen()
                if query == "not audio":
                    continue
                else:
                    break
        searchResults = spotifyObject.search(query,1,0,"track")
        # Get required data from JSON response.
        tracks_dict = searchResults['tracks']
        tracks_items = tracks_dict['items']
        song = tracks_items[0]['external_urls']['spotify']
        # Open the Song in Web Browser
        webbrowser.open(song)
        respond(f'Song results for {query} have opened in your browser.')


    elif "covid data" in data:
        # generic US covid data
        listening = True
        webbrowser.open("https://covid.cdc.gov/covid-data-tracker/#datatracker-home")
        respond("Covid data has been opened in your browser.")

    elif "send email" in data:
        listening = True
        FROM = 'anikag006@gmail.com'

        respond("Who would you like to email(please say the email address)? ")
        while True:
            email = listen()
            if email == "not audio":
                continue
            else:
                break
        
        email = email.split(" ")
        for index in range(len(email)):
            if email[index] == "at":
                email[index] = "@"
            elif email[index] == "dot":
                email[index] = "."
        email = "".join(email)
        full_email = ["email"]
        full_email[0] = email

        TO = full_email # must be a list
        respond("What would you like the subject to be? ")
        while True:
            sub = listen()
            if sub == "not audio":
                continue
            else:
                break
        SUBJECT = sub

        respond("What would you like the text to be? ")
        while True:
            txt = listen()
            if txt == "not audio":
                continue
            elif "stop" in txt:
                return listening
            else:
                break
        TEXT = txt

        # Prepare actual message

        message = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

        # Send the mail

        server = smtplib.SMTP('localhost')
        server.sendmail(FROM, TO, message)
        server.quit()

    elif "not audio" in data:
        listening = True
        pass

    else:   
        # nlp(transformers.Conversation(data), pad_token_id=50256)
        # chat = nlp(transformers.Conversation(data), pad_token_id=50256)
        # res = str(chat)
        # res = res[res.find("bot >> ")+6:].strip()
        # respond(res)

        #for dict in the responses, if the data matches one then it responds and tries for a goodbye, otherwise it responds with ai thing
        for dictionary in responses:
            if data in dictionary["patterns"]:
                respond(random.choice(dictionary["responses"]))

                #checks for a tag to see if its goodbye
                try:
                    thing = type(dictionary["tag"])
                    listening = False
                #except no tag then just continue
                except:
                    listening = True
            else:
                listening = True
                respond(str(english_bot.get_response(data)))
                
        
    return listening

listening = True
start = datetime.now()
while listening == True:
    data = listen()
    print(f"data: {data}")
    listening = digital_assistant(data)
    time.sleep(3)
    if reminders != {}:
        for reminder, hour in reminders.items():
            if datetime.now().hour - hour >= 1:
                notification.notify(
                    title="Reminder",
                    message=str(reminder),
                    timeout=10
                )