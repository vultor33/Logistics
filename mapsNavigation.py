from SaveGoogleMapsDirection import SaveGoogleMapsDirection

posStart = [-17.879161,-41.499234]
posEnd = [-17.875492,-41.50968]
projectKey = 'consult developers'

sgm = SaveGoogleMapsDirection(projectKey)
sgm.saveCoord(posStart, posEnd)

