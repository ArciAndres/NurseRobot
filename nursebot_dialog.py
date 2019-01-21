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
import ruamel
import os
import win32com.client as wincl

import warnings
warnings.simplefilter('ignore', ruamel.yaml.error.UnsafeLoaderWarning)
warnings.filterwarnings("ignore",category=DeprecationWarning)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #To ignore Tensorflow AVX AVX2 bonary warning

logger = logging.getLogger(__name__)
speak = wincl.Dispatch("SAPI.SpVoice")

def train_dialogue(domain_file = 'nurse_domain.yml',
					model_path = './models/dialogue',
					training_data_file = './data/stories.md'):
					
	agent = Agent(domain_file, policies = [MemoizationPolicy(), KerasPolicy(max_history=3, epochs=200, batch_size=50)])
	data = agent.load_data(training_data_file)	
	agent.train(data)
	agent.visualize("data/stories.md",output_file="graph.html", max_history=2)
	agent.persist(model_path)
	return agent
	
def run_nurse_bot(serve_forever=True):
	interpreter = RasaNLUInterpreter('./models/nlu/default/nursenlu')
	action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
	agent = Agent.load('./models/dialogue', interpreter=interpreter, action_endpoint=action_endpoint)
	print("[INFO] The nurse is ready to listen. Please start a dialog... (Type 'stop' to quit)")
	while serve_forever:
		print(">> ", end='')
		a = input()
		if a == 'stop':
			break
		responses = agent.handle_message(a)
		for response in responses:
			print("👩 "+"  >>  " + response["text"]+"\n")
			speak.Speak(response["text"])

		#rasa_core.run.serve_application(agent ,channel='cmdline')

if __name__ == '__main__':
	#train_dialogue()
	run_nurse_bot()

#Code to display stories
#python -m rasa_core.visualize -d nurse_domain.yml -s data/stories.md -o graph.html -c config_spacy.json