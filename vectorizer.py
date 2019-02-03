from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_nlu.components import Component


class WordVectorizer(Component):
    name = "WordVectorizer"
    provides = ["feature_matrix"]
    requires = ["token_spellchecked"]
    defaults = {}
    language_list = None
    model = None
    words_index = None
    def __init__(self, component_config=None):
        super(WordVectorizer, self).__init__(component_config)

    def train(self, training_data, cfg, **kwargs):
        import pandas as pd
        from gensim.models import Word2Vec
        EMBEDDING_DIM = 100
        print("TRAINING VECTORIZER")
        df = pd.read_json('models/current/nlu/training_data.json')
        dataset = pd.DataFrame()
        label = []
        text = []
        for a in list(df["rasa_nlu_data"][0]):
            label.append(a["intent"])
            text.append(a["text"])
        dataset["data"]=text
        dataset["label"]=label
        macronum=sorted(set(dataset["label"]))
        print(len(macronum))
        macro_to_id = dict((note, number) for number, note in enumerate(macronum))
        def fun(i):
            return macro_to_id[i]
        dataset["label"]=dataset["label"].apply(fun)
        sentences = []
        for row in dataset["data"]:
            sentences.append(row.split())
        self.model = Word2Vec(sentences, min_count=1 ,size = EMBEDDING_DIM)
        print(self.model)
        words = list(self.model.wv.vocab)
        self.words_index={}
        for index,word in enumerate(words):
            self.words_index[word]=index

    def process(self, message, **kwargs):
        import json
        with open('models/current/nlu/data.json') as f:
            self.words_index = json.load(f)
        feature_matrix = []
        for token in message.get("token_spellchecked"):
            feature_matrix.append(self.words_index[token.text])
        message.set("feature_matrix", feature_matrix)

    def persist(self, model_dir):
        import json
        self.model.save(model_dir+'/model.bin')
        with open(model_dir+'/data.json', 'w') as outfile:
            json.dump(self.words_index, outfile)

    @classmethod
    def load(cls, model_dir=None, model_metadata=None, cached_component=None,
             **kwargs):
        if cached_component:
            return cached_component
        else:
            component_config = model_metadata.for_component(cls.name)
            return cls(component_config)