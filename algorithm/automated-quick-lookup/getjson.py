from sshtunnel import SSHTunnelForwarder
import mysql.connector
import json
import re

AUTHOR_LIST = {}

with open("authors.txt", "r") as txtFile:
    Lines = txtFile.readlines()
    for line in Lines:
        AUTHOR_LIST[line.strip("\n")] = re.sub(r"\W+", "", line.lower()) + ".json"

ssh_config = {
    "ssh_address_or_host": ("10.173.204.216", 22),
    "ssh_username": "jhofstein",
    "ssh_password": "masquerade42",
    "remote_bind_address": ("127.0.0.1", 3306)
}

ssh_conn = SSHTunnelForwarder(**ssh_config)

ssh_conn.start()

db_config = {
    "user": "sjd_quotes",
    "password": "SJDquotes2020",
    "host": "127.0.0.1",
    "database": "SJDquotes",
    "port": ssh_conn.local_bind_port
}

db_conn = mysql.connector.connect(**db_config)

if db_conn.is_connected():
    print("Connected to the MySQL database.")

cursor = db_conn.cursor(dictionary=True)

for author in AUTHOR_LIST:
    q = author.replace(".", "")
    q = q.replace(",", "")
    q = q.replace("'s", "")
    q = q.replace("'", "\\'")
    print("current author: " + q)
    cursor.execute("SELECT * FROM work_metadata WHERE author LIKE '%" + q + "%'")
    result = cursor.fetchall()
    d = {"data": result}
    with open(AUTHOR_LIST[author], "w") as jsonFile:
        json.dump(d, jsonFile)

db_conn.close()

ssh_conn.stop()