import re
import os
import sys
import time
import logging
import logging.handlers
from datetime import datetime
import mysql.connector
from csv import reader
import filecmp
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from SPARQLWrapper import SPARQLWrapper, JSON

# Get the directory to search from the user
base_dir: str = input("Enter the base directory of the literature files: ")
print_to_terminal: str = input("Output prints to terminal? (y/n)")

# Remove trailing '/' if it was given
if base_dir[-1] == '/':
	base_dir = base_dir[:-1]

os.makedirs('logs/', exist_ok=True)

# Custom logger
logger: logging.RootLogger = logging.getLogger("reduce_corpora")
logger.setLevel(logging.DEBUG)

# File name for log files
logfilename: str = 'logs/match_log{:%Y-%m-%d}.log'.format(datetime.now())

# Flag to determine if the logger has already created a file
rollover: bool = os.path.isfile(logfilename)

# Handler for log files
# The FileHandler will also output logs to the terminal window, so an extra
# 	handler for that is not necessary
file_handler: logging.handlers.RotatingFileHandler = logging.handlers.RotatingFileHandler(logfilename, mode='w', backupCount=5, delay=True)

# Handler for terminal log entries
print_handler: logging.StreamHandler = logging.StreamHandler()

if 'y' in print_to_terminal.lower():
	print_handler.setLevel(logging.DEBUG)
else:
	print_handler.setLevel(logging.INFO)

# Roll over file name if a log already exists
if rollover:
	file_handler.doRollover()

file_handler.setLevel(logging.DEBUG)

# Formatter for logger output
log_format: logging.Formatter = logging.Formatter('%(asctime)s\t: %(name)s : %(levelname)s -- %(message)s', '%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(log_format)
print_handler.setFormatter(log_format)

# Add to logger
logger.addHandler(file_handler)
logger.addHandler(print_handler)

# Connect to SQL database
db_conn: mysql.connector.MySQLConnection = mysql.connector.connect(
	user=os.environ.get('DB_USER'),
	password=os.environ.get('DB_PASS'),
	host=os.environ.get('DB_IP'),
	database=os.environ.get('DB_DB'))

db_cursor: mysql.connector.cursor.CursorBase = db_conn.cursor()

# This will go through the gut_texts and lib_texts directories and
#	remove all files/database entries that are seen as not published
#	within the range we care about.
# This uses a regular expression to find "dates" within the files, so it is
#	not very accurate. This was not used in the final reduction of the
#	corpora, but I figured the code should stay in case it is useful
#	in the future.
def remove_texts_out_of_range() -> None:
	re_date: object = re.compile(r'\b1([0-9][0-9][0-9])\b')
	in_range_count: int = 0
	match_count: int = 0
	dirs: list = ['gut_texts', 'lib_texts']

	for pdir in dirs:
		logger.info(f'Checking texts in {base_dir}/{pdir}...')

		# Walk the directory of files
		for path, _, files in os.walk(os.path.abspath(f'{base_dir}/{pdir}')):
			# Process each file in the directory
			for f in files:
				filepath: str = os.path.join(path, f)

				with open(filepath, mode='r', encoding='utf8') as file:
					# Read the file line by line, checking for a string match.
					#	If a match is found, print the line it was found on
					#	and the file path
					largest_match: int = 0
					for index, line in enumerate(file):
						match: object = re_date.search(line)

						# Found a match -> print the line & file then end loop
						# In a lot of the gutenberg files, the first match is some address in
						#	Salt Lake City so it is best to skip over that one
						if match and 'salt lake city' not in line.lower():
							match_count = match_count + 1
							date: int = int(match[0])

							# Keep the ones that are in range, but remove the file and database entry
							#	for the ones that are not
							if date > 1755:
								logger.debug(f'OUT OF RANGE match {match[0]} found in {filepath} on line {index}:\n\t{line}')
								# Find the entry in the database containing this file and delete both
								#	the entry and the file

								## This code was left commented so nothing gets
								## accidentally deleted.

								# try:
								# 	db_cursor.execute(f'SELECT id FROM work_metadata WHERE filepath LIKE "{pdir}/{f}"')
								# except Exception as err:
								# 	print(f'{pdir}/{f}')
								# 	logger.error(f'Problem finding file in database:', exc_info=True)
								# else:
								# 	results: list = db_cursor.fetchall()
								# 	#print(results)
							else:
								logger.debug(f'In-range match {match[0]} found in {filepath} on line {index}:\n\t{line}')
								in_range_count = in_range_count + 1

							break

		logger.info(f'Found {in_range_count} files in {pdir} containing a match within the desired range.')
		logger.info(f'{match_count} contained a match in general.')

		in_range_count = 0
		match_count = 0

	logger.info(f'Matches can be found in {logfilename}')

def remove_unknown_titleauthor() -> None:
	db_cursor.execute('SELECT id, filepath FROM work_metadata WHERE title LIKE "UNKNOWN%" AND author LIKE "UNKNOWN%";')
	results: list = db_cursor.fetchall()

	logger.info(f'Removing {len(results)} files and database entries with UNKNOWN title & author...')
	
	for index, elem in enumerate(results):
		try:
			os.remove(f'{base_dir}/{elem[1]}')
			db_cursor.execute(f'DELETE FROM work_metadata WHERE id = {elem[0]}')
			db_conn.commit()
		except Exception as err:
			logger.critical(f'Problem removing file or database entry for {elem[1]}: ', exc_info=True)

	logger.info('Done.')

def remove_duplicates() -> None:
	# The entries that have duplicates have been stored in a csv file,
	#	so we can just read the title and author combos and work with
	#	them directory instead of searching again

	equivalent: int = 0

	with open('query.csv', 'r') as csv_file:
		csv_reader: reader = reader(csv_file, delimiter='\t')

		# Skip over the header
		header: str = next(csv_reader)

		# Iterate over the file if it's not empty
		if header != None:
			for row in csv_reader:
				title: str = row[0].replace('"', '\\"').replace("'", "\\'")
				author: str = row[1]

				# Find all entries with this title and author
				db_cursor.execute(f'SELECT id, filepath FROM work_metadata WHERE title LIKE "{title}" AND author LIKE "{author}"')
				results: list = db_cursor.fetchall()
				keep: list = []
				remove: list = []

				# Compare the contents of each file to all of the other suspected duplicates
				for res in results:
					filepath1: str = f'{base_dir}/{res[1]}'

					for res2 in results:
						filepath2 = f'{base_dir}/{res2[1]}'
						
						# Make sure we're not comparing the file to itself before we do the comparison
						if filepath1 != filepath2:
							# If the files are exactly equivalent, we can remove one of the duplicate
							#	files and database entries
							if filecmp.cmp(filepath1, filepath2):
								logger.debug(f'{filepath1} and {filepath2} are exactly equivalent.')

								if res not in keep:
									keep.append(res)

								if res2 not in keep and res2 not in remove:
									remove.append(res2)

				# Remove all texts in the 'remove' list
				for item in remove:
					db_cursor.execute(f'DELETE FROM work_metadata WHERE id = {item[0]}')
					db_conn.commit()

					os.remove(f'{base_dir}/{item[1]}')

					equivalent = equivalent + 1

	print(f'{equivalent} duplicate files were removed.')					

def remove_sj_books_and_dicts() -> None:
	db_cursor.execute("SELECT id, filepath FROM work_metadata WHERE author LIKE '%Samuel Johnson%' OR author LIKE '%Johnson, Samuel%'")
	books_by_sj: list = db_cursor.fetchall()

	db_cursor.execute("SELECT id, filepath FROM work_metadata WHERE title LIKE '%dictionary%'")
	dict_books: list = db_cursor.fetchall()

	for book in books_by_sj:
		db_cursor.execute(f"DELETE FROM work_metadata WHERE id = {book[0]}")
		db_conn.commit()
		os.remove(f'{base_dir}/{book[1]}')

	for book in dict_books:
		db_cursor.execute(f"DELETE FROM work_metadata WHERE id = {book[0]}")
		db_conn.commit()
		os.remove(f'{base_dir}/{book[1]}')

	print(f'Removed {len(books_by_sj) + len(dict_books)} works.')

def verify_author_publication_dates(browser: webdriver.Chrome, author: str) -> list:
	loc_search_page: str = 'https://catalog.loc.gov/vwebv/searchAdvanced'
	hat_search_page: str = 'https://catalog.hathitrust.org/Search/Advanced'
	re_date: object = re.compile(r'\b1([0-9][0-9][0-9])\b')

	# Get all Gutenberg texts from the database
	db_cursor.execute(f"SELECT id, title, filepath FROM work_metadata WHERE author LIKE {author}")
	texts: list = db_cursor.fetchall()

	in_range_count: int = 0
	texts_no_result: int = 0
	texts_removed: int = 0
	
	# Search the HathiTrust catalog for each text. If no results were found, 
	#	do another search on Library of Congress
	for i, text in enumerate(texts):
		text_id: int = text[0]
		text_title: str = text[1]
		text_filepath: str = text[2]

		time.sleep(2)

		# Each search needs to begin on a fresh search page
		browser.get(hat_search_page)

		# Wait until the text boxes show up before trying to enter the title/author
		search_box: EC.presence_of_element_located = EC.presence_of_element_located((By.ID, 'field-search-text-input-1'))
		WebDriverWait(browser, 5).until(search_box)

		# Enter title and author into text boxes and select the corresponding
		#	options in the dropdowns to specify where to search in
		browser.find_element_by_id('field-search-text-input-1').send_keys(text_title)
		browser.find_element_by_id('field-search-text-input-2').send_keys(author)

		dropdown_title: Select = Select(browser.find_element_by_xpath('//*[@id="section"]/form/fieldset[1]/div/select'))
		dropdown_title.select_by_value('title')

		dropdown_author: Select = Select(browser.find_element_by_xpath('//*[@id="section"]/form/fieldset[2]/div/select'))
		dropdown_author.select_by_value('author')

		# Selecting the 'OR' radio button seems to yield better results
		#browser.find_element_by_xpath('//*[@id="section"]/form/fieldset[2]/fieldset/div[2]/label').click()

		browser.find_element_by_class_name('button.btn.btn-primary').click()

		# Wait for the page to load before grabbing the HTML
		results_intro: EC.presence_of_element_located = EC.presence_of_element_located((By.CLASS_NAME, 'listcs-intro'))
		WebDriverWait(browser, 5).until(results_intro)

		soup: BeautifulSoup = BeautifulSoup(browser.page_source, 'lxml')

		# Check if no results were found
		result_desc: bs4.element.Tag = soup.find('h2', class_='results-summary')

		if result_desc != None:
			# If no results on HathiTrust, need to search on LOC
			if 'No results matched your search' not in result_desc.text:
				list_term: bs4.element.ResultSet = soup.find('dt')
				list_desc: bs4.element.ResultSet = soup.find('dd')
				pub_date: int = 0

				# Sometimes a publication date isn't listed, so instead of trying
				#	to access it directly we need to look for it. If there isn't one,
				#	then pub_date will remain 0 and we will count this text as within
				#	range to be on the safe side.
				if 'Published' in list_term.text:
					pub_date = int(list_desc.text)

				# Remove all texts published outside our cutoff date
				if pub_date > 1755:
					db_cursor.execute(f'DELETE FROM work_metadata WHERE id = {text_id}')
					db_conn.commit()
					os.remove(f'{base_dir}/{text_filepath}')

					texts_removed = texts_removed + 1
			else:
				texts_no_result = texts_no_result + 1

	# print(f'Out of {len(gut_texts)} texts, {in_range_count} were in the date range.')

	return [texts_no_result, texts_removed]

def verify_author_birthdates() -> None:
	re_date: object = re.compile(r'\b1([0-9][0-9][0-9])\b')
	get_author_query: str = """SELECT author, count(author) FROM work_metadata
							   WHERE filepath LIKE '%gut_texts%'
							   OR filepath LIKE '%lib_texts%'
							   GROUP BY author 
							   ORDER BY count(author) DESC"""

	db_cursor.execute(get_author_query)
	author_list: list = db_cursor.fetchall()

	author_no_result: int = 0

	# Set up a headless Chrome instance to be used when no result is returned
	#	from Wikidata
	chromeopts: Options = Options()
	chromeopts.headless = True
	chromeopts.add_argument('window-size=1920x1080')
	browser: webdriver.Chrome = Chrome(options=chromeopts)

	def run_wiki_query(qauthor: str) -> int:
		print(f'Running query on `{qauthor}`')
		endpoint_url: str = "https://query.wikidata.org/sparql"
		user_agent: str = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])

		query_string: str = """
		SELECT distinct ?item ?itemLabel ?itemDescription (SAMPLE(?DR) as ?DR) (SAMPLE(?RIP) as ?RIP) (SAMPLE(?image)as ?image) (SAMPLE(?article)as ?article) WHERE {
		  ?item wdt:P31 wd:Q5.
		  ?item ?label "%s"@en.  
		  ?article schema:about ?item .
		  ?article schema:inLanguage "en" .
		  ?article schema:isPartOf <https://en.wikipedia.org/>.  
		  OPTIONAL{?item wdt:P569 ?DR .} # P569 : Date of birth
		  OPTIONAL{?item wdt:P570 ?RIP .}     # P570 : Date of death
			
		  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }    
		}
		GROUP BY ?item ?itemLabel ?itemDescription
		"""

		sparql: SPARQLWrapper = SPARQLWrapper(endpoint_url, agent=user_agent)
		sparql.setQuery(query_string % qauthor)
		sparql.setReturnFormat(JSON)

		wiki_search_res: object = sparql.query().convert()

		earliest_date: int = 2100

		for row in wiki_search_res['results']['bindings']:
			try:
				date: object = re_date.match(row['DR']['value'])
			except Exception as e:
				date: object = re_date.match('2100')

			if date:
				int_date: int = int(date[0])

				if int_date < earliest_date:
					earliest_date = int_date

		return earliest_date

	total_removal_candidates: int = 0
	cross_ref_removals: int = 0
	cross_ref_no_results: int = 0

	for result in author_list:
		author: str = result[0]

		# Some names with abbreviations in them are not spaced correctly,
		#	which causes them to not return a result from Wikidata.
		#	This regex will fix that; for example, 'H.G. Wells'
		#	will become 'H. G. Wells'
		author = re.sub(r'\.(?! )', '. ', author)

		# Similarly, some authors have quotes in them, like ones that
		#	have a nickname along with their real name. Attempting
		#	to pass that to SPARQL will throw an exception because of how
		#	our query is formatted, so here we simply escape all " instances
		author = author.replace('"', r'\"')

		orig_author: str = author

		# Skip over 'fake' authors, like 'Various' and such
		if not (author == 'Various' or author == 'Unknown' or author == 'Anonymous' or 'Editor' in author):
			# Check if there is a second name in parentheses, and if so
			#	get the name not in parentheses
			if '(' in author:
				tokens: list = author.split('(')
				author = tokens[0]
				author2 = tokens[1][:-1]

			birth_date: int = run_wiki_query(author.strip())

			if birth_date == 2100:
				author_no_result = author_no_result + 1

				try:
					pub_date_result: list = verify_author_publication_dates(browser, author)
					total_removal_candidates = total_removal_candidates + pub_date_result[1]
					cross_ref_removals = cross_ref_removals + pub_date_result[1]
					cross_ref_no_results = cross_ref_no_results + pub_date_result[0]
				except Exception as e:
					pass				

			elif birth_date > 1755:
				print(f'Author {author} born after 1755, removing {result[1]} texts.')
				total_removal_candidates = total_removal_candidates + result[1]

				db_cursor.execute(f'SELECT id, filepath FROM work_metadata WHERE author LIKE "{orig_author}"')
				texts: list = db_cursor.fetchall()

				for entry in texts:
					db_cursor.execute(f'DELETE FROM work_metadata WHERE id = {entry[0]}')
					db_conn.commit()
					os.remove(f'{base_dir}/{entry[1]}')

	print(f'{total_removal_candidates} texts were removed. Of the {author_no_result} authors that returned no result, {cross_ref_removals} of their texts were removed and {cross_ref_no_results} of their texts could not be found.')

	browser.close()

	# result = return_sparql_query_results(query_string % author)
	# for row in result['results']['bindings']:
	# 	print(row['DR']['value'])

verify_author_birthdates()

db_conn.close()
