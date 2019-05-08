import numpy as np

class CalculateScore:
    def __init__(self, version):
        self.__version = version

    def calculate(self, Y):
        if self.__version[0:4] == '0-1-':
            return self._calculateScorev01(Y)
        else:
            raise Exception('Version ' + self.__version + ' not implemented in CalculateScore')
        
    def _calculateScorev01(self, Y):
        score = []
        for i_batch in range(Y.shape[1]):
            clientScore = []
            for day in range(Y.shape[0]):
                clientScore.append(int(100*Y[day][i_batch][0]))
            score.append(np.array(clientScore))
        return np.array(score)        
        
