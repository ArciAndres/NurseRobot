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
from rasa_core.utils import EndpointConfig
from rasa_core.run import serve_application
from rasa_core import config
import spacy
from spacy import displacy

import ruamel
import os
import win32com.client as wincl

import warnings
warnings.simplefilter('ignore', ruamel.yaml.error.UnsafeLoaderWarning)
warnings.filterwarnings("ignore",category=DeprecationWarning)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #To ignore Tensorflow AVX AVX2 bonary warning

logger = logging.getLogger(__name__)
speak = wincl.Dispatch("SAPI.SpVoice")
nlp = spacy.load('en_core_web_sm')
phrases = []
interpreter_path ='./models/nursebot/interpreter'

def train_dialogue(train = True,domain_file = 'nurse_domain.yml',
					model_path = './models/dialogue',
					training_data_file = './data/stories.md'):
	if(train == True):
		agent = Agent(domain_file, policies = [MemoizationPolicy(), KerasPolicy(max_history=3, epochs=200, batch_size=50)])
		data = agent.load_data(training_data_file)
		agent.train(data)
		#agent.visualize("data/stories.md",output_file="graph.html", max_history=2)
		agent.persist(model_path)
		return agent

def saveDependencyGraph(phrase,saveImages = True):
	phrases.append(nlp(phrase))
	html = displacy.render(phrases, style='dep', page=True)
	#svg = displacy.render(doc, style='dep')
	#output_path = Path('/images/sentence.html')
	#output_path.open('w', encoding='utf-8').write(html)

def run_nurse_bot(serve_forever=True):
	interpreter = RasaNLUInterpreter(interpreter_path)
	action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
	agent = Agent.load('./models/dialogue', interpreter=interpreter, action_endpoint=action_endpoint)
	print("[INFO] The nurse is ready to listen. Please start a dialog... (Type 'stop' to quit)")
	while serve_forever:
		print(">> ", end='')
		a = input()
		if a == 'stop':
			break
		#saveDependencyGraph(a,True)
		responses = agent.handle_message(a)
		if(len(responses) == 0):
			print("Action returned 0 elements. Maybe the action listener is not active. Activate listener:\n python -m rasa_core_sdk.endpoint --actions actions")
		for response in responses:
			print("👩 "+" >> " + response["text"]+"\n")
			#speak.Speak(response["text"])

		#rasa_core.run.serve_application(agent ,channel='cmdline')

if __name__ == '__main__':
	#train_dialogue(True)
	run_nurse_bot(True)

#Code to display stories
#python -m rasa_core.visualize -d nurse_domain.yml -s data/stories.md -o graph.html -c config_spacy.json