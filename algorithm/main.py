'''main.py

Entry point for the fuzzy search program

'''

__authors__ = ["Jacob Hofstein", "Brent Pappas"]
__contact__ = "pappasbrent@knights.ucf.edu"

import json
from typing import Dict, List, Union

import dotenv
import sshtunnel
from mysql.connector import MySQLConnection, connect
from mysql.connector.cursor import CursorBase

from util.config import (get_database_connection_options_from_env,
                         get_ssh_connection_options_from_env)
from util.custom_types import *
from util.database_ops import write_to_database
from util.misc import flatten_quotes, get_file_paths
from util.string_comp import fuzzy_search_over_corpora


def main() -> None:
    # TODO: Turn these constants into command line args using begins package
    # TODO: Log errors using the logger module instead
    #       of printing them to the console
    # TODO: Try to make this main function smaller
    # TODO: Add a config so that dotenv only loads in development, not in
    #       final product
    JSON_FILEPATH = "./quotes.json"
    CORPORA_PATH = "."

    dotenv.load_dotenv()

    try:
        ssh_connection_options: Dict[str, Union[str, int]
                                     ] = get_ssh_connection_options_from_env()
    except EnvironmentError as e:
        print(e)
        return

    try:
        database_connection_options: Dict[str,
                                          str] = get_database_connection_options_from_env()
    except EnvironmentError as e:
        print(e)
        return

    conn: MySQLConnection
    cursor: CursorBase
    try:
        with sshtunnel.SSHTunnelForwarder(**ssh_connection_options) as tunnel:
            conn = connect(**database_connection_options,
                           port=tunnel.local_bind_port)
            cursor = conn.cursor()

        # Refer to convert-excel-to-json module for quote object schema
        headword_quotes: HeadwordQuotesDict
        try:
            with open(JSON_FILEPATH, "r") as fp:
                headword_quotes = json.load(fp)
        except FileNotFoundError as fnfe:
            print(fnfe)
            return

        # Get the list of quote objects, with the headword added to each object
        quotes: FlattenedQuotesDict = flatten_quotes(headword_quotes)

        # Convert to list to avoid exhausting iterator
        file_paths: List[str] = list(get_file_paths(CORPORA_PATH))

        # TODO: Consider storing quotes and top five metadatum in a list
        # before writing to database. This would allow for parallel processing
        # using a multiprocessing.Pool object

        for quote in quotes:
            top_five: MatchToMetadataDict = fuzzy_search_over_corpora(
                quote.get("quote"), file_paths, cursor)
            write_to_database(quote, top_five, cursor)

        cursor.close()
        conn.close()

    except Exception as e:
        print("Unable to connect to the database due to the following error:")
        print(e)
        print("Please ensure that the correct environment variables are set and that you are connected to the VPN")
        return
