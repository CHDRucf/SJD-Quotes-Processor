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

def process_page() -> None:
	return

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

	#print(viewall_links)
	print(extra_links)

scrape('https://oll.libertyfund.org/titles')