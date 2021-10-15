from selenium import webdriver

def getWorldWide(table_data):
	world_wide_total_cases = table_data[2].text
	world_wide_new_cases = table_data[3].text
	world_wide_total_deaths = table_data[4].text
	world_wide_new_deaths = table_data[5].text
	world_wide_total_recovered = table_data[6].text
	world_wide_new_recovered = table_data[7].text
	world_wide_active_cases = table_data[8].text
		

	if world_wide_total_cases == "N/A" or len(world_wide_total_cases) == 0:
		world_wide_total_cases = 0
	else:
		world_wide_total_cases = int(world_wide_total_cases.replace(',',''))

	if world_wide_new_cases == "N/A" or len(world_wide_new_cases) == 0:
		world_wide_new_cases = 0
	else:
		world_wide_new_cases = 	int(world_wide_new_cases.split('+')[1].replace(',',''))

	if world_wide_total_deaths == "N/A" or len(world_wide_total_deaths) == 0:
		world_wide_total_deaths = 0
	else:
		world_wide_total_deaths = int(world_wide_total_deaths.replace(',',''))

	if world_wide_new_deaths == "N/A" or len(world_wide_new_deaths) == 0:
		world_wide_new_deaths = 0
	else:
		world_wide_new_deaths = 	int(world_wide_new_deaths.split('+')[1].replace(',',''))

	if world_wide_total_recovered == "N/A" or len(world_wide_total_recovered) == 0:
		world_wide_total_recovered = 0
	else:
		world_wide_total_recovered = int(world_wide_total_recovered.replace(',',''))

	if world_wide_new_recovered == "N/A" or len(world_wide_new_recovered) == 0:
		world_wide_new_recovered = 0
	else:
		world_wide_new_recovered = 	int(world_wide_new_recovered.split('+')[1].replace(',',''))

	if world_wide_active_cases == "N/A" or len(world_wide_active_cases) == 0:
		world_wide_active_cases = 0
	else:
		world_wide_active_cases = int(world_wide_active_cases.replace(',',''))

	return { "NewConfirmed" : world_wide_new_cases,"TotalConfirmed" : world_wide_total_cases,"NewDeaths" : world_wide_new_deaths, "TotalDeaths" : world_wide_total_deaths,"TotalRecovered":world_wide_total_recovered,"NewRecovered":world_wide_new_recovered,"ActiveCases" : world_wide_active_cases}	