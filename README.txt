INSTALACAO

O primeiro passo � ter um projeto no google:

https://console.developers.google.com

Depois � necess�rio ativar os apis:

Direction API
Geocode API

O google maps � pago, ent�o � necess�rio ativar a conta paga
Adicionalmente, tem que fucar um pouco para mexer no n�mero de usos por dia de cada API


ANACONDA

conda create --name geoML
conda activate geoML
conda install -c conda-forge googlemaps 
conda install spyder
conda install ipykernel=4.8.2  #Tinha um bug na versao do spyder por isso essa instalacao e necessario
conda install matplotlib

HEADER DO distances.csv:

latStart;lngEnd;latEnd;lngEnd;distance;time




