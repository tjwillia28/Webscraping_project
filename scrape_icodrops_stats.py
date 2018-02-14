from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

# Initialize Chrome Browser
driver = webdriver.Chrome()

#Go to the page we want to scrape
driver.get('https://icodrops.com/ico-stats/')

#Open our csv file to write in
csv_file = open('icodrops_stats_2_10_18.csv', 'w')
writer = csv.writer(csv_file)
writer.writerow(['Ticker', 'ICO_Price', 'Market_Price', 'USD_ROI', 'ETH_ROI', 'BTC_ROI'])

page_url = 'https://icodrops.com/ico-stats/'

while True:
	try:
		#print the url that we are scraping
		print('Scraping this url:' + page_url)

		# Extract a list object where each element of the list is a row in the table
		rows = driver.find_elements_by_xpath('//div[@class="col-md-12 col-12 a_ico"]')

		# Extract detail in columns from each row
		for row in rows:
			# Initialize a dictionary for each row
			row_dict = {}

			#Use relative xpaths to locate desired data
			ticker = row.find_element_by_xpath('.//div[@id="t_tikcer"]').text
			ico_price = row.find_element_by_xpath('.//div[@class="token_pr"]').text
			market_price = row.find_element_by_xpath('.//div[@class="usd-price"]').text
			usd_roi = row.find_element_by_xpath('.//div[@class="st_r_usd"]').text
			eth_roi = row.find_element_by_xpath('.//div[@class="st_r_eth"]').text
			btc_roi = row.find_element_by_xpath('.//div[@class="st_r_btc"]').text


			# Add extracted data to dictionary

			row_dict['ticker'] = ticker
			row_dict['ico_price'] = ico_price
			row_dict['market_price'] = market_price
			row_dict['usd_roi'] = usd_roi
			row_dict['eth_roi'] = eth_roi
			row_dict['btc_roi'] = btc_roi


			writer.writerow(row_dict.values())

	except Exception as e:
		print(e)
		csv_file.close()
		driver.close()
		break