#from SaveGoogleMapsDirection import SaveGoogleMapsDirection
import matplotlib.pyplot as plt
import random

def getKey():
	keyFileName = 'C:\\Users\\frederico\\Desktop\\projectKey.txt'
	keyFile = open(keyFileName, 'r')
	pKey = keyFile.read()
	keyFile.close()
	return pKey

pKey = getKey()
posStart = [-17.879161,-41.499234]
posEnd = [-17.875492,-41.50968]


def matrix():
	x = []
	y = []
	for i in range(1000):
		x.append(random.random())
		y.append(random.random())
	return [x,y]

matrStart = matrix()
matrEnd = matrix()

plt.scatter(matrStart[0],matrStart[1])

#sgm = SaveGoogleMapsDirection(projectKey)
#sgm.saveCoord(posStart, posEnd)

 