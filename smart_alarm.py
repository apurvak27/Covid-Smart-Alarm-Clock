"""
A smart alarm clock presented by a bootstrap web interface, using the Flask Module in Python. 
It contains information about the latest Weather, News and Covid-19 cases in the region set in the config.json file. 
The user is able to select and cancel alarms for which an announcement goes off and passively recieve notifications.
"""
import pyttsx3
import time
import sched
from uk_covid19 import Cov19API
from flask import Flask, request, render_template
import json
import requests
import logging


with open("config.json", "r") as file:
    #Opens the confid.json file and accordingly extracts the information needed to access the JSON files 
    


    config = json.load(file)
    api_keys = config["api_keys"]
    file_paths = config["file_paths"]
    location = config["location"]

#Global variables of alarms and notification in the forn of a list 
notifications = []
alarms = []

logging.basicConfig(filename=file_paths["logging"], level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s")

#Intialises the scheduler for the alarm
s = sched.scheduler(time.time, time.sleep) 

logging.info("Refresh Smart Alarm Clock")
#Initalises Flask for web-interface 
app = Flask(__name__)


def get_weather() -> dict:
    """Returns a dictionary containing the description of the current weather"""
    logging.info("Getting Weather Updates from Weather API")
    weatherdict = {}
    weather_key = api_keys["weather"]
    city = location["city"]
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + weather_key + "&q=" + city 

    raw_weather = requests.get(complete_url)
    weather = raw_weather.json()
    round_temp = round(int(weather["main"]["temp"]- 273.15))
    temp = str(round_temp)
    description = weather["weather"][0]["description"].capitalize()


    weather_description = "The temperature is " + temp + "°C" + " , Conditions: " + description
    weatherdict = {"title": "Weather Update", "content": weather_description}

    logging.info("Returning Weather Updates from Weather API")

    return weatherdict


def get_news() -> dict: 
    """Returns a dictionary containing the current top news story either from the BBC or a story containing information regarding the coronavirus pandemic"""
    logging.info("Getting News Updates from News API")


    news_key = api_keys["news"]
    country = location["country"]
    news_api = ("https://newsapi.org/v2/top-headlines?"
                "country={}&apiKey={}").format(country,news_key)

    #Get data for raw news 
    raw_news = requests.get(news_api)
    news = raw_news.json()
    articles = news["articles"]
    newsdict = {}
    for article in articles:
        if 'BBC News' in article["source"]["name"] or 'coronavirus' or 'covid' in article['content'].lower():
            newsdict = {"title": "News Update", "content": str(article["title"])}

    logging.info("Returning News Updates from News API")

    return newsdict


def get_covid() -> dict:
    """Returns a dictionary containing the daily and total covid cases,daily and total covid deaths"""
    logging.info("Getting covid-19 cases and deaths updates from covid-19 API")


    covid_dict = {}


    cases_and_deaths = {
    "date": "date",
    "areaName": "areaName",
    "areaCode": "areaCode",
    "newCasesByPublishDate": "newCasesByPublishDate",
    "cumCasesByPublishDate": "cumCasesByPublishDate",
    "newDeathsByDeathDate": "newDeathsByDeathDate",
    "newDeaths28DaysByPublishDate": "newDeaths28DaysByPublishDate",
    "cumDeaths28DaysByPublishDate": "cumDeaths28DaysByPublishDate"
    }

    england_only = ['areaName=England']


    api = Cov19API(filters = england_only, structure = cases_and_deaths)
    data = api.get_json()
    covid_data = data["data"]


    if int(covid_data[0]["newCasesByPublishDate"]) >= 50:
        threshold = "There is a significant jump in the number of cases by "
    else:
        threshold = "There is not a slight jump in the number of cases by "
    if str(covid_data[0]["newDeathsByDeathDate"]) == "None":
        limit = "There have been no new recorded deaths today bringing the total deaths to "
    else: 
        limit = "There have been recorded deaths today bringing the total deaths to "

    new_count = str(covid_data[0]["newCasesByPublishDate"])
    total_count = str(covid_data[0]["cumCasesByPublishDate"])
    total_death = str(covid_data[0]["cumDeaths28DaysByPublishDate"])

    count_description = threshold + new_count + "." + " Bringing the total number of cases to " + total_count + ". " + limit + total_death + "."

    covid_dict = {"title": "Covid-19 Update", "content": count_description}

    logging.info("Returning Covid-19 Cases and Deaths Updates from Covid-API")

    return covid_dict

def get_notification():
    logging.info("Collecting Notifications")
    """Appends the notifications to show the current statistics"""
    notifications.append(get_covid())
    notifications.append(get_weather())
    notifications.append(get_news())


def refresh_notification():
    logging.info("Refreshing notifications")
    """Refreshes the notifications every 30 minutes for the main page"""
    s.run(blocking=False)
    s.enter(1800,1,get_notification())
    refresh_notification()
    logging.info("Enter the Patients Weight")


def run_alarm (text: str):
    """Executes a text-to-speech command

    Keyword Arguments: 
    Text - This a string value of the text that is supposed to be executed
    """
    logging.info("Preparing to execute text_to_speech command")
    text_to_speech = pyttsx3.init()
    text_to_speech.say(text)
    text_to_speech.runAndWait()

def alarm_repeat (alarm_time: str) -> str:
    """Used for combining the alarm_time and label when it is displayed

    Keyword Argument:
    alarm_time - This is a string of the scheduled time when alarm is supposed to be announced
    """
    alarm_time = alarm_time.replace("T", " ")
    alarm_time = alarm_time.replace("+", " ")

    return alarm_time

def announce(alarm_time: str):
    """Conducts the speech of the announcement for the alarm/ what it will speak when it goes off

    Keyword Argument:
    alarm_time - This is a string of the scheduled time when the alarm is supposed to be announced
    """
    alarm = get_alarm(alarm_time)
    text_to_speech.say(("Your alarm with label", alarm_label, "is going off"))

    logging.info("Alarm for Covid-Updates is going off")

    covid_data = get_covid_data()

    text = covid_data["content"]
    text_to_speech.say((text))

    if alarm["news"]:
        logging.info("Alarm for News is going off")
        news = get_news()
        text = news["content"]
        text_to_speech.say(("News Update"))
        text_to_speech.say((text))

    if alarm["weather"]:
        logging.info("Alarm for Weather is going off")
        weather = get_weather()
        text = weather["content"]
        text_to_speech.say(("Weather Update"))
        text_to_speech.say((text))


def add_alarm(alarm_time: str, alarm_label: str, news: str, weather: str):
    """Enables an alarm to be added

    Keyword Arguments:
    alarm_time - This is a string of the scheduled time when the alarm is supposed to be announced
    alarm_label- This is a string of the label given by the user input 
    news- This is a string containing the news information
    weather- This is a string containing the weather information 
    """

    time_stamp = "%Y-%m-%d %H:%M"
    alarm_set = time.mktime(time.strptime(alarm_time, time_stamp))

    event = s.enterabs(alarm_set, 1, announce, argument=(alarm_time,))

    alarm_dict = {
            "title": alarm_time,
            "content": alarm_label,
            "event": event,
            "news": news,
            "weather": weather
            }
    logging.info("New Alarm Added")
    alarms.append(alarm_dict)


def get_alarm(alarm_time: str) -> dict:
    """Returns the dictionary for the alarm stored in the list which will later be spoken 

    Keyword Arguments:
    alarm_time - This is a string of the scheduled time when the alarm is supposed to be announced
    """
    for alarm in alarms:
        if alarm["title"] == alarm_time:
            logging.info("Alarm stored")
            return alarm



app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    """Renders the HTML Template to display on webpage from the index page"""

    alarm_time = request.args.get("alarm")
    alarm_label = request.args.get("two")
    news = request.args.get("news")
    weather = request.args.get("weather")
    alarm_identifier = request.args.get("alarm_item")
    notification_name = request.args.get("notif")

    #Combines the label and inputs given by the user for the addition of alarm 
    if alarm_time and alarm_label:
        alarm_time = alarm_repeat (alarm_time)
        add_alarm(alarm_time, alarm_label, news, weather)
        logging.info("Scheduled alarm created with label")

    #Allows user to delete alarms by clicking 'x'
    if alarm_identifier:
        alarms[:] = [x for x in alarms if x.get('title')!= alarm_identifier]
        logging.info("Alarm Removed")

    #Allows user to delete notifications by clicking 'x'
    if notification_name:
        notifications[:] = [x for x in notifications if x.get("title")!= notification_name]
        logging.info("Notification Removed")

    logging.info("Render Template with HTML")
    #Returns the variables to the HTML file to render template webpage 
    return render_template("template.html", title= "Smart Alarm Clock", image = "clock.jpg", alarms = alarms,
            notifications= notifications)

#Ensures the display of the notifications on the web-server 
notifications.append(get_covid())
notifications.append(get_weather())
notifications.append(get_news())

#Prevents the code from executing when the script is imported as a module
if __name__ == "__main__":
    app.run(debug =True)
    #Refreshes notifications while code is being executed 
    refresh_notification()
