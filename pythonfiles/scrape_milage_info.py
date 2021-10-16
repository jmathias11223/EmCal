from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys

class Car:
	def __init__(self):
		self.make = ""
		self.model = ""
		self.year = ""
		self.mpg = 0

	def __str__(self):
		returnValue = "{} {} {} gives {} MPG".format(self.year, self.make, self.model, self.mpg)
		return returnValue

	def __eq__(self, other):
		if (self.make == other.make):
			if (self.model == other.model):
				if (self.year == other.year):
					return True
		return False

	def setAttributes(self, make, model, year):
		self.make = make
		self.model = model
		self.year = year

	def getSearchString(self):
		searchString = "{} {} {}".format(self.year, self.make, self.model)
		return searchString

car = Car()

def carInputs(make, model, year):
	car.setAttributes(make, model, year)

#carInputs("Toyota", "Tacoma", "2013")
carInputs(sys.argv[1], sys.argv[2], sys.argv[3])

option = webdriver.ChromeOptions()
option.add_argument('headless')

driver = webdriver.Chrome(executable_path="../Hackathon/chromedriver", options = option)
driver.get("https://www.google.com")
time.sleep(2)

search = driver.find_element_by_name('q')
search.send_keys(car.getSearchString() + " mpg")
search.send_keys(Keys.RETURN)

mpgCity = 0
mpgHighway = 0

allSpecs = driver.find_elements_by_class_name('wDYxhc')
for i in allSpecs:
	if 'city' in i.text and 'highway' in i.text:
		iterate = i.text.split()
		for j in range(len(iterate)):
			if iterate[j] == 'city':
				mpgCity = int(iterate[j - 1])
			elif iterate[j] == 'highway':
				mpgHighway = int(iterate[j - 1])

driver.close()

avgMpg = (0.45 * mpgHighway) + (0.55 * mpgCity)
#print("%.2f MPG" % avgMpg)
print(str(mpgHighway) + "," + str(mpgCity))