from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_nlu.tokenizers import Token
from rasa_nlu.components import Component

class SlangReplace(Component):
    name = "SlangReplace"
    provides = ["tokens_slangprocessed"]
    requires = ["tokens"]
    defaults = {}
    language_list = None
    slangs = None
    def __init__(self, component_config=None):
        import pandas as pd
        self.slangs=pd.read_csv("slangs.csv")
        super(SlangReplace, self).__init__(component_config)

    def train(self, training_data, cfg, **kwargs):
        print("TRAINING SLANGS")
        pass

    def process(self, message, **kwargs):
        tokens_s=[]
        for token in message.get("tokens"):
            if token.text in self.slangs:
                for subtoken in self.slangs[token.text].split(" "):
                    tokens_s.extend(Token(subtoken,0))
            else:
                tokens_s.append(token)
        message.set("tokens_slangprocessed", tokens_s)

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