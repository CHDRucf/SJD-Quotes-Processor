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
from typing import List

import begin
import dotenv
from mysql.connector import MySQLConnection, connect
from sshtunnel import SSHTunnelForwarder

from config import (get_database_connection_options_from_env,
                    get_ssh_connection_options_from_env)
from database_ops import reset_db_quotes
from excel_to_json import QuoteMetadata, write_to_json


@begin.start(auto_convert=True)
def main(quotes_filepath='quotes.json', excel_filepath='FullQuotes.xlsx', excel_to_json=False, json_to_sql=False, delete_quotes=False, write_quotes=False, delete_metadata=False, insert_and_link_metadata=False):
    '''
    Entry point for the program
    TODO: Allow user to specify excel and json filenames from command line
    TODO: Allow user to toggle ssh tunnelling (see algorithm component)
    '''
    dotenv.load_dotenv(".dotenv", override=True)
    quotes_metadatas: List[QuoteMetadata] = None

    if excel_to_json:
        quotes_metadatas = write_to_json(excel_filepath, quotes_filepath)

    if json_to_sql:
        # Only re-read quotes if necessary
        if quotes_metadatas is None:
            with open(quotes_filepath, "r", encoding="utf-8") as fp:
                quotes_metadatas = json.load(fp)
                quotes_metadatas = [QuoteMetadata(
                    **meta) for meta in quotes_metadatas]

        with SSHTunnelForwarder(**get_ssh_connection_options_from_env()) as tunnel:
            conn: MySQLConnection = connect(
                **{**get_database_connection_options_from_env(False), "port": tunnel.local_bind_port}, charset="utf8")

            reset_db_quotes(quotes_metadatas, conn, delete_quotes,
                            write_quotes, delete_metadata, insert_and_link_metadata)

            conn.close()
