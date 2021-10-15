from selenium import webdriver
from random import randint
from time import sleep
from graphdatascraper import *


def getCountry(table_data):
	
	country_name = table_data[1].text
	flag_url = ""
	total_cases = table_data[2].text
	new_cases = table_data[3].text
	total_deaths = table_data[4].text
	new_deaths = table_data[5].text
	total_recovered = table_data[6].text
	new_recovered = table_data[7].text
	active_cases = table_data[8].text
	total_tests = table_data[12].text

	if total_cases == "N/A" or len(total_cases) == 0:
		total_cases = 0
	else:
		total_cases = int(total_cases.replace(',',''))

	if new_cases == "N/A" or len(new_cases) == 0:
		new_cases = 0
	else:
		new_cases = int(new_cases.split('+')[1].replace(',',''))	

	if total_deaths == "N/A" or len(total_deaths) == 0:
		total_deaths = 0
	else:
		total_deaths = int(total_deaths.replace(',',''))
		
	if new_deaths == "N/A" or len(new_deaths) == 0:
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

	if active_cases == "N/A" or len(active_cases) == 0:
		active_cases = 0
	else:
		active_cases = int(active_cases.replace(',',''))
		
	if total_tests == "N/A" or len(total_tests) == 0:
		total_tests = 0
	else:
		total_tests = int(total_tests.replace(',',''))


	try:
		link = table_data[1].find_element_by_xpath('./a').get_attribute('href')
		sleepTime = randint(10,20)
		print("sleeping for "+str(sleepTime)+" seconds...")
		sleep(sleepTime)
		flag_url = storeGraphDataAndGetFlagURL(country_name,link)	
	except Exception as e:
		print("Couldn't get Graph Data for "+country_name)

	return { "Country" : country_name,"Flag" : flag_url,"NewConfirmed" : new_cases,"TotalConfirmed" : total_cases,"NewDeaths" : new_deaths,"TotalDeaths" : total_deaths,"TotalRecovered": total_recovered,"NewRecovered":new_recovered,"ActiveCases" : active_cases,"TotalTests":total_tests }	