'''main.py

Entry point for the fuzzy search program
'''

__authors__ = ["Jacob Hofstein", "Brent Pappas"]
__contact__ = "pappasbrent@knights.ucf.edu"

import json
import logging
import traceback
from contextlib import nullcontext
from multiprocessing import cpu_count
from typing import List

import begin
import dotenv
from mysql.connector import MySQLConnection, connect
from mysql.connector.cursor import CursorBase
from sshtunnel import (BaseSSHTunnelForwarderError,
                       HandlerSSHTunnelForwarderError, SSHTunnelForwarder)

from fuzzy_search import fuzzy_search_multiprocessed
from util.config import Config, get_config_from_env
from util.custom_types import Quote, QuoteMatch, WorkMetadata
from util.database_ops import (get_quotes, get_works_metadata,
                               write_match_to_database)

CHUNK_SIZE = 6

logging.basicConfig(level=logging.INFO)


@begin.start(auto_convert=True)
def main(use_ssh_tunnelling=True, corpora_path="./corpora",
         load_dotenv=True, perform_search=True,
         use_multiprocessing=True, num_processes=cpu_count(),
         write_to_json=True, write_to_database=False,
         json_path='matches.json',
         start_quote_id=1, end_quote_id=None) -> None:

    if start_quote_id <= 0:
        logging.error(f"Starting quote id of {start_quote_id} is invalid.\n"
                      "Please enter a value >= 1")
        return

    if end_quote_id is not None:
        end_quote_id = int(end_quote_id)

    if end_quote_id is not None and end_quote_id <= 0:
        logging.error(f"Ending quote id of {end_quote_id} is invalid.\n"
                      "Please enter a value >= 1")
        return

    if load_dotenv:
        dotenv.load_dotenv(override=True)

    config: Config = get_config_from_env(use_ssh_tunnelling)

    try:
        ssh_context_manager = SSHTunnelForwarder(
            **config.ssh_connection_options) if use_ssh_tunnelling else nullcontext()

        with ssh_context_manager as tunnel:
            # Set the database port if using SSH tunnelling
            if use_ssh_tunnelling:
                config.my_sql_connection_options["port"] = tunnel.local_bind_port

            conn: MySQLConnection = connect(
                **config.my_sql_connection_options, charset="utf8")
            cursor: CursorBase = conn.cursor()
            logging.info("Connected to database %s",
                         config.my_sql_connection_options.get("database"))

            quotes: List[Quote] = get_quotes(
                cursor, start_quote_id, end_quote_id)
            logging.info("%s quotes obtained from the database", len(quotes))
            work_metadatas: List[WorkMetadata] = get_works_metadata(cursor)
            logging.info(
                "Metadata for %s works obtained from the database", len(work_metadatas))

            # Get the matches, either by searching for them or
            # by reading them from a JSON file
            matches: List[QuoteMatch]
            if perform_search:
                if use_multiprocessing:
                    matches = fuzzy_search_multiprocessed(
                        quotes, work_metadatas, corpora_path, num_processes, CHUNK_SIZE)
                else:
                    matches = fuzzy_search_multiprocessed(
                        quotes, work_metadatas, corpora_path, 1, len(quotes))
            else:
                with open(json_path, 'r', encoding='utf-8') as fp:
                    matches = [QuoteMatch(**match_)
                               for match_ in json.load(fp)]

            if write_to_json:
                with open(json_path, 'w', encoding='utf-8') as fp:
                    json.dump([match_._asdict() for match_ in matches], fp)

            if write_to_database:
                ...
                ''' for match_ in matches:
                        write_match_to_database(match_, cursor)'''

            # cursor.commit()
            cursor.close()
            conn.close()

    except (BaseSSHTunnelForwarderError, HandlerSSHTunnelForwarderError):
        logging.error(traceback.format_exc())
        logging.error(
            "SSH connection error; please ensure that the correct environment "
            "variables are set and that you are connected to the VPN.")
    except Exception:
        logging.error(traceback.format_exc())
        logging.error("The above error occurred after opening the SSH tunnel")
