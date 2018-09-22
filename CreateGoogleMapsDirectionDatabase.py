import googlemaps
from datetime import datetime
import matplotlib.pyplot as plt
import random

class CreateGoogleMapsDirectionDatabase:

	def __init__(self, projectKey):
		"""Object to create a database for distance and time estimator\n
		check example test below"""


		self.__FILE_DIR_TXT = "directions.txt"
		self.__FILE_DIR_CSV = "directions.csv"

		self.__gmaps = googlemaps.Client(key=projectKey)
		self.__timeCreated = str(datetime.now()) #failing HTTP 400

        
	def saveCoord(self, posStart, posEnd):
		coordStart = self._createCoord(posStart)
		coordEnd = self._createCoord(posEnd)
		direction = self.__gmaps.directions(coordStart,coordEnd,mode="driving",departure_time='now')
		self._saveDirectionInFile(posStart, posEnd, direction)

	def generateRandomRectangle(self, pointStart, dlat, dlng, Npoints):
		lat = []
		lng = []
		for i in range(Npoints):
			rLat = random.random()
			lat.append(pointStart[0] + dlat*rLat)
			rLng = random.random()
			lng.append(pointStart[1] + dlng*rLng)
		return [lat,lng]

	def plotNtrajectories(self, coord1, coord2, Npoints):
		for i in range(Npoints):
			fig = plt.figure()
			plt.scatter([coord1[0][i],coord2[0][i]],[coord1[1][i],coord2[1][i]])
			plt.show()
			plt.close(fig)


	def _createCoord(self,vector):
		coord = {}
		coord['lat'] = vector[0]
		coord['lng'] = vector[1]
		return coord
	
	def _saveDirectionInFile(self, coordStart, coordEnd, direction):
		with open(self.__FILE_DIR_TXT, "a") as myfile:
			myfile.write(str(direction) + '\n')
		with open(self.__FILE_DIR_CSV, "a") as myfile:
			myfile.write('\n' + str(coordStart[0]) + ';' + str(coordStart[1]))
			myfile.write(';' + str(coordEnd[0]) + ';' + str(coordEnd[1]))
			myfile.write(';' + str(direction[0]['legs'][0]['distance']['value']))
			myfile.write(';' + str(direction[0]['legs'][0]['duration']['value']))


#################################################################################

def getKey():
	"""Build your own key or check developers for more info"""
	keyFileName = 'C:\\Users\\frederico\\Desktop\\projectKey.txt'
	keyFile = open(keyFileName, 'r')
	pKey = keyFile.read()
	keyFile.close()
	return pKey

if __name__ == "__main__":
	pKey = getKey()
	sgm = CreateGoogleMapsDirectionDatabase(pKey)
	p1 = [-17.894595, -41.525351]
	dlatMax = 0.05331699999999984
	dlngMax = 0.03347699999999776
	coord1 = sgm.generateRandomRectangle(p1,dlatMax,dlngMax, 5)
	coord2 = sgm.generateRandomRectangle(p1,dlatMax,dlngMax, 5)
	for i in range(len(coord1[0])):
		sgm.saveCoord([coord1[0][i],coord1[1][i]],[coord2[0][i],coord2[1][i]])






