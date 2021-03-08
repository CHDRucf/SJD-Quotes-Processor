import re
import os
import logging
import logging.handlers
from datetime import datetime

re_date: object = re.compile('1([0-9][0-9][0-9])')

# Get the directory to search from the user
file_dir: str = input("Enter the directory to search: ")
print_to_terminal: str = input("Output matches to terminal? (y/n)")

in_range_count: int = 0
match_count: int = 0

os.makedirs('logs/', exist_ok=True)

# Custom logger
logger: logging.RootLogger = logging.getLogger("date_match")
logger.setLevel(logging.INFO)

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
	print_handler.setLevel(logging.INFO)
else:
	print_handler.setLevel(logging.WARNING)

# Roll over file name if a log already exists
if rollover:
	file_handler.doRollover()

file_handler.setLevel(logging.INFO)

# Formatter for logger output
log_format: logging.Formatter = logging.Formatter('%(asctime)s\t: %(name)s : %(levelname)s -- %(message)s', '%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(log_format)
print_handler.setFormatter(log_format)

# Add to logger
logger.addHandler(file_handler)
logger.addHandler(print_handler)

# Walk the directory of files
for path, _, files in os.walk(os.path.abspath(file_dir)):
	# Process each file in the directory
	for f in files:
		filepath: str = os.path.join(path, f)

		with open(filepath, mode='r', encoding='utf8') as file:
			# Read the file line by line, checking for a string match.
			#	If a match is found, print the line it was found on
			#	and the file path
			for index, line in enumerate(file):
				match: object = re_date.search(line)

				# Found a match -> print the line & file then end loop
				if match:
					match_count = match_count + 1
					date: int = int(match[0])

					logger.info(f'Match {match[0]} found in {filepath} on line {index}:\n\t{line}')

					if date <= 1755:
						in_range_count = in_range_count + 1

					break
				
print(f'Found {in_range_count} files containing a match within the desired range.')
print(f'{match_count} contained a match in general.')
print(f'Matches can be found in {logfilename}')
