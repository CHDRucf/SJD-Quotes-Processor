'''main.py
Program entry point
'''

import json

import begin
import dotenv
from mysql.connector import MySQLConnection, connect, cursor
from sshtunnel import SSHTunnelForwarder

from config import (get_database_connection_options_from_env,
                    get_ssh_connection_options_from_env)
from database_ops import delete_quotes_from_db, write_quotes_to_database
from excel_to_json import write_to_json


@begin.start(auto_convert=True)
def main(excel_to_json=False, json_to_sql=False):
    '''Entry point for the program'''
    dotenv.load_dotenv(".dotenv", override=True)
    quotes: dict = None

    if excel_to_json:
        quotes = write_to_json("FullQuotes.xlsx", "quotes.json")

    if json_to_sql:
        # Only re-read quotes if not already in quotes variable
        if quotes is None:
            with open("quotes.json", "r", encoding="utf-8") as fp:
                quotes = json.load(fp)

        with SSHTunnelForwarder(**get_ssh_connection_options_from_env()) as tunnel:
            conn: MySQLConnection = connect(
                **{**get_database_connection_options_from_env(False), "port": tunnel.local_bind_port})

            cursor: cursor.CursorBase = conn.cursor()
            delete_quotes_from_db(cursor)
            write_quotes_to_database(quotes, cursor)

            conn.commit()
            conn.close()
