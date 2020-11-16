import requests
import time
import logging
import os
import mysql.connector
from datetime import datetime
from collections import deque
from bs4 import BeautifulSoup

# TODO look into 'begins' library for beautifying the command-line interface

# Create 'logs' directory if it doesn't already exist
os.makedirs('logs/', exist_ok=True)

# Custom logger
logger: object = logging.getLogger("loc_scraper")

# Handlers for logger
stream_handler: object = logging.StreamHandler()
file_handler: object = logging.FileHandler('logs/log{:%Y-%m-%d}.log'.format(datetime.now()), mode='a')
stream_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.WARNING)

# Formatter for logger output
log_format: object = logging.Formatter('%(asctime)s\t: %(name)s : %(levelname)s -- %(message)s', '%Y-%m-%d %H:%M:%S')
stream_handler.setFormatter(log_format)
file_handler.setFormatter(log_format)

# Add to logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

# Connect to SQL database
db_conn: object = mysql.connector.connect(
	user='root',
	password='password',
	host='127.0.0.1',
	database='test')

db_cursor: object = db_conn.cursor()

def processPage(pageURL: str, index: int) -> None:
	page: object
	jsonpage: object

	sql_insert_stmt: str = (
		"INSERT INTO Metadata(title, author, url, filepath)"
		"VALUES (%s, %s, %s, %s)" )

	# Storage for metadata entry values
	title: str
	contribs: str
	filepath: str

	page = requests.get(pageURL + "?fo=json")
	page.raise_for_status()
	jsonpage = page.json()

	fulltext_link: str
	#page = requests.get(litpage)
	soup = BeautifulSoup(page.content, 'lxml')

	# try:
	# 	for c in jsonpage.get('item').get('contributor_names'):
	# 		#print(list(c.keys())[0])
	# 		print(c)
	# except:
	# 	print("no contribs")

	for c in jsonpage.get('resources'):
		fulltext_link = c.get('fulltext_file')

	# for collections in jsonpage.get('item'):
	# 	try:
	# 		print(type(jsonpage.get('item')))
	# 		print(jsonpage.get)
	# 	except:
	# 		print("No contributors listed")

	#print(jsonpage.json()["item"]["contributors"])

	# Extract Metadata
	try:
		title = jsonpage.get('item').get('title')[:255] # Limit to 255 characters to fit in table entry
	except:
		logger.info(f'No title provided for {pageURL}')

	contrib_list: list = jsonpage.get('item').get('contributor_names')

	if contrib_list == None:
		logger.info(f'No contributors listed for {pageURL}')
		contribs = 'None'
	else:
		contribs = " ".join(str(x) for x in contrib_list)

	# Extract written text
	#pagelinks = soup.findAll('a')

	page = requests.get(fulltext_link)
	page.raise_for_status()

	soup = BeautifulSoup(page.content, 'xml')

	results: object = soup.find(name = 'text')
	text_elems: object = results.find_all('body')

	filename: str = f"literature{index}.txt"

	# Output text to file
	file: object = open(filename, "a")

	for elem in text_elems:
		file.write(elem.text)

	filepath = os.path.realpath(file.name)

	file.close()
	print("File " + filename + " written.")

	# Put the metadata in the database
	try:
		data: tuple = (title, contribs, pageURL, filepath)
		db_cursor.execute(sql_insert_stmt, data)
		db_conn.commit()
	except Exception as err:
		db_conn.rollback()
		logger.warning("Error occurred when writing to databse", exc_info=True)

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

	# Load the starting page (assumed to be the result of a search) and begin parsing
	# If the starting page doesn't load on first try, exit with error code
	try:
		page: object = requests.get(startingURL)
		page.raise_for_status()
	except Exception as err:
		logger.critical('Error occurred when loading starting page', exc_info=True)
		return -1

	soup: object = BeautifulSoup(page.content, 'lxml')

	# Loop until we have exhausted the contents of this corpus
	while True:

		# Queue up each piece of literature on the page
		search_items: object = soup.findAll('li', class_ = ['item first', 'item']) # first result is a different name for whatever reason
		next_page: object = soup.find('a', class_ = 'next')

		for item in search_items:
			linksoup: object = BeautifulSoup(item.prettify(), 'lxml')
			links: object = linksoup.findAll('a')
			q.append(links[0].attrs['href'])
			# print(links[0].attrs['href'])

		# Go through the queue of results, first extracting their metadata then the full text
		while len(q) > 0:
			litpage: str = q.popleft()

			# Encapsulate this call in a try block to capture all exceptions thrown because of HTTP requests
			try:
				processPage(litpage, fileindex)
			except Exception as err:
				# With an error found, put the page that caused it into the failure queue so it can be processed again
				fail_q.append(litpage)
				logger.warning(f'Processing of {litpage} failed, adding to fail queue', exc_info=True)

			fileindex = fileindex + 1

		# Load up the next page of results, if there is one
		# If not, return successful exit code
		if next_page == None:
			return 0

		print("NEXT PAGE")
		try:
			page = requests.get(next_page.attrs['href'])
			page.raise_for_status()
		except Exception as err:
			logger.warning(f'Failed to load next page of results, trying again after 3 seconds', exc_info=True)
			time.sleep(3)
			page = requests.get(next_page.attrs['href'])

		soup = BeautifulSoup(page.content, 'lxml')

scrape("https://www.loc.gov/books/?fa=online-format%3Aonline+text&dates=1700%2F1799&st=list&c=25")

db_conn.close()