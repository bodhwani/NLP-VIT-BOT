from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_nlu.components import Component
from nltk.corpus import gutenberg
import nltk 
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet 
from rasa_nlu.tokenizers import Token
lemmatizer = WordNetLemmatizer()

class Lemmatizer(Component):
    name = "Lemmatizer"

    provides = ["token_lemmatized"]
    requires = ["token_spellchecked"]
    defaults = {}
    language_list = None
    model = None
    words_index = None
    def __init__(self, component_config=None):
        super(Lemmatizer, self).__init__(component_config)

    def train(self, training_data, cfg, **kwargs):
        pass

    def process(self, message, **kwargs):
        message.set("token_lemmatized", [Token(lemmatizer.lemmatize(token.text),0) for token in message.get("token_spellchecked")])

    def persist(self, model_dir):
        pass

    @classmethod
    def load(cls, model_dir=None, model_metadata=None, cached_component=None,
             **kwargs):
        if cached_component:
            return cached_component
        else:
            component_config = model_metadata.for_component(cls.name)
            return cls(component_config)