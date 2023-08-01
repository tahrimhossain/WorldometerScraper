from selenium import webdriver
from pymongo import MongoClient
from Country import *
from WorldWide import *

def main():
    url = 'https://www.worldometers.info/coronavirus/'

    secrets = open('secrets.txt',mode = 'r')
    mongoURL = secrets.read()
    secrets.close()

    client = MongoClient(mongoURL)
    database = client["covidDatabse"]


    options = webdriver.ChromeOptions()
    options.headless = True

    driver = webdriver.Chrome("/Users/tahrim/Desktop/WorldometerScraper/chromedriver",options = options)
    driver.get(url)

    table_row = driver.find_elements_by_xpath('//html/body/div[3]/div[3]/div/div[7]/div[1]/div/table/tbody[1]/tr')
    
    countries = []
    summary = {"_id":"summary"}
    
    for x in table_row:
        table_data = x.find_elements_by_xpath('./td')

        if len(table_data[1].text) > 0 and table_data[1].text != "World":
            country = getCountry(table_data)
            countries.append(country)
            print(country)

        elif len(table_data[1].text) > 0 and table_data[1].text == "World":
            worldwide = getWorldWide(table_data)
            summary["Global"] = worldwide
            print(worldwide)

    summary["Countries"] = countries
    database.summary.replace_one({"_id":"summary"},summary,True)
    print("Done Scraping Successfully")        

if __name__ == "__main__":
    main()
