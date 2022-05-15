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

secrets = json.load('secrets.json')

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


#email, notifications, meme?, covid stats, open other apps, call people

reminders = {}
comebacks = ["Stop pushing my buttons!", "You're such a wet sock.", "Calling you stupid would be an insult to all the stupid people.", "Sharp as a marble, that one.", "Maybe if you didn't talk like an idiot, I would be able to understand you.", "Well I don't like you either."]
greetings = ["Whats up?!", "How can I help you today?", "How you doin?", "Whatcha need?", "I am a computer!"]
goodbyes = ["Computer, out!", "Signing off!", "To infinity and beyond!", "Thats all folks!", "Blast off!"]
random_answers = ["I don't know what that means, but it sounds wonderful!", "Today is a great day to be a computer.", "I like trains.", "Give me a break, man!", "What the heck are you talking about?", "Are you talking to someone that isn't me?", "Well said.", "I only work in black. And very very dark gray"]
pickup_lines = ["you better call life support baby cause ive fallen for you and i cant get up", "are you helium cause you look high", "are you an endothermic reaction", "are you an overheating nuclear power plant cause youre looking pretty thermal", "you must be match fumes cause you take my breath away", "are you missing an electron because youre looking positively attractive", "theres a lot of elements on the periodic table but all i see is U and I", "hey baby id sacrifice my life for you like a charred nut on a paper clip","are you depleted plutonium because youre radioactive","hey you know my favorite element is uranium because its U", "are you uranium because i cant find you on ebay", "you must be the square root of negative one cause you cant be real", "cant help but notice youre the perfect person to have some dino nuggies with", "i might give up chicken for tofu but id never give you up", "roses are red, the copper two+ ion is blue, id love to have some dino nuggies with you", "to bean or not to bean", "So, did i ever tell you about that time I went backpacking in western Europe? Years ago, when I was backpacking across Western Europe. I was just outside Barcelona hiking in the foothills of Mount Tibidabo. I was at the end of this path and I came to a clearing and there was a lake, very secluded. And there were tall trees all around. It was dead silent. Gorgeous. And across the lake I saw…a beautiful woman…bathing herself…but she was crying…", "I'm a werewolf, and you're a full moon"]

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



def digital_assistant(data):

    if "computer" in data:
        listening = True
        respond(f"Hey {name}, {random.choice(greetings)}")
    
    elif "shut up" in data or "you suck" in data or "stupid" in data or "idiot" in data or "dumb" in data:
        listening = True
        respond(random.choice(comebacks))


    elif "hello" in data or "hi" in data or "hey" in data:
        listening = True
        respond("Hey man!")
    
    elif "browser" in data:
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
 
    elif "help" in data:
        listening = True
        respond("You can ask me: my name, how I am, the time, pickup lines, jokes, the weather, to google something, to remind you to do something, the battery, to start a timer, start a stopwatch, play a song, open a browser, or say stop listening to turn me off")

    elif "name" in data:
        listening = True
        respond(f"My name is computer, and your's is {name}!")

    elif "how are you" in data:
        listening = True
        respond("I'm doing good, how are you?")
    
    elif "good" in data or "great" in data:
        listening = True
        respond("Thats great!")
    
    elif "bad" in data:
        listening = True
        respond("Whats wrong?")

    elif "what time is it" in data:
        listening = True
        respond(datetime.now())
    
    elif "pick up line" in data:
        listening = True
        respond(random.choice(pickup_lines))
    
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

    elif "stop listening" in data:
        listening = False
        respond(random.choice(goodbyes))
        return listening
    
    elif "thank" in data:
        listening = True
        respond("You're welcome!")
    
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
            try:
                limit = int(listen())
            except ValueError:
                respond("Sorry, I didn't get that, so I'm going with 3.")
                limit = 3
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


    elif "homework" in data:
        listening = True
        respond("Who needs homework?")
    
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
        try:
            limit = int(listen())
        except ValueError:
            respond("Sorry, I didn't get that, so I'm going with 3.")
            limit = 3
        index = 0
        for item in output:
            index +=1
            if index == limit:
                    break
            for key,value in item.items():
                respond(key)
                respond(value)
    
    elif "remind me to" in data:
        listening = True
        data_l = data.split(" ")
        data_l.remove("remind")
        data_l.remove("me")
        data_l.remove("to")
        reminder = "".join(data_l)
        time = datetime.now()
        reminders[reminder] = time.hour
        respond("Reminder added to the list! you will be reminded in an hour.")
    
    elif "battery" in data:
        listening = True
        battery = psutil.sensors_battery()
        percent = battery.percent
        plug = battery.power_plugged
        
        respond(f"Battery percentage is {percent}. Plugged in status: {plug}")


    elif "not audio" in data:
        listening = True
        num = random.randint(0,5)
        if num == 3:
            respond("Bless you!")
        else:
            pass
    
    elif "start timer" in data:
        import time
        listening = True
        data_l = data.split(" ")
        data_l.remove("timer")
        data_l.remove("start")
        unit = data_l[1]
        times = int(data_l[0])
        respond(f"Timer for {times} {unit} started.")
        if "min" in unit:
            time.sleep(60*times)
        elif "h" in unit:
            time.sleep(60*60*times)
        elif "sec" in unit:
            time.sleep(times)
        
        respond("Ring ring! Timer over.")
    
    elif "stopwatch" in data:
        listening = True
        time = 0
        respond("Stopwatch started. say stop to stop.")
        while True:
            if time > 3600:
                respond("Stopwatch has been running too long and has been stopped.")
                break
            time.sleep(1)
            time += 1
            data = listen()
            if data == "stop":
                if time > 60:
                    time = time/60
                    respond(f"Stopwatch ran for {time} minutes")
                else:
                    respond(f"Stopwatch ran for {time} seconds")
                break
            else:
                continue
    elif "play" in data:
        listening = True
        data_l = data.split(" ")
        data_l.remove("play")
        searchQuery = "".join(data_l)
        searchResults = spotifyObject.search(searchQuery,1,0,"track")
        # Get required data from JSON response.
        tracks_dict = searchResults['tracks']
        tracks_items = tracks_dict['items']
        song = tracks_items[0]['external_urls']['spotify']
        # Open the Song in Web Browser
        webbrowser.open(song)
        respond(f'Song results for {searchQuery} have opened in your browser.')


    elif "covid" in data:
        # generic US covid data
        listening = True
        webbrowser.open("https://covid.cdc.gov/covid-data-tracker/#datatracker-home")
        respond("Covid data has been opened in your browser.")


    else:   
        listening = True
        # num = random.randint(0,5)
        # if num == 3:
        respond(random.choice(random_answers))

        # else:
        #     pass
        

    return listening

listening = True
start = datetime.now()
while listening == True:
    data = listen()
    listening = digital_assistant(data)
    time.sleep(1)
    if reminders != {}:
        for reminder, hour in reminders.items():
            if datetime.now().hour - hour >= 1:
                notification.notify(
                    title="Reminder",
                    message=str(reminder),
                    timeout=10
                )