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
from dotenv import load_dotenv, find_dotenv
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create 'logs' and 'lib_texts' directories if they don't already exist
os.makedirs('logs/', exist_ok=True)
os.makedirs('lib_texts/', exist_ok=True)

# Custom logger
logger: logging.RootLogger = logging.getLogger("libertyfund_scraper")
logging.basicConfig(level = logging.INFO)

# File name for log files
logfilename: str = 'logs/log{:%Y-%m-%d}.log'.format(datetime.now())

# Flag to determine if the logger has already created a file
rollover: bool = os.path.isfile(logfilename)

# Handler for logger
# The FileHandler will also output logs to the terminal window, so an extra
# 	handler for that is not necessary
file_handler: logging.handlers.RotatingFileHandler = logging.handlers.RotatingFileHandler(logfilename, mode='w', backupCount=5, delay=True)

# Roll over file name if a log already exists
if rollover:
	file_handler.doRollover()

file_handler.setLevel(logging.INFO)

# Formatter for logger output
log_format: logging.Formatter = logging.Formatter('%(asctime)s\t: %(name)s : %(levelname)s -- %(message)s', '%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(log_format)

# Add to logger
logger.addHandler(file_handler)

# Load the environment variables
load_dotenv(find_dotenv())

# Connect to SQL database
db_conn: mysql.connector.MySQLConnection = mysql.connector.connect(
	user=os.environ.get('DB_USER'),
	password=os.environ.get('DB_PASS'),
	host=os.environ.get('DB_IP'),
	database=os.environ.get('DB_DB'))

db_cursor: mysql.connector.cursor.CursorBase = db_conn.cursor()

# Retry strategy that defines how and when to retry a failure on http.get
# Allows for 3 retries that are executed if any of the status_forcelist
# 	errors are encountered. backoff_factor = 1 determines the sleep time
# 	between failed requests. Increases exponentially: 0.5, 1, 2, 4, 8, etc.
retry_strat: Retry = Retry(
	total = 3,
	status_forcelist = [413, 429, 500, 502, 503, 504],
	allowed_methods = ["HEAD", "GET", "OPTIONS"],
	backoff_factor = 1
)

# Applies the retry strategy to all requests done through the http object
adapter: HTTPAdapter = HTTPAdapter(max_retries=retry_strat)
http: requests.session.Session = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

def process_page(browser: webdriver.Chrome, pageURL: str, index: int, timeout: int) -> None:
	title: str
	contribs: str
	file: file
	filename: str
	filepath: str

	sql_insert_stmt: str = (
		"INSERT INTO work_metadata(title, author, url, filepath, lccn)"
		"VALUES (%s, %s, %s, %s, %s)" )

	# Normally this would be encapsulated within a try block, but this
	#	function will be called from within a try block so any exceptions
	#	will be handled that way
	browser.get(pageURL)

	# Wait for the HTML preview to load before doing anything
	document_elem: bool = EC.presence_of_element_located((By.CLASS_NAME, 'document'))
	WebDriverWait(browser, timeout).until(document_elem)

	page_soup = BeautifulSoup(browser.page_source, 'lxml')

	# Extract title
	title = page_soup.find('h1').text.strip()[:255] # title is in first header

	# Extract author
	people_column: bs4.element.Tag = page_soup.find('div', class_='column')
	contribs = people_column.find('li').text[8:255] # first li is author; [8:] skips over leading 'Author: ' substring

	# Extract full text
	document: str = page_soup.find('div', class_='document').text

	# Store full text
	filename = f"lib_texts/lib{index}" + title[:5].replace(" ", "_") + ".txt"
	file = open(filename, 'a')
	file.write(document)

	filepath = filename

	file.close()

	print('File ' + filename + ' written.')

	# Put metadata in database
	try:
		data: tuple = (title, contribs, pageURL, filepath, '-1')
		db_cursor.execute(sql_insert_stmt, data)
		db_conn.commit()
	except Exception as err:
		db_conn.rollback()
		logger.warning("Error occurred when writing to databse", exc_info=True)

def process_links(browser: webdriver.Chrome, links: list, index: int, fail_q: deque) -> int:
	fileindex: int = index
	page: requests.models.Response

	if links == None:
		logger.warning("process_links(): None type object passed as links list, exiting")
		return 0

	if len(links) == 0:
		logger.warning("process_links(): Empty list passed in as links list, exiting")
		return 0

	if fail_q == None:
		logger.warning("process_links(): None type object passed for fail_q, exiting")
		return 0

	for text_link in links:
		# First check if this text has multiple volumes. If it does,
		#	they need to be processed in a second loop to maintain
		#	the correct file index
		page = http.get(text_link)
		page_soup = BeautifulSoup(page.content, 'lxml')

		# If the text has multiple volumes, this list will contain one element
		volume_header: list = [x for x in page_soup.findAll('h4') if x.text == 'Members of this set:']

		if len(volume_header) > 0:
			# Find the links leading to the other volumes and process them like a normal literature page
			ul_tags: bs4.element.ResultSet = page_soup.findAll('ul')

			for li in ul_tags[len(ul_tags) - 2].findAll('a'): # the <ul> containing the links we want is second to last
				vol_link: str = 'https://oll.libertyfund.org' + li['href']

				try:
					process_page(browser, vol_link + '#preview', fileindex, 10)
					fileindex = fileindex + 1
				except Exception as err:
					fail_q.append(vol_link)
					logger.warning(f'Processing of {vol_link} failed, adding to fail queue', exc_info=True)
		# Otherwise process the text as having one volume
		else:
			try:
				process_page(browser, text_link + '#preview', fileindex, 10)
				fileindex = fileindex + 1
			except Exception as err:
				fail_q.append(text_link)
				logger.warning(f'Processing of {text_link} failed, adding to fail queue', exc_info=True)

	return fileindex

def scrape(startingURL: str) -> int:
	q: deque = deque()
	fail_q: deque = deque()
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
		page: requests.models.Response = http.get(startingURL)
		page.raise_for_status()
	except Exception as err:
		logger.critical('Error occurred when loading starting page', exc_info=True)
		return -1

	# The full text is loaded using Javascript after the page loads,
	#	so a headless browser will need to be spun up to see it as
	#	the requests library can't handle Javascript
	opts: Options = Options()
	opts.headless = True
	opts.add_argument('window-size=1920x1080')
	browser = Chrome(executable_path='/home/chris/chromedriver', options=opts)

	soup: BeautifulSoup = BeautifulSoup(page.content, 'lxml')

	# First, extract all of the links leading to "View All" pages
	row_containers: list = soup.findAll('aside', class_='columns')
	viewall_links: list = ['https://oll.libertyfund.org' + x.find('a')['href'] for x in row_containers[1:4]] # Only want to pull the first 3

	# Now extract the rest of the links that are unique in the fact that they lead to pages that have
	#	the texts divided into pages (similar to a page of search results)
	extra_links: list = ['https://oll.libertyfund.org' + x['href'] for x in row_containers[4].findAll('a')]

	# Process the View All pages
	for viewall_page in viewall_links:
		page: requests.models.Response
		page_soup: BeautifulSoup

		try:
			page = http.get(viewall_page)
			page.raise_for_status()
		except Exception as err:
			logger.warning(f'Failed to load View All page {viewall_page}, retrying in 3 seconds', exc_info=True)
			time.sleep(3)
			page = http.get(viewall_page)
			page.raise_for_status()

		page_soup = BeautifulSoup(page.content, 'lxml')

		# There is only one page of texts for this type of link,
		# 	so there isn't a need to put them in a queue first
		link_group: bs4.element.Tag = page_soup.find('ul', class_='group-member-listing')
		links: list = ['https://oll.libertyfund.org' + x['href'] for x in link_group.findAll('a')]

		fileindex = process_links(browser, links, fileindex, fail_q)

	# Process the divided pages
	for extra_page in extra_links:
		page: requests.models.Response
		page_soup: BeautifulSoup

		try:
			page = http.get(extra_page)
			page.raise_for_status()
		except Exception as err:
			logger.warning(f'Failed to load Extra page {extra_page}, retrying in 3 seconds', exc_info=True)
			time.sleep(3)
			page = http.get(extra_page)
			page.raise_for_status()

		# Loop forever until it is broken by there not being a Next Page to advance to
		while True:
			page_soup = BeautifulSoup(page.content, 'lxml')
			next_page: bs4.element.Tag = page_soup.find('a', rel='next')

			# All links to literature pages have '/title/' in them, so extracting all the literature links
			#	from these pages is simple
			title_links: list = ['https://oll.libertyfund.org' + x['href'] for x in page_soup.findAll('a', href=True) if '/title/' in x['href']]

			fileindex = process_links(browser, title_links, fileindex, fail_q)

			if next_page == None:
				break

			try:
				page = http.get('https://oll.libertyfund.org' + next_page['href'])
				page.raise_for_status()
			except Exception as err:
				logger.warning(f'Failed to load next page {str(next_page)}, retrying in 3 seconds', exc_info=True)
				time.sleep(3)
				page = http.get('https://oll.libertyfund.org' + next_page['href'])
				page.raise_for_status()

	# Since the main process has finished, we can now process the failure queue
	logger.info('Main scraping process finished, now processing fail_q with ' + str(len(fail_q)) + ' entries.')
	while len(fail_q) > 0:
		litpage: str = fail_q.popleft()

		try:
			process_page(browser, litpage, fileindex, 30) # increased timeout length in case it just took too long to load
			fileindex = fileindex + 1
		except Exception as err:
			logger.critical(f'Processing of {litpage} failed a second time.', exc_info=True)

	browser.quit()

scrape('https://oll.libertyfund.org/titles')

db_conn.close()
