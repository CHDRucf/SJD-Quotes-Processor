import time
import logging
import logging.handlers
import os
import mysql.connector
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from collections import deque
from bs4 import BeautifulSoup

# Create 'logs' and 'gut_texts' directories if they don't already exist
os.makedirs('logs/', exist_ok=True)
os.makedirs('gut_texts/', exist_ok=True)

# Custom logger
logger: logging.RootLogger = logging.getLogger("gutenberg_scraper")
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

def scrape() -> int:
	fileindex: int = 1
	file_dir: str = os.environ.get('GB_FILES')

	if not os.path.isdir(file_dir):
		logger.critical(f'Directory {file_dir} does not exist, please check your .env file.')
		return -1

	if len(os.listdir(file_dir)) == 0:
		logger.critical(f'Directory {file_dir} is empty, is it the correct directory?')
		return -2

	sql_insert_stmt: str = (
		"INSERT INTO metadata(title, author, url, filepath, lccn)"
		"VALUES (%s, %s, %s, %s, %s)" )

	# Walk the directory of files 
	for path, _, files in os.walk(os.path.abspath(file_dir)):
		# Process each file in the directory
		for f in files:
			text_filename: str
			filepath: str = os.path.join(path, f)
			file: file = open(filepath, mode='r', encoding='latin-1')
			full_html: str = file.read()

			file.close()

			soup: BeautifulSoup = BeautifulSoup(full_html, 'lxml')
			fulltext: str = soup.find('body').text
			first2k: str = fulltext[:2000]
			title_author: list = [x.strip() for x in first2k.splitlines() if 'Title:' in x or ('Author:' in x or 'Editor:' in x)]

			# Extract title and author from the text and build the URL
			#	based on the file name
			if len(title_author) != 0:
				# Check if there was an editor listen instead of an author so we can mark it accordingly
				for i, s in enumerate(title_author):
					temp = s.split(':')
					
					if 'Editor' in temp[0]:
						print(s)
						title_author[i] = temp[1].strip() + ' (Editor)'
					else:
						title_author[i] = temp[1].strip()
			else:
				logger.info(f'Title and author of {filepath} could not be determined.')
				title_author = ['UNKNOWN Title', 'UNKNOWN Author']

			filenum: str = "".join([x for x in str(f) if x.isdigit()])
			url: str = f'https://www.gutenberg.org/files/{filenum}/{filenum}-h/{str(f)}'

			# Extract full text to the file system and make a database 
			#	entry with the extracted metadata
			text_filename = f'gut_texts/gut{fileindex}{title_author[0][:5].replace(" ", "_").replace("/", "-")}.txt'
			
			fileindex = fileindex + 1

			fulltext_file: file = open(text_filename, 'w')
			fulltext_filepath: str = text_filename

			fulltext_file.write(fulltext)

			print(f'File {fulltext_file.name} written.')

			fulltext_file.close()

			try:
				data: tuple = (title_author[0][:255], title_author[1][:255], url, fulltext_filepath, '-1')
				db_cursor.execute(sql_insert_stmt, data)
				db_conn.commit()
			except Exception as err:
				db_conn.rollback()
				print(f"Problem file: {filepath}")
				logger.warning("Error occurred when writing to database", exc_info=True)

	return 0

scrape()

db_conn.close()
