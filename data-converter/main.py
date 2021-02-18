'''main.py
Program entry point

TODO:   The code between this component and the algorithm is not DRY,
        e.g., config.py is copied from that component. This is not amenable
        to future changes, so some form of unifying these two components
        should be implemented. Maybe move this a sub-package of the algorithm
        component?
'''

__author__ = "Brent Pappas"
__email__ = "pappasbrent@knights.ucf.edu"

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
    '''
    Entry point for the program
    TODO: Allow user to specify excel and json filenames from command line
    TODO: Allow user to toggle ssh tunnelling (see algorithm component)
    '''
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
                **{**get_database_connection_options_from_env(False), "port": tunnel.local_bind_port}, charset="utf8")

            cursor: cursor.CursorBase = conn.cursor()
            delete_quotes_from_db(cursor)
            write_quotes_to_database(quotes, cursor)

            conn.commit()
            conn.close()
