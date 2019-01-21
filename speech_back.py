import speech_recognition as sr
from gtts import gTTS
#quiet the endless 'insecurerequest' warning
import urllib3
import os
import win32com.client as wincl

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
 
from pygame import mixer
mixer.init()
speak = wincl.Dispatch("SAPI.SpVoice")

while (True == True):
# obtain audio from the microphone
  r = sr.Recognizer()
  with sr.Microphone() as source:
    #print("Please wait. Calibrating microphone...")
    # listen for 1 second and create the ambient noise energy level
    r.adjust_for_ambient_noise(source, duration=1)
    print("Say something!")
    audio = r.listen(source,phrase_time_limit=5)
 
# recognize speech using Sphinx/Google
  try:
    #response = r.recognize_sphinx(audio)
    response = r.recognize_google(audio)
    print("I think you said '" + response + "'")
    speak.Speak(response)
   # os.remove(responseFile)
 
  except sr.UnknownValueError:
    print("Sphinx could not understand audio")
  except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))