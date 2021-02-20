'''main.py

Entry point for the fuzzy search program
'''

__authors__ = ["Jacob Hofstein", "Brent Pappas"]
__contact__ = "pappasbrent@knights.ucf.edu"

import traceback
from contextlib import nullcontext
from itertools import repeat
from multiprocessing import Pool
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


@begin.start(auto_convert=True)
def main(use_ssh_tunnelling=True, corpora_path="./corpora", load_dotenv=True) -> None:
    # TODO: Log errors using the logger module instead
    #       of printing them to the console
    # TODO: Add command line argument to enable/disable multiprocessing,
    #       configure the number of cores to use, and the chunk size

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

            quotes: List[Quote] = get_quotes(cursor)

            work_metadatas: List[WorkMetadata] = get_works_metadata(cursor)

            quote_chunks: Iterator[List[Quote]] = chunks(quotes, CHUNK_SIZE)

            print("Records obtained from the database, starting search now...")
            i = 0
            with Pool() as pool:
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
                    print(
                        f"Wrote top matches for {i} / {len(quotes)} "
                        "quotes to the database")

            # cursor.commit()
            cursor.close()
            conn.close()

    except (BaseSSHTunnelForwarderError, HandlerSSHTunnelForwarderError):
        print("Unable to connect to the ssh server due to the following error:")
        print(traceback.format_exc())
        print("Please ensure that the correct environment variables are set and that you are connected to the VPN.")
    except Exception:
        print("After successfully opening the ssh tunnel, the following error occurred:")
        print(traceback.format_exc())
