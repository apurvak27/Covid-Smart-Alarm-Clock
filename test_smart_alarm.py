"""Module to test the functionality including unit-testing"""


import unittest
import json 
import requests 
import smart_alarm 


def test_api():
    #Tests the Restful API Calls and the Documentation to ensure that it runs smoothly 
    news = request.args.get(smart_alarm.get_news())
    weather = request.args.get(smart_alarm.get_weather())
    assert weather.status_code == 200
    assert news.status_code == 200
    

class TestWeather(unittest.TestCase):
    # Unit tests the get_weather function 

    def test_weather_none(self) -> None:
        #Tests the weather function to check it returns a value and is not none 
        weatherdict = smart_alarm.get_weather()
        self.assertIsNotNone(weatherdict)

    def test_news_none(self) -> None:
        #Tests the news function to check it returns a value and is not none 
        newsdict = smart_alarm.get_news()
        self.assertIsNotNone(newsdict)

    def test_covid_none(self) -> None:
        #Tests the covid function to check it returns a value and is not none 
        covid_dict = smart_alarm.get_covid()
        self.assertIsNotNone(covid_dict)




if __name__ == "__main__":
    test_api()
    unittest.main()