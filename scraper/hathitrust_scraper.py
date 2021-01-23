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

# opts = Options()
# opts.set_headless()
# assert opts.headless
# browser = Chrome(options=opts)
# browser.get('https://www.google.com/')
# browser.quit()

# TODO look into 'begins' library for beautifying the command-line interface

# Create 'logs' directory if it doesn't already exist
os.makedirs('logs/', exist_ok=True)

# Custom logger
logger: object = logging.getLogger("hathitrust_scraper")
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

# The main scraper method
# Takes in a starting URL and puts it in a deque. That URL
# is then popped off and the scraper begins traversing 
# through the pages. The end result should be text files
# containing the full written text of each piece of literature
# contained in a corpus along with entries in the database
# for the metadata about each piece of literature.
def scrape(startingURL: str) -> int:
	q: object = deque()
	fail_q: object = deque()
	fileindex: int = 1

	if(startingURL == None):
		logger.critical('\'None\' type received as input, exiting')
		return -3

	# Check the URL to make sure it leads to the website we want to scrape
	if not 'hathitrust.org' in startingURL:
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

	# Loop until we have exhausted the contents of this corpus
	while True:
		search_items: object = soup.findAll('article', class_='record')
		next_page: object = soup.find('a', href=True, text='Next Page ') # the text on this button has an extra space at the end

		for item in search_items:
			metasoup: object = BeautifulSoup(item.prettify(), 'lxml')
			catalog_link: object = metasoup.find('a', href=True, class_='cataloglinkhref')
			metadata_objs: ResultSet = metasoup.findAll('dd')

			title: str = metasoup.find('span', class_='title').text.strip()
			contribs: str

			# Extract author(s)
			contribs = ", ".join(x.text.strip() for x in metadata_objs[1:])

			print(title)
			print(contribs)

			#for dd in metadata_objs[1:]: # the first 'dd' tag is the publication date which we don't care about here
			#	print(dd.text)

			q.append('https://catalog.hathitrust.org' + catalog_link['href'])

		#while len(q) > 0:

		#if next_page == None:
		break

	return 1

# Everything published during or before 1755
scrape("https://catalog.hathitrust.org/Search/Home?fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&fqor-format%5B%5D=Dictionaries&fqor-format%5B%5D=Encyclopedias&fqor-format%5B%5D=Journal&fqor-format%5B%5D=Manuscript&fqor-format%5B%5D=Newspaper&filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&page=1&pagesize=20&ft=ft")