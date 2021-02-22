import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time
import logging
import logging.handlers
import os
import mysql.connector
import bs4
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from collections import deque
from bs4 import BeautifulSoup

# TODO look into 'begins' library for beautifying the command-line interface

# Create 'logs' and 'loc_texts' directories if they don't already exist
os.makedirs('logs/', exist_ok=True)
os.makedirs('loc_texts/', exist_ok=True)

# Custom logger
logger: logging.RootLogger = logging.getLogger("loc_scraper")
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
http: requests.sessions.Session = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

def process_page(pageURL: str, index: int) -> None:
	page: requests.models.Response
	jsonpage: dict

	sql_insert_stmt: str = (
		"INSERT INTO work_metadata(title, author, url, filepath, lccn)"
		"VALUES (%s, %s, %s, %s, %s)" )

	# Storage for metadata entry values
	title: str
	contribs: str
	lccn: str
	filepath: str

	# Add a short delay so we don't overload the corpus server
	time.sleep(1)

	page = http.get(pageURL + "?fo=json")
	page.raise_for_status()
	jsonpage = page.json()

	fulltext_link: str

	for c in jsonpage.get('resources'):
		fulltext_link = c.get('fulltext_file')

	# Extract Metadata
	try:
		title = jsonpage.get('item').get('title')[:255] # Limit to 255 characters to fit in table entry
	except:
		logger.info(f'No title provided for {pageURL}')
		title = "NoTitle"

	contrib_list: list = jsonpage.get('item').get('contributor_names')

	if contrib_list == None:
		logger.info(f'No contributors listed for {pageURL}')
		contribs = 'NoContribs'
	else:
		contribs = ", ".join(str(x) for x in contrib_list)[:255]

	lccn = jsonpage.get('item').get('library_of_congress_control_number')

	if lccn == None:
		logger.info(f'No LCCN provided for {pageURL}')
		lccn = '-1'

	# Extract written text

	page = http.get(fulltext_link)
	page.raise_for_status()

	soup = BeautifulSoup(page.content, 'xml')

	results: bs4.element.Tag = soup.find(name='text')
	text_elems: bs4.element.ResultSet = results.find_all('boidy')

	filename: str = f"loc_texts/loc{index}" + title[:5].replace(" ", "_") + ".txt"

	# Output text to file
	with open(filename, 'a') as file:

		for elem in text_elems:
			file.write(elem.text)
	
		filepath = filename
	
	print("File " + filename + " written.")

	# Put the metadata in the database
	try:
		data: tuple = (title, contribs, pageURL, filepath, lccn)
		db_cursor.execute(sql_insert_stmt, data)
		db_conn.commit()
	except Exception as err:
		db_conn.rollback()
		logger.warning("Error occurred when writing to database", exc_info=True)

# The main scraper method
# Takes in a starting URL and puts it in a deque. That URL
# is then popped off and the scraper begins traversing 
# through the pages. The end result should be text files
# containing the full written text of each piece of literature
# contained in a corpus along with entries in the database
# for the metadata about each piece of literature.
def scrape(startingURL: str, starting_index: int) -> int:
	q: deque = deque()
	fail_q: deque = deque()
	fileindex: int = starting_index

	if(startingURL == None):
		logger.critical('\'None\' type received as input, exiting')
		return -3

	# Check the URL to make sure it leads to the website we want to scrape
	if not 'loc.gov' in startingURL:
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

	soup: BeautifulSoup = BeautifulSoup(page.content, 'lxml')

	# Loop until we have exhausted the contents of this corpus
	while True:

		# Queue up each piece of literature on the page
		search_items: bs4.element.ResultSet = soup.findAll('li', class_ = ['item first', 'item']) # first result is a different name for whatever reason
		next_page: bs4.element.Tag = soup.find('a', class_ = 'next')

		for item in search_items:
			linksoup: BeautifulSoup = BeautifulSoup(item.prettify(), 'lxml')
			links: bs4.element.ResultSet = linksoup.findAll('a')
			q.append(links[0].attrs['href'])

		# Go through the queue of results, first extracting their metadata then the full text
		while len(q) > 0:
			litpage: str = q.popleft()

			# Encapsulate this call in a try block to capture all exceptions thrown because of HTTP requests
			try:
				process_page(litpage, fileindex)
			except Exception as err:
				# With an error found, put the page that caused it into the failure queue so it can be processed again
				fail_q.append(litpage)
				logger.warning(f'Processing of {litpage} failed, adding to fail queue', exc_info=True)

			fileindex = fileindex + 1

		# Load up the next page of results, if there is one
		# If not, return successful exit code

		# MODIFICATION FOR UNIT TEST
		#next_page = None
		# END MODIFICATION

		# End of the corpus has been reached, exit loop
		if next_page == None:
			break

		print("NEXT PAGE")
		try:
			page = http.get(next_page.attrs['href'])
			page.raise_for_status()
		except Exception as err:
			logger.warning(f'Failed to load next page of results, trying again after 3 seconds', exc_info=True)
			time.sleep(3)
			page = http.get(next_page.attrs['href'])

		soup = BeautifulSoup(page.content, 'lxml')

	# Since the main process has finished, we can now process the failure queue
	logger.info('Main scraping process finished, now processing fail_q with ' + str(len(fail_q)) + ' entries.')
	while len(fail_q) > 0:
		litpage: str = fail_q.popleft()

		try:
			process_page(litpage, fileindex)
		except Exception as err:
			logger.critical(f'Processing of {litpage} failed a second time.', exc_info=True)

		fileindex = fileindex + 1

	return fileindex

# Books published between 1600 and 1699, inclusive
next_start: int = scrape("https://www.loc.gov/books/?dates=1600/1699&fa=online-format:online+text%7Clanguage:english", 1)
print("finished 1600-1699")
# Books published between 1700 and 1709, inclusive
next_start = scrape("https://www.loc.gov/books/?dates=1700/1709&fa=online-format:online+text%7Clanguage:english", next_start)
# 1710-1719
next_start = scrape("https://www.loc.gov/books/?dates=1710/1719&fa=online-format:online+text%7Clanguage:english", next_start)
# 1720-1729
next_start = scrape("https://www.loc.gov/books/?dates=1720/1729&fa=online-format:online+text%7Clanguage:english", next_start)
# 1730-1739
next_start = scrape("https://www.loc.gov/books/?dates=1730/1739&fa=online-format:online+text%7Clanguage:english", next_start)
# 1740-1749
next_start = scrape("https://www.loc.gov/books/?dates=1740/1749&fa=online-format:online+text%7Clanguage:english", next_start)
# 1750
next_start = scrape("https://www.loc.gov/books/?dates=1750&fa=online-format:online+text%7Clanguage:english", next_start)
# 1751
next_start = scrape("https://www.loc.gov/books/?dates=1751&fa=online-format:online+text%7Clanguage:english", next_start)
# 1752
next_start = scrape("https://www.loc.gov/books/?dates=1752&fa=online-format:online+text%7Clanguage:english", next_start)
# 1753
next_start = scrape("https://www.loc.gov/books/?dates=1753&fa=online-format:online+text%7Clanguage:english", next_start)
# 1754
next_start = scrape("https://www.loc.gov/books/?dates=1754&fa=online-format:online+text%7Clanguage:english", next_start)
# 1755
scrape("https://www.loc.gov/books/?dates=1755&fa=online-format:online+text%7Clanguage:english", next_start)

db_conn.close()
