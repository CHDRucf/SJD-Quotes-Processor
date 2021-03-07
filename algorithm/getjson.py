from sshtunnel import SSHTunnelForwarder
import mysql.connector
import json

AUTHOR_LIST = {
    "Addison": "addison.json",
    "Dryden": "dryden.json"
}

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
    cursor.execute("SELECT * FROM work_metadata WHERE author LIKE '%" + author + "%'")
    result = cursor.fetchall()
    with open(AUTHOR_LIST[author], "w") as f:
        json.dump(result, f)
    

db_conn.close()

ssh_conn.stop()