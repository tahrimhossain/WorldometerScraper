from selenium import webdriver
from pymongo import MongoClient
from bson.json_util import dumps
import json
from graphdatascraper import *
from random import randint
from time import sleep


url = 'https://www.worldometers.info/coronavirus/'

options = webdriver.ChromeOptions()
options.headless = True

driver = webdriver.Chrome("/Users/tahrim/Desktop/WorldometerScraper/chromedriver",options = options)
driver.get(url)

secrets = open('secrets.txt',mode = 'r')
mongoURL = secrets.read()
secrets.close()

client = MongoClient(mongoURL)
database = client["covidDatabse"]


body = driver.find_elements_by_xpath('//html/body/div[3]/div[3]/div/div[6]/div[1]/div/table/tbody[1]/tr')


country_list = []

world_wide_total_cases = ""
world_wide_new_cases = ""
world_wide_total_deaths = ""
world_wide_new_deaths = ""
world_wide_total_recovered = ""
world_wide_new_recovered = ""

for x in body:
	td = x.find_elements_by_xpath('./td')
	
	if len(td[1].text) > 0 and td[1].text != "World":
		
		country_name = td[1].text
		total_cases = td[2].text
		new_cases = td[3].text
		total_deaths = td[4].text
		new_deaths = td[5].text
		total_recovered = td[6].text
		new_recovered = td[7].text

		if len(total_cases) == 0:
			total_cases = 0
		else:
			total_cases = int(total_cases.replace(',',''))

		if len(new_cases) == 0:
			new_cases = 0
		else:
			new_cases = int(new_cases.split('+')[1].replace(',',''))	

		if len(total_deaths) == 0:
			total_deaths = 0
		else:
			total_deaths = int(total_deaths.replace(',',''))
		
		if len(new_deaths) == 0:
			new_deaths = 0
		else:
			new_deaths = int(new_deaths.split('+')[1].replace(',',''))

		if total_recovered == "N/A" or len(total_recovered) == 0:
			total_recovered = 0
		else:
			total_recovered = int(total_recovered.replace(',',''))

		if new_recovered == "N/A" or len(new_recovered) == 0:
			new_recovered = 0
		else:
			new_recovered = int(new_recovered.split('+')[1].replace(',',''))			
		
		country_obj = { "Country" : country_name,"NewConfirmed" : new_cases,"TotalConfirmed" : total_cases,"NewDeaths" : new_deaths,"TotalDeaths" : total_deaths,"TotalRecovered": total_recovered,"NewRecovered":new_recovered }
		country_list.append(country_obj)
		
		try:
			link = td[1].find_element_by_xpath('./a').get_attribute('href')
			sleepTime = randint(10,100)
			print("sleeping for "+str(sleepTime)+" seconds...")
			sleep(sleepTime)
			storeGraphData(country_name,link)	
		except Exception as e:
			print("Couldn't get Graph Data for "+country_name)
		
		
	elif len(td[1].text) > 0 and td[1].text == "World":

		world_wide_total_cases = td[2].text
		world_wide_new_cases = td[3].text
		world_wide_total_deaths = td[4].text
		world_wide_new_deaths = td[5].text
		world_wide_total_recovered = td[6].text
		world_wide_new_recovered = td[7].text

		if len(world_wide_total_cases) == 0:
			world_wide_total_cases = 0
		else:
			world_wide_total_cases = int(world_wide_total_cases.replace(',',''))

		if len(world_wide_new_cases) == 0:
			world_wide_new_cases = 0
		else:
			world_wide_new_cases = 	int(world_wide_new_cases.split('+')[1].replace(',',''))

		if len(world_wide_total_deaths) == 0:
			world_wide_total_deaths = 0
		else:
			world_wide_total_deaths = int(world_wide_total_deaths.replace(',',''))

		if len(world_wide_new_deaths) == 0:
			world_wide_new_deaths = 0
		else:
			world_wide_new_deaths = 	int(world_wide_new_deaths.split('+')[1].replace(',',''))

		if len(world_wide_total_recovered) == 0:
			world_wide_total_recovered = 0
		else:
			world_wide_total_recovered = int(world_wide_total_recovered.replace(',',''))

		if len(world_wide_new_recovered) == 0:
			world_wide_new_recovered = 0
		else:
			world_wide_new_recovered = 	int(world_wide_new_recovered.split('+')[1].replace(',',''))						
	
jsonObj = {"_id": "summary","Global": { "NewConfirmed" : world_wide_new_cases,"TotalConfirmed" : world_wide_total_cases,"NewDeaths" : world_wide_new_deaths, "TotalDeaths" : world_wide_total_deaths,"TotalRecovered":world_wide_total_recovered,"NewRecovered":world_wide_new_recovered},"Countries": country_list}
serialized = json.dumps(jsonObj)

database.summary.replace_one({"_id":"summary"},jsonObj,True)

print("Scraping Done Succesfully!!")
driver.quit()
