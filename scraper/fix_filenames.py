import os
import mysql.connector
import re

# Connect to SQL database
db_conn: mysql.connector.MySQLConnection = mysql.connector.connect(
	user=os.environ.get('DB_USER'),
	password=os.environ.get('DB_PASS'),
	host=os.environ.get('DB_IP'),
	database=os.environ.get('DB_DB'))

db_cursor: mysql.connector.cursor.CursorBase = db_conn.cursor()

file_dirs: list = ['gut_texts', 'hat_texts', 'lib_texts', 'loc_texts']

def remove_nonalpha() -> None:
	for fdir in file_dirs:
		print(f'Checking {fdir} for file names containing quotes...')

		for path, _, files in os.walk(os.path.abspath(f'/home/chris/lit_texts/{fdir}')):
			for f in files:
				filepath: str = os.path.join(path, f)

				new_filename: str = re.sub('[^a-zA-Z0-9]+', '-', f[:len(f) - 4]) + '.txt'

				# Only update the database if the new file name is different
				if f != new_filename:
					pref_and_index: str = f[:len(f) - 9]
					new_filepath: str = os.path.join(path, new_filename)

					db_cursor.execute(f'SELECT id FROM work_metadata WHERE filepath LIKE "%{pref_and_index}%";')
					id = db_cursor.fetchall()[0][0]

					print(f'Renaming {f} to {new_filename} and updating database entry with id {id}.')
					
					db_cursor.execute(f'UPDATE work_metadata SET filepath = "{fdir}/{new_filename}" WHERE id = {id}')
					db_conn.commit()
					os.rename(filepath, new_filepath)

def verify_database() -> None:
	for fdir in file_dirs:
		print(f'Checking {fdir} against database...')
		# Walk the directory of files
		for path, _, files in os.walk(os.path.abspath(f'/home/chris/lit_texts/{fdir}')):
			# Process each file in the directory
			for f in files:
				filepath: str = os.path.join(path, f)

				try:
					db_cursor.execute(f'SELECT * FROM work_metadata WHERE filepath LIKE "%{f}%";')
					result: list = db_cursor.fetchall()
				except Exception as err:
					print(f'SELECT * FROM work_metadata WHERE filepath LIKE "%{f}%";')
				else:
					if len(result) == 0:
						print(f'File {f} not in database correctly.')

def verify_file_matches_title() -> None:
	db_cursor.execute('SELECT id,title,filepath FROM work_metadata')
	res: tuple = db_cursor.fetchall()

	for r in res:
		if len(r[1]) < 5:
			correct_title_sub: str = re.sub('[^a-zA-Z0-9]+', '-', r[1])
		else:
			correct_title_sub: str = re.sub('[^a-zA-Z0-9]+', '-', r[1][:5])

		cur_title_sub: str = r[2][len(r[2]) - 9 : len(r[2]) - 4]

		if correct_title_sub != cur_title_sub:
			print(f'Entry with id {r[0]} leads to incorrect file. Current suffix: {cur_title_sub} Correct suffix: {correct_title_sub}')

verify_file_matches_title()

db_conn.close()
