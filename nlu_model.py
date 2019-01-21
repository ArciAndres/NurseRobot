from rasa_nlu.training_data import load_data
from rasa_nlu import config
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter
import rasa_core.interpreter

#nlu -> Natural Language Understanding
def train_nlu(data, configFile, model_dir):
    training_data = load_data(data)
    trainer = Trainer(config.load('config_spacy.json'))
    trainer.train(training_data)
    model_directory = trainer.persist(model_dir, fixed_model_name = 'nursenlu') #Saves the model in a folder

def run_nlu():
    interpreter = rasa_core.interpreter.RasaNLUInterpreter('./models/nlu/default/nursenlu', config.load('config_spacy.json'))
    #interpreter = Interpreter.load('./models/nlu/default/nursenlu', config.load('config_spacy.json')) #Loads the saved model
    print(interpreter.parse(u"Hello.")) #test model with a phrase

if __name__ == '__main__':
    train_nlu("./data/data.md", "config_spacy.json","./models/nlu")
    run_nlu() #Test the model, and get the intent
