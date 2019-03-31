from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_nlu.components import Component


class CNN(Component):
    name = "CNN"
    provides = ["intent","intent_ranking"]
    requires = ["feature_matrix"]
    defaults = {}
    language_list = None
    MAX_SEQUENCE_LENGTH = None
    words_index = None
    model = None
    macro_to_id = None
    def __init__(self, component_config=None):
        self.MAX_SEQUENCE_LENGTH = 1000
        super(CNN, self).__init__(component_config)

    def train(self, training_data, cfg, **kwargs):
        import json
        import pandas as pd
        with open('models/current/nlu/data.json') as f:
           self.words_index = json.load(f)
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
        self.macro_to_id = dict((note, number) for number, note in enumerate(macronum))
        print("TRAINING CNN")
        import numpy as np
        import pandas as pd
        from collections import defaultdict
        import re
        import sys
        import os # Why theano why not
        from keras.preprocessing.sequence import pad_sequences
        from keras.utils.np_utils import to_categorical
        from keras.layers import Embedding
        from keras.layers import Dense, Input, Flatten
        from keras.layers import Conv1D, MaxPooling1D, Embedding, Dropout
        from keras.models import Model
        from keras.callbacks import ModelCheckpoint
        from gensim.models import Word2Vec
        MAX_NB_WORDS = 20000
        EMBEDDING_DIM = 100
        VALIDATION_SPLIT = 0.2
        MAX_WORDS_IN_SENTENCE = 20
        model = Word2Vec.load('models/current/nlu/model.bin')
        def fun(i):
            return self.macro_to_id[i]
        dataset["label"]=dataset["label"].apply(fun)
        embedding_matrix = np.zeros((len(self.words_index)+1, EMBEDDING_DIM))
        for word, i in self.words_index.items():
            embedding_vector = model[word]
            embedding_matrix[i] = embedding_vector
        embedding_layer = Embedding(len(self.words_index)+1,
                                    EMBEDDING_DIM,weights=[embedding_matrix],
                                    input_length=self.MAX_SEQUENCE_LENGTH,trainable=True)
        sequence_input = Input(shape=(self.MAX_SEQUENCE_LENGTH,), dtype='int32')
        embedded_sequences = embedding_layer(sequence_input)
        l_cov1= Conv1D(32, 2, activation='relu')(embedded_sequences)
        l_pool1 = MaxPooling1D(5)(l_cov1)
        l_cov2 = Conv1D(32, 2, activation='relu')(l_pool1)
        l_pool2 = MaxPooling1D(5)(l_cov2)
        l_cov3 = Conv1D(32, 2, activation='relu')(l_pool2)
        l_pool3 = MaxPooling1D(32)(l_cov3)  # global max pooling
        l_flat = Flatten()(l_pool3)
        l_dense = Dense(32, activation='relu')(l_flat)
        preds = Dense(len(macronum), activation='softmax')(l_dense)

        self.model = Model(sequence_input, preds)
        self.model.compile(loss='categorical_crossentropy',
                      optimizer='rmsprop',
                      metrics=['acc'])
        print("CNN Text Classifier")
        self.model.summary()
        cp=ModelCheckpoint('model_cnn.hdf5',monitor='val_acc',verbose=1,save_best_only=True)
        X_train = [row.split() for row in list(dataset["data"])]
        for a in range(len(X_train)):
            X_train[a]=[self.words_index[x] for x in X_train[a]]
        X_train = pad_sequences(X_train, padding='post',maxlen=self.MAX_SEQUENCE_LENGTH)
        y_train = [[0 for a in range(len(macronum))] for b in range(len(dataset["label"]))]
        print(dataset["label"][0])
        for a in range(len(dataset["label"])):
            y_train[a][dataset["label"][a]]=1
        print(np.array(X_train).shape)
        history=self.model.fit(np.array(X_train),np.array(y_train),epochs=1,validation_split=0.2,batch_size=1,callbacks=[cp],verbose=1,shuffle=True)

    def process(self, message, **kwargs):
        import json
        import pandas as pd
        with open('models/current/nlu/data.json') as f:
           self.words_index = json.load(f)
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
        self.macro_to_id = dict((note, number) for number, note in enumerate(macronum))
        from keras.preprocessing.sequence import pad_sequences
        from keras.models import model_from_json
        import numpy as np
        print(self.MAX_SEQUENCE_LENGTH)
        json_file = open('models/current/nlu/model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights("models/current/nlu/model.h5")
        print("Loaded model from disk")
        X = message.get("feature_matrix")
        print(type(X))
        X = pad_sequences([X], padding='post',maxlen=self.MAX_SEQUENCE_LENGTH)
        Y = loaded_model.predict(X)
        i=np.argmax(Y[0])
        m=np.amax(Y[0])
        inv_map = {v: k for k, v in self.macro_to_id.items()}
        print(inv_map[i] , m)
        message.set("intent", {"name": inv_map[i], "conf" : str(m)}, add_to_output=True)

    def persist(self, model_dir):
        from keras.models import model_from_json
        model_json = self.model.to_json()
        with open(model_dir+"/model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        self.model.save_weights(model_dir+"/model.h5")
        print("Saved model to disk")

    @classmethod
    def load(cls, model_dir=None, model_metadata=None, cached_component=None,
             **kwargs):
        """Load this component from file."""

        if cached_component:
            return cached_component
        else:
            component_config = model_metadata.for_component(cls.name)
            return cls(component_config)