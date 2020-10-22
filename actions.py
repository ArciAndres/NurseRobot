from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
import requests
import json

# class ActionWeather(Action):
# 	def name(self):
# 		return 'action_weather'
		
# 	def run(self, dispatcher, tracker, domain):
# 		from apixu.client import ApixuClient
# 		api_key = '...' #your apixu key
# 		client = ApixuClient(api_key)
		
# 		loc = tracker.get_slot('location')
# 		current = client.getCurrentWeather(q=loc)
		
# 		country = current['location']['country']
# 		city = current['location']['name']
# 		condition = current['current']['condition']['text']
# 		temperature_c = current['current']['temp_c']
# 		humidity = current['current']['humidity']
# 		wind_mph = current['current']['wind_mph']

# 		response = """It is currently {} in {} at the moment. The temperature is {} degrees, the humidity is {}% and the wind speed is {} mph.""".format(condition, city, temperature_c, humidity, wind_mph)
						
# 		dispatcher.utter_message(response)
# 		return [SlotSet('location',loc)]
    
    
class ActionJoke(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_joke"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        request = json.loads(requests.get('https://api.chucknorris.io/jokes/random').text)  # make an api call
        joke = request['value']  # extract a joke from returned json response
        #dispatcher.utter_message(joke)  # send the message back to the user
        dispatcher.utter_message(joke)  # send the message back to the user
        return []

# request = json.loads(requests.get('https://api.chucknorris.io/jokes/random').text)  # make an api call
# joke = request['value']  # extract a joke from returned json response
# print(joke)

class ActionStatus(Action):
    def name(self):
        return "action_status"        
    def run(self, dispatcher, tracker, domain):
        status = tracker.get_slot('status')
        if status == 'pain':
            dispatcher.utter_message("That's not good. Let me get some medicine, and I will call a human to verify your condition.")
        if status == 'fine':
            dispatcher.utter_message("I'm glad")
        #if status == 'hungry'
            
        return []

class ActionCall(Action):
    def name(self):
        return "action_call"        
    def run(self, dispatcher, tracker, domain):
        callto = tracker.get_slot('callto')
        if callto == 'doctor':
            dispatcher.utter_message("I am calling the doctor right now.")
        if callto == 'ambulance':
            dispatcher.utter_message("It's an emergency! I am getting the closest ambulance for you now. Hold there!")
        if (callto != 'doctor' and callto != 'ambulance'):
            dispatcher.utter_message("Ok. I am calling your " + callto + " now.")
        return []