from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv



#Initialize a Chrome browser
driver = webdriver.Chrome()

#Go to the page we want to scrape
driver.get('https://icodrops.com/category/ended-ico/')

#Open our csv file to write in 
csv_file = open('icodrops_ended_icos.csv', 'w')
writer = csv.writer(csv_file)
writer.writerow(['Project_Name', 'Interest', 'Category', 'Received', 'Goal', 'End_Date', 'Ticker'])


page_url = 'https://icodrops.com/category/ended-ico/'
# We only have one page to scrape
while True:
	try:
		#print the url that we are scraping
		print('Scraping this url:' + page_url)

		#Exract a list object where each element of the list is a row in the table
		rows = driver.find_elements_by_xpath('//div[@class="col-md-12 col-12 a_ico"]') 
		
		# Extract detail in columns from each row
		for row in rows:
			#Initialize a dictionary for each row
			row_dict = {}

			#Use relative xpaths to locate desired data
			project_name = row.find_element_by_xpath('.//div[@class="ico-row"]/div[2]/h3/a').text
			interest = row.find_element_by_xpath('.//div[@class="interest"]').text
			category = row.find_element_by_xpath('.//div[@class="categ_type"]').text
			received = row.find_element_by_xpath('.//div[@id="new_column_categ_invisted"]/span').text
			goal = row.find_element_by_xpath('.//div[@id="categ_desctop"]').text
			end_date = row.find_element_by_xpath('.//div[@class="date"]').text
			ticker = row.find_element_by_xpath('.//div[@id="t_tikcer"]').text


			# Add extracted data to the dictionary
			row_dict['project_name'] = project_name
			row_dict['interest'] = interest
			row_dict['category'] = category
			row_dict['received'] = received
			row_dict['goal'] = goal
			row_dict['end_date'] = end_date
			row_dict['ticker'] = ticker


			writer.writerow(row_dict.values())
	

	except Exception as e:
		print(e)
		csv_file.close()
		driver.close()
		break
