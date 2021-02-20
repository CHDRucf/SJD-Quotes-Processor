'''main.py

Entry point for the fuzzy search program
'''

__authors__ = ["Jacob Hofstein", "Brent Pappas"]
__contact__ = "pappasbrent@knights.ucf.edu"

import logging
import traceback
from contextlib import nullcontext
from itertools import repeat
from multiprocessing import Pool, cpu_count
from typing import Iterator, List

import begin
import dotenv
from mysql.connector import MySQLConnection, connect
from mysql.connector.cursor import CursorBase
from sshtunnel import (BaseSSHTunnelForwarderError,
                       HandlerSSHTunnelForwarderError, SSHTunnelForwarder)

from util.config import Config, get_config_from_env
from util.custom_types import Quote, QuoteMatch, WorkMetadata
from util.database_ops import (get_quotes, get_works_metadata,
                               write_matches_to_database)
from util.misc import chunks
from util.string_comp import fuzzy_search_over_corpora

CHUNK_SIZE = 6

logging.basicConfig(level=logging.INFO)


@begin.start(auto_convert=True)
def main(use_ssh_tunnelling=True, corpora_path="./corpora", load_dotenv=True, num_processes=cpu_count()) -> None:
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

            quotes: List[Quote] = get_quotes(cursor)
            logging.info("%s quotes obtained from the database", len(quotes))
            work_metadatas: List[WorkMetadata] = get_works_metadata(cursor)
            logging.info(
                "Metadata for %s works obtained from the database", len(work_metadatas))

            quote_chunks: Iterator[List[Quote]] = chunks(quotes, CHUNK_SIZE)
            i = 0
            with Pool(num_processes) as pool:
                for quote_chunk in quote_chunks:
                    # TODO: If a work cannot be found, log an error message
                    # and skip it instead of crashing
                    top_fives: List[QuoteMatch] = pool.starmap(
                        fuzzy_search_over_corpora, zip(
                            quote_chunk,
                            repeat(work_metadatas),
                            repeat(corpora_path))
                    )

                    ''' for top_five in top_fives:
                        # write_matches_to_database(top_five, cursor'''
                    i += len(quote_chunk)
                    logging.info(
                        f"Wrote top matches for {i} / {len(quotes)} "
                        "quotes to the database")

            # cursor.commit()
            cursor.close()
            conn.close()

    except (BaseSSHTunnelForwarderError, HandlerSSHTunnelForwarderError):
        logging.error(
            "Unable to connect to the ssh server due to the following error:")
        logging.error(traceback.format_exc())
        logging.error(
            "Please ensure that the correct environment variables are set "
            "and that you are connected to the VPN.")
    except Exception:
        logging.error(
            "The following error occurred after opening the SSH tunnel:")
        logging.error(traceback.format_exc())
