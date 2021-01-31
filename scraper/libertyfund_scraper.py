import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time
import logging
import logging.handlers
import os
import mysql.connector
from datetime import datetime
from collections import deque
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create 'logs' directory if it doesn't already exist
os.makedirs('logs/', exist_ok=True)

# Custom logger
logger: object = logging.getLogger("libertyfund_scraper")
logging.basicConfig(level = logging.INFO)

# File name for log files
logfilename: str = 'logs/log{:%Y-%m-%d}.log'.format(datetime.now())

# Flag to determine if the logger has already created a file
rollover: bool = os.path.isfile(logfilename)

# Handler for logger
# The FileHandler will also output logs to the terminal window, so an extra
# 	handler for that is not necessary
file_handler: object = logging.handlers.RotatingFileHandler(logfilename, mode='w', backupCount=5, delay=True)

# Roll over file name if a log already exists
if rollover:
	file_handler.doRollover()

file_handler.setLevel(logging.INFO)

# Formatter for logger output
log_format: object = logging.Formatter('%(asctime)s\t: %(name)s : %(levelname)s -- %(message)s', '%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(log_format)

# Add to logger
logger.addHandler(file_handler)

# Connect to SQL database
db_conn: object = mysql.connector.connect(
	user='root',
	password='password',
	host='127.0.0.1',
	database='test')

db_cursor: object = db_conn.cursor()

# Retry strategy that defines how and when to retry a failure on http.get
# Allows for 3 retries that are executed if any of the status_forcelist
# 	errors are encountered. backoff_factor = 1 determines the sleep time
# 	between failed requests. Increases exponentially: 0.5, 1, 2, 4, 8, etc.
retry_strat: object = Retry(
	total = 3,
	status_forcelist = [413, 429, 500, 502, 503, 504],
	allowed_methods = ["HEAD", "GET", "OPTIONS"],
	backoff_factor = 1
)

# Applies the retry strategy to all requests done through the http object
adapter: object = HTTPAdapter(max_retries=retry_strat)
http: object = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

def process_page(pageURL: str, index: int) -> None:
	page: object
	title: str
	contribs: str
	file: object
	filename: str
	filepath: str

	print(pageURL)

	sql_insert_stmt: str = (
		"INSERT INTO Metadata(title, author, url, filepath)"
		"VALUES (%s, %s, %s, %s)" )

	# The full text is loaded using Javascript after the page loads,
	#	so a headless browser will need to be spun up to see it as
	#	the requests library can't handle Javascript
	opts = Options()
	opts.headless = True
	browser = Chrome(options=opts)

	# Normally this would be encapsulated within a try block, but this
	#	function will be called from within a try block so any exceptions
	#	will be handled that way
	browser.get(pageURL)

	# Wait for the HTML preview to load before doing anything
	document_elem: bool = EC.presence_of_element_located((By.CLASS_NAME, 'document'))
	WebDriverWait(browser, 5).until(document_elem)

	# page = http.get(pageURL, timeout=(10, 27))
	# page.raise_for_status()

	# Wait for page to load
	#time.sleep(3)

	page_soup = BeautifulSoup(browser.page_source, 'lxml')

	# Extract title
	title = page_soup.find('h1').text.strip()[:255] # title is in first header

	# Extract author
	people_column: object = page_soup.find('div', class_='column')
	contribs = people_column.find('li').text[8:255] # first li is author; [8:] skips over leading 'Author: ' substring

	# Extract full text
	document: str = page_soup.find('div', class_='document').text

	# Store full text
	filename = f"lib{index}" + title[:5].replace(" ", "_") + ".txt"
	file = open(filename, 'a')
	file.write(document)

	filepath = os.path.realpath(file.name)

	file.close()

	print('File ' + filename + ' written.')

	# Put metadata in database
	try:
		data: tuple = (title, contribs, pageURL, filepath)
		db_cursor.execute(sql_insert_stmt, data)
		db_conn.commit()
	except Exception as err:
		db_conn.rollback()
		logger.warning("Error occurred when writing to databse", exc_info=True)

def scrape(startingURL: str) -> int:
	q: object = deque()
	fail_q: object = deque()
	fileindex: int = 1

	if(startingURL == None):
		logger.critical('\'None\' type received as input, exiting')
		return -3

	# Check the URL to make sure it leads to the website we want to scrape
	if not 'libertyfund.org' in startingURL:
		logger.critical(startingURL + ' is either an invalid URL or not the target of the scraper')
		return -2

	# Load the starting page (assumed to be the result of a search) and begin parsing
	# If the starting page doesn't load on first try, exit with error code
	try:
		page: object = http.get(startingURL)
		page.raise_for_status()
	except Exception as err:
		logger.critical('Error occurred when loading starting page', exc_info=True)
		return -1

	soup: object = BeautifulSoup(page.content, 'lxml')

	# First, extract all of the links leading to "View All" pages
	row_containers: list = soup.findAll('aside', class_='columns')
	viewall_links: list = ['https://oll.libertyfund.org' + x.find('a')['href'] for x in row_containers[1:4]] # Only want to pull the first 3

	# Now extract the rest of the links that are unique in the fact that they lead to pages that have
	#	the texts divided into pages (similar to a page of search results)
	extra_links: list = ['https://oll.libertyfund.org' + x['href'] for x in row_containers[4].findAll('a')]

	# Process the View All pages
	for viewall_page in viewall_links:
		page: object
		page_soup: object

		try:
			page = http.get(viewall_page)
			page.raise_for_status()
		except Exception as err:
			logger.warning(f'Failed to load View All page {viewall_page}, retrying in 3 seconds', exc_info=True)
			time.sleep(3)
			page = requests.get(viewall_page)

		page_soup = BeautifulSoup(page.content, 'lxml')

		# There is only one page of texts for this type of link,
		# 	so there isn't a need to put them in a queue first
		link_group: object = page_soup.find('ul', class_='group-member-listing')
		links: list = ['https://oll.libertyfund.org' + x['href'] for x in link_group.findAll('a')]

		for text_link in links:
			# First check if this text has multiple volumes. If it does,
			#	they need to be processed in a second loop to maintain
			#	the correct file index
			if 0:
				print()
			# Otherwise process the text as having one volume
			else:
				try:
					process_page(text_link + '#preview', fileindex)
					fileindex = fileindex + 1
				except Exception as err:
					fail_q.append(text_link)
					logger.warning(f'Processing of {text_link} failed, adding to fail queue', exc_info=True)

	# Process the divided pages

	#print(viewall_links)
	#print(extra_links)

scrape('https://oll.libertyfund.org/titles')

db_conn.close()