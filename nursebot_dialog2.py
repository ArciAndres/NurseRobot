
# coding: utf-8

# # AI(2A) - Human Robot Interaction Project
# # 👩‍⚕️  Nurse Robot

# ## Introduction
# This script implements a Spoke Dialog System (SDS) based on Spoken Natural Language Dialog in the context of an automated home nurse assistant, to be used by people with limited capabilities. It simulates actions such as reaching things, provide meals and inspect patient status. The system acquires a spoken input from the user through Google Speech Recognition API. Then, recognizes the intent of the sentence using Rasa NLU and retrieves and action result that is transmitted to the user through VocalWare Text-To-Speech API. The order of the sentences, and the recognition of the utterances and dependencies is processed by the libraries spaCy and Keras, building a model that returns the adequate actions given a series of inputs. 

# ![title](images/NurseRobotMindmap.png)

# In[1]:


#imports for project

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import rasa_core
from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_nlu.model import Metadata, Interpreter
from rasa_core.utils import EndpointConfig
from rasa_core.run import serve_application
from rasa_nlu.model import Trainer
from rasa_nlu.training_data import load_data
from rasa_core import config
from IPython.display import IFrame
import pandas as pd
import ruamel
import urllib.request
from urllib.request import urlopen
from playsound import playsound
import uuid
import speech_recognition as sr
import os
import spacy
from spacy import displacy
import warnings
warnings.simplefilter('ignore', ruamel.yaml.error.UnsafeLoaderWarning)
warnings.filterwarnings("ignore",category=DeprecationWarning)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #To ignore Tensorflow AVX AVX2 bonary warning

nlp = spacy.load('en')


# Some of the data used in this project is not shown in this notebook, but in external files. The content of each relevant file is described hereunder.
# 
# * nurse_domain.yml: Defines the actions that can be taken by the agent, the intents that are expected, the entities to be saved if received, and some answers to the basic user utterances.
# * stories.md: Contains the examples of dialogs and the specification of the entities that could be found on the phrases.
# * config_spacy.json: Saves the pipeline to be used by the NLP library, in this case sklearn with spaCy 
# 

# In[2]:


# Declare paths
domain_file = './nurse_domain.yml'
model_path = './models/dialogue'
interpreter_path ='./models/nursebot/interpreter'
training_data_file = './data/stories.md'
conf_file = './config_spacy.json'


# In[3]:


# Build the interpreter of the elements of dialog for the agent. If it doesn't work on the notebook, try on an external console
#!python -m rasa_nlu.train -c config_spacy.json --data data/data.md -o models --fixed_model_name interpreter --project nursebot --verbose


# In[3]:


action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
interpreter = RasaNLUInterpreter(interpreter_path)


# In[5]:


if False:
    agent = Agent(domain_file, 
                  policies = [MemoizationPolicy(), KerasPolicy(max_history=3, epochs=200, batch_size=50)],
                  interpreter=interpreter,
                  action_endpoint=action_endpoint)
    data = agent.load_data(training_data_file)
    agent.train(data)
    
    # Save model to be used later
    agent.persist(model_path)


# In[4]:


# Load saved agent, in case no training is needed.
agent = Agent.load('./models/dialogue', interpreter=interpreter, action_endpoint=action_endpoint)


# In[5]:


# Generate tree of interaction of utterances in possible dialogs
treeFile = "images/dialogtree.html"
agent.visualize("data/stories.md",output_file=treeFile, max_history=2)
IFrame(src=treeFile, width=1000, height=600)


# In[6]:


interpreter.parse(u"Pass the remote") # Parsed phrase


# In[7]:


# Interpret a sentence
def parsetxt(sent, deptree = False):
    pp = interpreter.parse(sent) # Parsed phrase
    # Print entities present in the sentence
    print(pd.DataFrame(pp['entities']))
    df = pd.DataFrame(pp['intent_ranking']).style.apply(lambda x: ['background: lightgreen' if x.name == 0 else '' for i in x],axis=1)
    if(deptree):
        doc = nlp(sent)
        displacy.render(doc, style='dep', jupyter=True, options={'distance':90})
    return df


# In[8]:


# Interpret a sentence
sent1 = u"Nurse, can you pass me the remote and my book, please"
parsetxt(sent1)


# In[11]:


# Render Dependency Tree
doc = nlp(sent1)
displacy.render(doc, style='dep', jupyter=True, options={'distance':90})


# In[12]:


# Interprete a sentence
sent2 = "Nurse, help me to get to the bathroom please"
parsetxt(sent2)


# In[13]:


# Render Dependency Tree
doc = nlp(sent2)
displacy.render(doc, style='dep', jupyter=True, options={'distance':110})


# In[14]:


parsetxt("call the doctor and tell me a joke")


# In[9]:


#Script to get the Text-To-Speech output.
audioFolder = "./audios/"
effect = ["",
          "&FX_TYPE=P&FX_LEVEL=2", #Pitch
          "&FX_TYPE=D&FX_LEVEL=-1" #Duration
         ]
rooturl = ["https://cache-a.oddcast.com/tts/gen.php?EID=3&LID=1&VID=3&TXT=",
           "&IS_UTF8=1&ACC=3314795&API=2292376&CB=vw_mc.vwCallback&HTTP_ERR=1&vwApiVersion=2"]
characters ={"," : "%2C"," " : "%20","?" : "%3F","'" : "%27"}
def play(phrase, ef = 0):
    for ch in characters:
        phrase = phrase.replace(ch,characters[ch]) #Replace character to match type in URL
    url = rooturl[0] + phrase + effect[ef]+ rooturl[1] #Build the URL
    file = audioFolder + str(uuid.uuid4()) +'.mp3'
    urllib.request.urlretrieve(url, file)
    playsound(file, True)
    #print(file)
    os.remove(file)


# In[10]:


play("My name is nurse. How may I help you?",0)


# In[11]:


#Configure microphone calibration
# Perform a quick test
r = sr.Recognizer()
with sr.Microphone() as source:
    #print("Please wait. Calibrating microphone...")
    # listen for 1 second and create the ambient noise energy level
    r.adjust_for_ambient_noise(source, duration=1)
    print("Say something!")
    audio = r.listen(source,phrase_time_limit=5)
    response = r.recognize_google(audio)
    print("I think you said: " + response)


# In[12]:


def printOut(msg, speech_out = False):
    print("👩 "+" >> " + msg +"\n")
    if(speech_out):
        play(msg)


# In[13]:


def init_nurse_bot(speech_in=False,speech_out=False):
    print("[INFO] The nurse is ready to listen. Please start a dialog... (Type 'stop' to quit)\n")
    errormsg = "I'm sorry, I didn't get it. Could you repeat please?"
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        while True:
            # >>>>>>>>>>> Input sentence
            if(speech_in):
                flag = False
                cont = 0
                while(not flag):
                    try:
                        print("Listening... >> ", end='')
                        audio = r.listen(source,phrase_time_limit=3)
                        a = r.recognize_google(audio)
                        print(a, end='\n')
                        flag = True
                    except:
                        cont += 1
                        printOut(errormsg, False)
                        if(cont == 3):
                            print("\n[TERMINATED]", end='')
                            return
            else:
                print(">> ", end='')
                a = input()
            if a == 'stop':
                print("\n[TERMINATED]", end='')
                return
            responses = agent.handle_message(a)
            if(len(responses) == 0):
                print("Action returned 0 elements. Maybe the action listener is not active. Activate listener:\n python -m rasa_core_sdk.endpoint --actions actions")
            for response in responses:
                
                printOut(response["text"], speech_out)
                if(response["text"] == "Have a nice day!"):
                    print("\n[TERMINATED]", end='')
                    return


# In[ ]:


#Activate action listener in an external console!: 
# python -m rasa_core_sdk.endpoint --actions actions


# In[14]:


init_nurse_bot(False,False)


# In[ ]:


#!python -m rasa_core.run -d models/dialogue -u models/nursebot/interpreter --debug --endpoints endpoints.yml

