import pickle
from sklearn.ensemble import RandomForestClassifier

class SmartCreditModel:
    def __init__(self, version, deploy = True):
        self.__MODEL_NAME = 'smartcredit-'
        self.__version = version
        self.__deploy = deploy
        
    def load(self):
        fileName = self.getFileName()
        model = pickle.load(open(fileName, 'rb'))
        return model
        
    def save(self, model):
        fileName = self.getFileName()
        pickle.dump(model, open(fileName, 'wb'))

    def untrained(self):
        model = RandomForestClassifier(n_estimators=301,
                               min_samples_split=30,
                               max_depth=16,
                               max_leaf_nodes=None,
                               criterion='entropy', 
                               class_weight="balanced")
        return model
        
    def getFileName(self):
        lastName = '.sav'
        if self.__deploy:
            lastName = '-deploy' + lastName
        fileName = self.__MODEL_NAME + self.__version + lastName
        return fileName
        
    
        
        
        