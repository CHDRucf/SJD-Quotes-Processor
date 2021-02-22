import re
import os

re_date: object = re.compile('1([0-9][0-9][0-9])')
file_dir: str = '/home/cmelton/gut_texts/'

#print(re_date.search('The Project Gutenberg EBook of The History of Currency, 1252 to 1896, by'))

in_range_count: int = 0
match_count: int = 0

# Walk the directory of files
for path, _, files in os.walk(os.path.abspath(file_dir)):
	# Process each file in the directory
	for f in files:
		filepath: str = os.path.join(path, f)

		with open(filepath, mode='r', encoding='utf8') as file:
			count: int = 0

			# Read the file line by line, checking for a string match.
			#	If a match is found, print the line it was found on
			#	and the file path
			while True:
				count = count + 1

				line = file.readline()
				match: object = re_date.search(line)

				# Found a match -> print the line & file then end loop
				if match:
					match_count = match_count + 1
					#print(f'Match {match[0]} found in {filepath} on line {count}:\n\t{line}')
					date: int = int(match[0])

					if date <= 1755:
						in_range_count = in_range_count + 1

					break
				
				# Reached the end of the file without finding a match -> end loop
				if not line:
					break

print(f'Found {in_range_count} files containing a match within the desired range.')
print(f'{match_count} contained a match in general.')
