import json
import numpy as np
import tensorflow as tf
from functools import partial
from keras import backend as K
from keras.models import model_from_json

class RupturaNeuralNetwork:
    def __init__(self, modelName = 'model'):
        self.MODEL_NAME = modelName
        self.__DEFAULT_LOSS = 'categorical_crossentropy'
    
    def saveModel(self, model):
        model_json = model.to_json()
        with open(self.MODEL_NAME + ".json", "w") as json_file:
            json_file.write(model_json)
        model.save_weights(self.MODEL_NAME + ".h5")    

    def loadModel(self, size = []):
        json_file = open(self.MODEL_NAME + '.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights(self.MODEL_NAME + ".h5")
        loaded_model = self.compileModel(loaded_model, size)
        return loaded_model
    
    def compileModel(self, model, size):
        if len(size) == 0:
            model.compile(loss = self.__DEFAULT_LOSS,optimizer='adam')
        else:
            custom_loss = self.getCustomLoss(size)
            model.compile(loss = custom_loss,optimizer='adam')
        return model
    
    def crossEntropyWeights(self, size, weightVector):
        batch_size, time_steps = size
        w_array = []
        for i in range(batch_size):
            auxWeight = []
            for j in range(time_steps):
                auxWeight.append(weightVector)
            w_array.append(auxWeight)
        w_array = tf.convert_to_tensor(np.array(w_array), dtype='float')
        return w_array
        
    def getCustomLoss(self, size, weightVector):
        def w_categorical_crossentropy(y_true, y_pred, weights):
            mask = weights * y_true
            mask = K.max(mask, axis=2)
            cross_ent = K.categorical_crossentropy(y_true,y_pred, from_logits=False)
            return cross_ent * mask

        custom_loss = partial(w_categorical_crossentropy, weights=self.crossEntropyWeights(size, weightVector))
        custom_loss.__name__ ='w_categorical_crossentropy'
        return custom_loss
            