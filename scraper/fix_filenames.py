import os
import mysql.connector

# Connect to SQL database
db_conn: mysql.connector.MySQLConnection = mysql.connector.connect(
	user=os.environ.get('DB_USER'),
	password=os.environ.get('DB_PASS'),
	host=os.environ.get('DB_IP'),
	database=os.environ.get('DB_DB'))

db_cursor: mysql.connector.cursor.CursorBase = db_conn.cursor()

file_dirs: list = ['/home/chris/lit_texts/gut_texts', '/home/chris/lit_texts/hat_texts', '/home/chris/lit_texts/lib_texts', '/home/chris/lit_texts/loc_texts']

for fdir in file_dirs:
	print(f'Checking {fdir} against database...')
	# Walk the directory of files
	for path, _, files in os.walk(os.path.abspath(fdir)):
		# Process each file in the directory
		for f in files:
			filepath: str = os.path.join(path, f)

			try:
				db_cursor.execute(f'SELECT * FROM work_metadata WHERE filepath LIKE \'%{f}%\';')
				result: list = db_cursor.fetchall()
			except Exception as err:
				print(f'SELECT * FROM work_metadata WHERE filepath LIKE \'%{f}%\';')
			else:
				if len(result) == 0:
					print(f'File {f} not in database correctly.')

db_conn.close()