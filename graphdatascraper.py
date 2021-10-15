from selenium import webdriver
import json
import re
import datetime
from pymongo import MongoClient
from bson.json_util import dumps


def getDeathGraphData(countryName,body):

	dates = re.search("{\n            categories: \[.*\]        }",body)
	cases = re.search("data: \[.*\]",body)

	datesJsonObj = json.loads(dates.group(0).replace('categories','"categories"'))
	casesJsonObj = json.loads("{"+cases.group(0).replace('data','"data"')+"}")


	listOfGraphData = []
	for case,date in zip(casesJsonObj['data'],datesJsonObj['categories']):
		if case is None:
			case = 0
		day = {"Cases" : case, "Date" : datetime.datetime.strptime(date,'%b %d, %Y').strftime("%Y-%m-%dT%H:%M:%SZ")}
		listOfGraphData.append(day)
	
	jsonObj = {"_id":countryName,"data":listOfGraphData}		
	return jsonObj


def getConfirmedGraphData(countryName,body):
	
	dates = re.search("{\n            categories: \[.*\]        }",body)
	cases = re.search("data: \[.*\]",body)

	datesJsonObj = json.loads(dates.group(0).replace('categories','"categories"'))
	casesJsonObj = json.loads("{"+cases.group(0).replace('data','"data"')+"}")


	listOfGraphData = []
	for case,date in zip(casesJsonObj['data'],datesJsonObj['categories']):
		if case is None:
			case = 0
		day = {"Cases" : case, "Date" : datetime.datetime.strptime(date,'%b %d, %Y').strftime("%Y-%m-%dT%H:%M:%SZ")}
		listOfGraphData.append(day)
	
	jsonObj = {"_id":countryName,"data":listOfGraphData}		
	return jsonObj	
	


def storeGraphDataAndGetFlagURL(countryName,url):

	options = webdriver.ChromeOptions()
	options.headless = True
	
	driver = webdriver.Chrome("/Users/tahrim/Desktop/WorldometerScraper/chromedriver",options = options)
	driver.get(url)

	secrets = open('secrets.txt',mode = 'r')
	mongoURL = secrets.read()
	secrets.close()

	
	client = MongoClient(mongoURL)
	database = client["covidDatabse"]
	
	
	try:
		print("Fetching Confirmed Data for "+countryName)
		confirmedData = getConfirmedGraphData(countryName,driver.find_element_by_xpath('//html/body/div[4]/div[2]/div[1]/div[2]/div/script').get_attribute('innerText'))
		database.confirmedGraphData.replace_one({"_id":countryName},confirmedData,True)
		print("Fetched and updated Confirmed Data for "+countryName+" successfully")
	except Exception as e:
		print("---Couldn't update Confirmed Data for "+countryName+"---")

	try:
		print("Fetching Death Data for "+countryName)
		deathData = getDeathGraphData(countryName,driver.find_element_by_xpath('//html/body/div[4]/div[2]/div[1]/div[5]/div/script').get_attribute('innerText'))
		database.deathGraphData.replace_one({"_id":countryName},deathData,True)
		print("Fetched and updated Death Data for "+countryName+" successfully")	
	except Exception as e:
		print("---Couldn't update Death Data for "+countryName+"---")	
	
	flag_url = driver.find_element_by_xpath("//html/body/div[3]/div[2]/div[1]/div/div[3]/h1/div/img").get_attribute('src')	
	driver.quit()
	return flag_url