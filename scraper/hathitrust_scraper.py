import time
import logging
import logging.handlers
import os
import shutil
import mysql.connector
from datetime import datetime
from collections import deque
from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

def process_page(page: list, index: int, browser: object) -> None:
	page: object
	filename: str
	filepath: str

	sql_insert_stmt: str = (
		"INSERT INTO Metadata(title, author, url, filepath)"
		"VALUES (%s, %s, %s, %s)" )

	# The login session will be preserved, so loading the literature page
	# 	will allow access to what we need to efficiently scrape each
	# 	piece of literature
	browser.get(page[0])

	# Wait for the page to load before trying to access Full View of the text
	section_elem: bool = EC.presence_of_element_located((By.ID, 'section'))
	WebDriverWait(browser, 5).until(section_elem)

	# The buttons to Full View are contained in a table, so it is easiest to
	#	simply access the first button directly using its XPath
	browser.find_element_by_xpath('//*[@id="section"]/article/table[2]/tbody/tr[1]/td[1]/a').click()
	
	# Advance to the text-only view
	browser.find_element_by_id('ssd-link').click()

	# Wait for the page to load before getting the page's HTML
	text_page: bool = EC.presence_of_element_located((By.ID, 'seq1'))
	WebDriverWait(browser, 10).until(text_page)

	soup: object = BeautifulSoup(browser.page_source, 'lxml')
	text_containers: list = soup.findAll('p', class_='Text')

	# Create and write to the text file
	filename = f"hat{index}" + page[1][:5].replace(" ", "_") + ".txt"
	file: object = open(filename, 'a')

	for text_elem in text_containers:
		file.write(text_elem.text)

	filepath = os.path.abspath(file.name)

	file.close()

	print(f'File {filename} written.')

	try:
		data: tuple = (page[1], page[2], page[0], filepath)
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
	opts: object
	browser: object
	USER: str
	PASS: str

	if(startingURL == None):
		logger.critical('\'None\' type received as input, exiting')
		return -3

	# Check the URL to make sure it leads to the website we want to scrape
	if not 'hathitrust.org' in startingURL:
		logger.critical(startingURL + ' is either an invalid URL or not the target of the scraper')
		return -2

	# Set up a headless Chrome instance and configure file download settings
	#	such that downloads are stored in a different directory and there is no
	#	prompt window popping up each time
	chromeopts = webdriver.ChromeOptions()
	chromeopts.headless = True
	chromeopts.add_argument('window-size=1920x1080')
	prefs = {"download.default_directory" : "/tmp/scraper-downloads/",
		 	 "download.prompt-for-download" : False,
		 	 "directory_upgrade" : True}
	chromeopts.add_experimental_option('prefs', prefs)
	browser = Chrome(chrome_options=chromeopts)

	# Load the starting page (assumed to be the result of a search)
	# If the starting page doesn't load on first try, exit with error code
	try:
		browser.get(startingURL)
	except Exception as err:
		logger.critical('Error occurred when loading starting page', exc_info=True)
		return -1

	# Navigate through the login process and log in using the 
	# 	credentials stored in .env
	browser.find_element_by_id('login-link').click()
	browser.find_element_by_id('select2-idp-container').click()

	textbox = browser.find_element_by_class_name('select2-search__field')
	textbox.send_keys('University of Central Florida')
	textbox.send_keys(Keys.ENTER)

	browser.find_element_by_class_name('continue').click()

	# Load in the stored credentials
	load_dotenv(find_dotenv())
	USER = os.environ.get('USER')
	PASS = os.environ.get('PASS')

	# wait for the login page to load before trying to populate
	#	credential fields
	user_elem: bool = EC.presence_of_element_located((By.ID, 'username'))
	WebDriverWait(browser, 5).until(user_elem)

	# Finish the login
	# The site will redirect back to where we started the login from,
	# 	allowing us to continue the scraping process without manually loading
	# 	an extra webpage
	browser.find_element_by_id('username').send_keys(USER)
	browser.find_element_by_id('password').send_keys(PASS)
	browser.find_element_by_class_name('btn-lg').click()

	# Wait for the page to finish loading, then pass the page's HTML
	# 	into the parser
	section_elem: bool = EC.presence_of_element_located((By.ID, 'section'))
	WebDriverWait(browser, 5).until(section_elem)

	soup: object = BeautifulSoup(browser.page_source, 'lxml')

	# Loop until we have exhausted the contents of this corpus
	while True:
		search_items: object = soup.findAll('article', class_='record')
		next_page: str
		title: str
		contribs: str

		next_page_container: object = soup.find('div', class_='page-advance-link')
		next_page = next_page_container.find('a')['href']

		for item in search_items:
			metasoup: object = BeautifulSoup(item.prettify(), 'lxml')
			catalog_link: object = metasoup.find('a', href=True, class_='cataloglinkhref')
			metadata_objs: object = metasoup.findAll('dd')

			# Extract title, limiting it to 255 characters
			title = metasoup.find('span', class_='title').text.strip()[:255]

			# Extract author(s), limiting the resulting string to 255 characters
			contribs = ", ".join(x.text.strip() for x in metadata_objs[1:])[:255] # the first 'dd' tag is the publication date so we skip it here

			# The page that results from the link here does not have
			#	the full list of contributors if there are more than one, 
			#	so the full list that is extracted from the page of search
			# 	results is compiled into a list along with the link 
			#	and title strings
			q.append(['https://catalog.hathitrust.org' + catalog_link['href'], title, contribs])

		# Go through the queue of results, saving the metadata to the database then the full text to the file system
		while len(q) > 0:
			litpage: list = q.popleft()

			# Capture all exceptions happening within process_page
			try:
				process_page(litpage, fileindex, browser)
			except Exception as err:
				# Error found -> put failed page into fail_q coupled with the title and contribs strings
				fail_q.append(litpage)
				logger.warning(f'Processing of {litpage[0]} failed, adding to fail queue', exc_info=True)

			fileindex = fileindex + 1

		# MODIFICATION FOR UNIT TEST
		#next_page = None
		# END UNIT TEST MODIFICATION

		if next_page == None:
			break

		print("NEXT PAGE")
		try:
			page = browser.get(next_page)
		except Exception as err:
			logger.warning(f'Failed to load next page of results, trying again after 3 seconds', exc_info=True)
			time.sleep(3)
			page = browser.get(next_page)

		# Wait for next page to load then pass its HTML into the parser
		section_elem: bool = EC.presence_of_element_located((By.ID, 'section'))
		WebDriverWait(browser, 5).until(section_elem)
		
		soup = BeautifulSoup(browser.page_source, 'lxml')

		# Process failure queue
		while len(fail_q) > 0:
			litpage: list = fail_q.popleft()

			# Capture all exceptions happening within process_page
			try:
				process_page(litpage, fileindex, browser)
			except Exception as err:
				logger.critical(f'Processing of {litpage[0]} failed a second time', exc_info=True)

			fileindex = fileindex + 1

	# Clean up time
	browser.quit()

	return 0

# Everything published during or before 1755
scrape("https://catalog.hathitrust.org/Search/Home?fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&page=1&pagesize=20&ft=ft")

db_conn.close()