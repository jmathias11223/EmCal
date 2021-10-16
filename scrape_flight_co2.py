from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import sys
import csv

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

	def setAddress(self, fullAddress):
		self.fullAddress = fullAddress

# create the start and destination location objects
startLoc = Location()
destinationLoc = Location()

# startAddress and destinationAddress are String parameters
def locationInputs(startAddress, destinationAddress):
	startLoc.setAddress(startAddress)
	destinationLoc.setAddress(destinationAddress)

#locationInputs("1111 S Figueroa St, Los Angeles, CA, USA", "1 center court, Cleveland, OH, USA")
locationInputs(sys.argv[1], sys.argv[2])

# option to make the Chrome window not pop up
option = webdriver.ChromeOptions()
option.add_argument('headless')

# open the Chrome window
driver = webdriver.Chrome(executable_path="../Hackathon/chromedriver", options = option)

# go to the website to find nearest airport
driver.get('https://airport.globefeed.com/US_Nearest_Airport.asp')

try:
	# find the search box
	searchBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'placename1')))
	# enter in the start location address
	searchBox.send_keys(startLoc.__str__())
	time.sleep(1)
	searchBox.send_keys(Keys.ARROW_DOWN)
	searchBox.send_keys(Keys.RETURN)
finally:
	pass

try:
	# find the nearest airport, assign to start location object attribute
	startLoc.nearestAirport = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[1]/div/div/div/div[2]/table[1]/tbody/tr[2]/td[4]'))).text
	# print(startLoc.nearestAirport)
finally:
	pass

# go to the beginning of the site again
driver.get('https://airport.globefeed.com/US_Nearest_Airport.asp')

# repeat all steps above but for the destination location this time
try:
	searchBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'placename1')))
	searchBox.send_keys(destinationLoc.__str__())
	time.sleep(1)
	searchBox.send_keys(Keys.ARROW_DOWN)
	searchBox.send_keys(Keys.RETURN)
finally:
	pass

try:
	destinationLoc.nearestAirport = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[1]/div/div/div/div[2]/table[1]/tbody/tr[2]/td[4]'))).text
	# print(destinationLoc.nearestAirport)
finally:
	pass

# ensure that the start and destination locations do not have the same nearest airport
if (startLoc.nearestAirport != destinationLoc.nearestAirport):
	# go to the flight carbon calculator website
	driver.get('https://calculator.carbonfootprint.com/calculator.aspx?tab=3')
	# calculate as a one way trip
	oneWayButton = driver.find_element_by_xpath('//*[@id="ctl05_rbnOneWay"]')
	oneWayButton.click()

	# find the start location box
	fromBox = driver.find_element_by_xpath('//*[@id="ctl05_rcbAirportFrom_Input"]')
	# enter in the airport nearest to the start location
	fromBox.send_keys(startLoc.nearestAirport)
	time.sleep(0.5)
	fromBox.send_keys(Keys.RETURN)
	time.sleep(0.5)

	# find the destination location box
	toBox = driver.find_element_by_xpath('//*[@id="ctl05_rcbAirportTo_Input"]')
	# enter in the airport nearest to the destination location
	toBox.send_keys(destinationLoc.nearestAirport)
	time.sleep(0.5)
	toBox.send_keys(Keys.RETURN)
	time.sleep(0.5)

	# find and press the go button to calculate carbon emissions due to that flight
	submitButton = driver.find_element_by_xpath('//*[@id="ctl05_btnAddFlight"]')
	submitButton.click()

	# find the value
	footprint = ' '.join(driver.find_element_by_xpath('//*[@id="lblTabTotal"]').text.split()[4:])

# if the start and destination locations do have the same nearest airport, then there is no point in flying
else:
	footprint = 'N/A'

# print(footprint)

# close the Chrome window
driver.close()

# row to be written to the csv file
row = [startLoc.nearestAirport, destinationLoc.nearestAirport, footprint]

filename = 'flight_co2_emission.csv'

# open and write the information to the csv file
with open(filename, 'w') as csvfile:
	csvwriter = csv.writer(csvfile)
	csvwriter.writerow(row)