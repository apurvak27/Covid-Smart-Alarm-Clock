# CA3 - Deployment and Documentation 

Information for User: 

This app is a smart alarm clock that includes updates of weather, news and covid-19 statistics. The alarm can announce these three updates as soon as it is triggered and the time for setting the alarm can be set and removed by the user. Additionally, text-based silent notifications containting the top headline, weather and covid statistic will be refreshed constantly throughout the time the user is engaging with the app and these notifications can also be dismissed. 

In order to run this app the user must install:
- Python Version 3.7 (or above). This is because it should include essential packages like json, logging, time, sched 

The user then must proceed to install: 
- pyttsx3
- flask 
- uk_covid19
- requests 

This can be done by running install on the command line:
$ pip install pyttsx3 
$ pip install flask 
$ pip install uk_covid19 
$ pip install requests 

Following this, the user should collect their personal API Keys in order to import the JSON Files 
From https://newsapi.org/, and https://openweathermap.org/current the user can create an individual account on both platforms and collect their API Keys 

The user can open the config.json file and input their API keys inside quotation marks in the area that says "news" and "weather" respectively. 
It is also possible to alter the city in the UK that they live in by changing the name of the city next to "city":
Currently the default city is set as Exeter. 

To finall run the program the user has to save this information on the config file and then proceed to the terminal
At the terminal they should enter: 
$ python3 smart_alarm.py and it should display this below: 

* Serving Flask app "smart_alarm" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Debug mode: on

If the link, does not show up the user can proceed to the logs.log file and find the respective link. An example of this is shown below: 
- 2020-12-18 18:33:41,395 INFO: Refresh Smart Alarm Clock
- 2020-12-18 18:33:41,406 INFO: Getting covid-19 cases and deaths updates from covid-19 API
- 2020-12-18 18:33:48,068 INFO: Returning Covid-19 Cases and Deaths Updates from Covid-API
- 2020-12-18 18:33:48,068 INFO: Getting Weather Updates from Weather API
- 2020-12-18 18:33:48,324 INFO: Returning Weather Updates from Weather API
- 2020-12-18 18:33:48,324 INFO: Getting News Updates from News API
- 2020-12-18 18:33:48,842 INFO: Returning News Updates from News API
- 2020-12-18 18:33:48,948 INFO:  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)



The user can copy the link http://127.0.0.1:5000/ and paste this into a browser (specifically Google Chrome) and all of the functionality can be executed from there. 

In order to quit/leave the broswer and app the user must press (control + c) into the terminal window 

Information for the Developer: 
- Testing can be carried out from the test_smart_alarm.py module where all of the API's and functionality can be tested. By entering the following into the terminal when reached file;
$ python3 -m pytest 

The code is structured in such a way that all of the functionality is in present in smart_alarm.py. 
- The template folder contains the HTML template "template.html" which is used to render the webpage 
- The static/images folder contains the image 'clock.jpg' which renders the image 
- The config.json file contains all of the private information such as API-Keys, location and also the path to the log file 
- log.logs logs all of the events that take place in the web page
- The main module smart_alarm.py contains all of the functions including get_weather(), get_news(), get_covid() which are needed to retrieve the dictionary values. All of the functions for the functionality of the alarms and notification are also in this file. 

If as a developer you would like to edit the information that is recieved from the dictionaries, it is possible to edit the get_news(), get_covid() and get_weather() functions from the smart_alarm.py module but it is also possible to apply filters to them in the config.json file. Additionally, it is also possible to contniually pass multiple notifications of news through by converting it as a list but this could overwhelm the user and provide unnecessary information. Further extensions and developments can also be done through editing the main smart_alarm.py module 




