import googlemaps
#from datetime import datetime

class SaveGoogleMapsDirection:

	def __init__(self, projectKey):
		self.__gmaps = googlemaps.Client(key=projectKey)
		self.__FILE_DIR_TXT = "directions.txt"
		self.__FILE_DIR_CSV = "directions.csv"
        
	def saveCoord(self, posStart, posEnd):
		coordStart = self._createCoord(posStart)
		coordEnd = self._createCoord(posEnd)
		direction = self.__gmaps.directions(coordStart,coordEnd,mode="driving",departure_time='now')
		self._saveDirectionInFile(posStart, posEnd, direction)

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


