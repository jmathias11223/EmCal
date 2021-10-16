from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import sys
import csv

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

startLoc = Location()
destinationLoc = Location()

# start and destination are String parameters
def locationInputs(startAddress, destinationAddress):
	startLoc.setAddress(startAddress)
	destinationLoc.setAddress(destinationAddress)

#locationInputs("1111 S Figueroa St, Los Angeles, CA, USA", "1 center court, Cleveland, OH, USA")
locationInputs(sys.argv[1], sys.argv[2])

option = webdriver.ChromeOptions()
option.add_argument('headless')

driver = webdriver.Chrome(executable_path="../Hackathon/chromedriver", options = option)
driver.get('https://airport.globefeed.com/US_Nearest_Airport.asp')

try:
	searchBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'placename1')))
	searchBox.send_keys(startLoc.__str__())
	time.sleep(1)
	searchBox.send_keys(Keys.ARROW_DOWN)
	searchBox.send_keys(Keys.RETURN)
finally:
	pass

try:
	startLoc.nearestAirport = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[1]/div/div/div/div[2]/table[1]/tbody/tr[2]/td[4]'))).text
	# print(startLoc.nearestAirport)
finally:
	pass

driver.get('https://airport.globefeed.com/US_Nearest_Airport.asp')

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

if (startLoc.nearestAirport != destinationLoc.nearestAirport):
	driver.get('https://calculator.carbonfootprint.com/calculator.aspx?tab=3')
	oneWayButton = driver.find_element_by_xpath('//*[@id="ctl05_rbnOneWay"]')
	oneWayButton.click()

	fromBox = driver.find_element_by_xpath('//*[@id="ctl05_rcbAirportFrom_Input"]')
	fromBox.send_keys(startLoc.nearestAirport)
	time.sleep(0.5)
	fromBox.send_keys(Keys.RETURN)
	time.sleep(0.5)

	toBox = driver.find_element_by_xpath('//*[@id="ctl05_rcbAirportTo_Input"]')
	toBox.send_keys(destinationLoc.nearestAirport)
	time.sleep(0.5)
	toBox.send_keys(Keys.RETURN)
	time.sleep(0.5)

	submitButton = driver.find_element_by_xpath('//*[@id="ctl05_btnAddFlight"]')
	submitButton.click()

	footprint = ' '.join(driver.find_element_by_xpath('//*[@id="lblTabTotal"]').text.split()[4:])

else:
	footprint = 'N/A'

# print(footprint)

driver.close()

row = [startLoc.nearestAirport, destinationLoc.nearestAirport, footprint]

filename = '../Hackathon/datafiles/flight_co2_emission.csv'

with open(filename, 'w') as csvfile:
	csvwriter = csv.writer(csvfile)
	csvwriter.writerow(row)