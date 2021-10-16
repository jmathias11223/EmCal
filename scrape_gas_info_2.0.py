from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv
import sys

class Location:
	def __init__(self):
		self.fullAddress = ""
		self.cheapestGasPrice = ""

	def __str__(self):
		return self.fullAddress

	def __eq__(self, other):
		if (self.fullAddress == other.fullAddress):
			return True

		return False

	def setAddress(self, fullAddress):
		self.fullAddress = fullAddress

class Car:
	def __init__(self):
		self.make = ""
		self.model = ""
		self.year = ""
		self.fuelType = ""

	def __str__(self):
		returnValue = "{} {} {} uses {} fuel type".format(self.year, self.make, self.model, self.fuelType)
		return returnValue

	def __eq__(self, other):
		if (self.make == other.make):
			if (self.model == other.model):
				if (self.year == other.year):
					return True
		return False

	def setAttributes(self, make, model, year, fuelType):
		self.make = make
		self.model = model
		self.year = year
		self.fuelType = fuelType

startLoc = Location()
destinationLoc = Location()
car = Car()

# start and destination are String parameters
def locationInputs(startAddress, destinationAddress):
	startLoc.setAddress(startAddress)
	destinationLoc.setAddress(destinationAddress)

def carInputs(make, model, year, fuelType):
	car.setAttributes(make, model, year, fuelType)

# Call with appropriate arguments
locationInputs(sys.argv[1], sys.argv[2])
#locationInputs("15040 Conference Center Dr #210, Chantilly, VA 20151", "25450 Riding Center Dr, Chantilly, VA 20152")	# argv[1] = Start location; argv[2] = Destination
# argv[3] = Vehicle make; argv[4] = Model; argv[5] = Year; argv[6] = Type of fuel
carInputs(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
#carInputs("Honda", "Pilot", "2018", "Regular")

relatedFuelTypes = {'Regular': 'Mid-Grade', 'Premium': 'Mid-Grade', 'Mid-Grade': 'Premium'}

option = webdriver.ChromeOptions()
option.add_argument('headless')

driver = webdriver.Chrome(executable_path="../Hackathon/chromedriver", options = option)
driver.get("https://www.geico.com/save/local-gas-prices/")
time.sleep(4)

while (len(startLoc.cheapestGasPrice) == 0):
	try:
		addressSearchBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="address"]')))
		addressSearchBox.clear()
		time.sleep(1)
		addressSearchBox.send_keys(startLoc.__str__())
		addressSearchBox.send_keys(Keys.RETURN)
		time.sleep(2.5)
	finally:
		pass

	found = False
	time.sleep(2)
	allGasInfo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'card')))
	allGasInfo = driver.find_elements_by_class_name('card')
	for oneStation in allGasInfo:
		gasStationInfo = oneStation.text.split('\n')
		for i in range(len(gasStationInfo)):
			if gasStationInfo[i] == car.fuelType:
				# print(gasStationInfo[i])
				gasPrice = gasStationInfo[i - 1]
				# print(gasPrice)
				if gasPrice == 'N/A':
					startLoc.cheapestGasPrice = 'N/A'
					break
				else:
					startLoc.cheapestGasPrice = gasPrice
					found = True
					break
		if (found):
			break

	if (startLoc.cheapestGasPrice == 'N/A'):
		if (car.fuelType == 'Diesel'):
			break
		startLoc.cheapestGasPrice = ""
		car.fuelType = relatedFuelTypes[car.fuelType]


# print(startLoc.cheapestGasPrice)

while (len(destinationLoc.cheapestGasPrice) == 0):
	try:
		addressSearchBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="address"]')))
		addressSearchBox.clear()
		time.sleep(1)
		addressSearchBox.send_keys(destinationLoc.__str__())
		addressSearchBox.send_keys(Keys.RETURN)
		time.sleep(2.5)
	finally:
		pass

	found = False
	time.sleep(2)
	allGasInfo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'card')))
	allGasInfo = driver.find_elements_by_class_name('card')
	for oneStation in allGasInfo:
		gasStationInfo = oneStation.text.split('\n')
		for i in range(len(gasStationInfo)):
			if gasStationInfo[i] == car.fuelType:
				# print(gasStationInfo[i])
				gasPrice = gasStationInfo[i - 1]
				# print(gasPrice)
				if gasPrice == 'N/A':
					destinationLoc.cheapestGasPrice = 'N/A'
					break
				else:
					destinationLoc.cheapestGasPrice = gasPrice
					found = True
					break
		if (found):
			break

	if (destinationLoc.cheapestGasPrice == 'N/A'):
		if (car.fuelType == 'Diesel'):
			break
		destinationLoc.cheapestGasPrice = ""
		car.fuelType = relatedFuelTypes[car.fuelType]

# print(destinationLoc.cheapestGasPrice)

driver.close()

# print("%s,%s" % (startLoc.cheapestGasPrice[1:], destinationLoc.cheapestGasPrice[1:]))

row = [startLoc.cheapestGasPrice[1:], destinationLoc.cheapestGasPrice[1:]]

filename = 'gas_prices.csv'

with open(filename, 'w') as csvfile:
	csvwriter = csv.writer(csvfile)
	csvwriter.writerow(row)

print("Done")