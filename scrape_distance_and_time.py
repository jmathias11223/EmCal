# scrape_flight_co2.py must be ran first in order to obtain the nearest airport 
# to each location; the full address and 3-letter airport code MUST be separated 
# by a semicolon

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import googlemaps
import csv
import sys

# class represents a type of travel
class ModeOfTravel:
	def __init__(self, mode):
		self.mode = mode
		self.travelDistance = ""
		self.travelTime = ""

	def __str__(self):
		returnValue = "{} takes {} over {} miles".format(self.mode, self.travelTime, self.travelDistance)
		return returnValue

# class represents each location (the start and destination)
class Location:
	def __init__(self):
		self.fullAddress = ""
		self.nearestAirport = ""

	def __str__(self):
		return self.fullAddress

	def __eq__(self, other):
		if (self.fullAddress == other.fullAddress):
			return True

		return False

	def setAddress(self, fullAddress, nearestAirport):
		self.fullAddress = fullAddress
		self.nearestAirport = nearestAirport

startLoc = Location()
destinationLoc = Location()

# start and destination are String parameters
def locationInputs(startAddress, destinationAddress):
	if '; ' in startAddress:
		startLoc.fullAddress = startAddress.split('; ')[0]
		startLoc.nearestAirport = startAddress.split('; ')[1]
	elif ';' in startAddress:
		startLoc.fullAddress = startAddress.split(';')[0]
		startLoc.nearestAirport = startAddress.split(';')[1]

	if '; ' in destinationAddress:
		destinationLoc.fullAddress = destinationAddress.split('; ')[0]
		destinationLoc.nearestAirport = destinationAddress.split('; ')[1]
	elif ';' in destinationAddress:
		destinationLoc.fullAddress = destinationAddress.split(';')[0]
		destinationLoc.nearestAirport = destinationAddress.split(';')[1]


# scrape_flight_co2.py must be ran first in order to obtain the nearest airport to each location; the full address and 3-letter airport code MUST be separated by a semicolon
#locationInputs("1111 S Figueroa St, Los Angeles, CA, USA; LAX", "1 center court, Cleveland, OH, USA; CLE")
locationInputs(sys.argv[1], sys.argv[2])

flying = ModeOfTravel('flying')

# ensure that the two locations are flyable between
if (startLoc.nearestAirport != destinationLoc.nearestAirport):
	option = webdriver.ChromeOptions()
	option.add_argument('headless')

	driver = webdriver.Chrome(executable_path="../Hackathon/chromedriver", options = option)
	url = 'https://www.travelmath.com/from/%s/to/%s' % (startLoc.nearestAirport, destinationLoc.nearestAirport)
	driver.get(url)

	try:
		flightDistanceText = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wide"]/div/div[2]/div[1]/table/tbody/tr[1]'))).text
		flyingTravelDistance = flightDistanceText.split()[2]
		flying.travelDistance = ''.join(flyingTravelDistance.split(','))
	finally:
		pass

	try:
		flightTimeText = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wide"]/div/div[2]/div[1]/table/tbody/tr[2]'))).text
		flightTime = ' '. join(flightTimeText.split()[2:])
	finally:
		pass

	flying.travelTime = ' '.join(flightTime.split(', '))

	driver.close()

else:
	flying.travelDistance = 'N/A'
	flying.travelTime = 'N/A'

walking = ModeOfTravel('walking')
biking = ModeOfTravel('bicycling')
driving = ModeOfTravel('driving')

modesOfTravel = [walking, biking, driving]
for q in range(len(modesOfTravel)):
	gmaps = googlemaps.Client(key='AIzaSyB3FsOh2YhBoBmms3qEfkUEKuSBppyssBY')
	directions_result = gmaps.directions(startLoc.__str__(), destinationLoc.__str__(), mode=modesOfTravel[q].mode)

	time = ""
	distance = ""

	# print(directions_result)

	for i in directions_result:
		if 'bounds' in i:
			for j in i:
				if j == 'legs':
					for k in i['legs']:
						for z in k:
							if 'distance' in z:
								distance = k['distance']
							if 'duration' in z:
								time = k['duration']
								break

	travelDistance = distance['text'].split()[0]
	modesOfTravel[q].travelDistance = ''.join(travelDistance.split(','))
	modesOfTravel[q].travelTime = time['text']
	# print(modesOfTravel[q].__str__())	

# print("Flying: %s miles %s" % (flying.travelDistance, flying.travelTime))

# print(directions_result)

rows = [ [driving.mode.capitalize(), str(driving.travelDistance), str(driving.travelTime)],
	     [walking.mode.capitalize(), str(walking.travelDistance), str(walking.travelTime)],
		 [biking.mode.capitalize(), str(biking.travelDistance), str(biking.travelTime)],
		 [flying.mode.capitalize(), str(flying.travelDistance), str(flying.travelTime), str(startLoc.nearestAirport), str(destinationLoc.nearestAirport)]
	   ]

# print(rows)

filename = 'travel_distance_and_time.csv'

with open(filename, 'w') as csvfile:
	csvwriter = csv.writer(csvfile)
	csvwriter.writerows(rows)
