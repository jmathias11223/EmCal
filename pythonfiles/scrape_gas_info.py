from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import sys

class Location:
	def __init__(self):
		self.streetAddress = ""
		self.city = ""
		self.state = ""
		self.cheapestGasPrice = ""

	def __str__(self):
		returnValue = "{}, {}, {}".format(self.streetAddress, self.city, self.state)
		return returnValue

	def __eq__(self, other):
		if (self.streetAddress == other.streetAddress):
			if (self.city == other.city):
				if (self.state == other.state):
					return True
		return False

	def setAttributes(self, streetAddress, city, state):
		self.streetAddress = streetAddress
		self.city = city
		self.state = state

class Car:
	def __init__(self):
		self.make = ""
		self.model = ""
		self.year = ""
		self.fuelType = ""
		self.mpg = 0

	def __str__(self):
		returnValue = "{} {} {} uses {} fuel type and gives {} MPG".format(self.year, self.make, self.model, self.fuelType, self.mpg)
		return returnValue

	def __eq__(self, other):
		if (self.make == other.make):
			if (self.model == other.model):
				if (self.year == other.year):
					return True
		return False

	def setAttributes(self, make, model, year, fuelType, mpg):
		self.make = make
		self.model = model
		self.year = year
		self.fuelType = fuelType
		self.mpg = mpg

startLoc = Location()
destinationLoc = Location()
car = Car()

# start and destination are String parameters
def locationInputs(start, destination):
	startParts = start.split(", ")
	destinationParts = destination.split(", ")

	startLoc.setAttributes(startParts[0], startParts[1], startParts[2])
	destinationLoc.setAttributes(destinationParts[0], destinationParts[1], destinationParts[2])

def carInputs(make, model, year, fuelType, mpg):
	car.setAttributes(make, model, year, fuelType, mpg)

# Call with appropriate arguments
locationInputs(sys.argv[1], sys.argv[2])	# argv[1] = Start location; argv[2] = Destination
# argv[3] = Vehicle make; argv[4] = Model; argv[5] = Year; argv[6] = Type of fuel; argv[7] = Mileage
carInputs(sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])

option = webdriver.ChromeOptions()
option.add_argument('headless')

driver = webdriver.Chrome(executable_path="../Hackathon/chromedriver", options = option)
driver.get("https://www.geico.com/save/local-gas-prices/")
time.sleep(2)

count = 0
while (len(startLoc.cheapestGasPrice) == 0 or len(destinationLoc.cheapestGasPrice) == 0 or startLoc == destinationLoc):
	try:
		addressSearchBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="address"]')))
		addressSearchBox.send_keys(startLoc.__str__())
		addressSearchBox.send_keys(Keys.RETURN)
		time.sleep(2)
	finally:
		pass

	found = False
	allGasInfo = driver.find_elements_by_class_name('card')
	for oneStation in allGasInfo:
		gasStationInfo = oneStation.text.split('\n')
		for i in range(len(gasStationInfo)):
			if gasStationInfo[i] == car.fuelType:
				gasPrice = gasStationInfo[i - 1]
				if gasPrice == 'N/A':
					break
				else:
					startLoc.cheapestGasPrice = gasPrice
					found = True
					break
		if (found):
			break


	addressSearchBox.clear()
	addressSearchBox.send_keys(destinationLoc.__str__())
	time.sleep(2)
	addressSearchBox.send_keys(Keys.RETURN)
	time.sleep(2)

	found = False
	allGasInfo = driver.find_elements_by_class_name('card')
	for oneStation in allGasInfo:
		gasStationInfo = oneStation.text.split('\n')
		for i in range(len(gasStationInfo)):
			if gasStationInfo[i] == car.fuelType:
				gasPrice = gasStationInfo[i - 1]
				if gasPrice == 'N/A':
					break
				else:
					destinationLoc.cheapestGasPrice = gasPrice
					found = True
					break
		if (found):
			break
	count += 1
	if(count >= 3):
		break

driver.close()

print("%s,%s" % (startLoc.cheapestGasPrice[1:], destinationLoc.cheapestGasPrice[1:]))

# Make it so that you can get gas prices based on if the car uses regular, midgrade, or premium fuel; Make a Car class with those attributes as well as make, model, and mpg