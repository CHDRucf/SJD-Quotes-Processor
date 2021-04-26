import os
import mysql.connector

# Connect to SQL database
db_conn: mysql.connector.MySQLConnection = mysql.connector.connect(
	user=os.environ.get('DB_USER'),
	password=os.environ.get('DB_PASS'),
	host=os.environ.get('DB_IP'),
	database=os.environ.get('DB_DB'))

db_cursor: mysql.connector.cursor.CursorBase = db_conn.cursor()

# This will check the database for any works whose file paths do not lead anywhere.
def verify_database_filepaths() -> None:
	db_cursor.execute('SELECT id,title,filepath FROM work_metadata')
	res: list = db_cursor.fetchall()

	for r in res:
		if not os.path.exists(f'/home/chris/lit_texts/{r[2]}'):
			print(f'Database entry with id {r[0]} has incorrect filepath {r[2]}')

verify_database_filepaths()

db_conn.close()
