import time
import logging
import logging.handlers
import os
import mysql.connector
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from collections import deque
from bs4 import BeautifulSoup

# Create 'logs' directory if it doesn't already exist
os.makedirs('logs/', exist_ok=True)

# Custom logger
logger: object = logging.getLogger("gutenberg_scraper")
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

# Load the environment variables
load_dotenv(find_dotenv())

# Connect to SQL database
db_conn: object = mysql.connector.connect(
	user=os.environ.get('DB_USER'),
	password=os.environ.get('DB_PASS'),
	host=os.environ.get('DB_IP'),
	database=os.environ.get('DB_DB'))

db_cursor: object = db_conn.cursor()

def scrape() -> int:
	fileindex: int = 1

	sql_insert_stmt: str = (
		"INSERT INTO Metadata(title, author, url, filepath, lccn)"
		"VALUES (%s, %s, %s, %s, %s)" )

	# Walk the directory of files 
	for path, _, files in os.walk(os.path.abspath(os.environ.get('GB_FILES'))):
		# Process each file in the directory
		for f in files:
			text_filename: str
			filepath: str = os.path.join(path, f)
			file: object = open(filepath, mode='r', encoding='latin-1')
			full_html: str = file.read()

			file.close()

			soup: object = BeautifulSoup(full_html, 'lxml')

			# Extract title and author from the text and build the URL
			#	based on the file name
			pre: str = soup.find('pre').text
			title_author: list = [x.split(':')[1].strip() for x in pre.splitlines() if 'Title:' in x or 'Author:' in x]
			filenum: str = "".join([x for x in str(f) if x.isdigit()])
			url: str = f'https://www.gutenberg.org/files/{filenum}/{filenum}-h/{str(f)}'

			# Extract full text to the file system and make a database 
			#	entry with the extracted metadata
			fulltext: str = soup.find('body').text
			text_filename = f'gut{fileindex}{title_author[0][:5].replace(" ", "_")}.txt'
			
			fileindex = fileindex + 1

			fulltext_file: object = open(text_filename, 'w')
			fulltext_filepath: str = os.path.realpath(fulltext_file.name)

			fulltext_file.write(fulltext)

			print(f'File {fulltext_file.name} written.')

			fulltext_file.close()

			try:
				data: tuple = (title_author[0], title_author[1], url, fulltext_filepath, '-1')
				db_cursor.execute(sql_insert_stmt, data)
				db_conn.commit()
			except Exception as err:
				db_conn.rollback()
				logger.warning("Error occurred when writing to databse", exc_info=True)

scrape()

db_conn.close()