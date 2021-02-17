'''main.py

Entry point for the fuzzy search program
'''

__authors__ = ["Jacob Hofstein", "Brent Pappas"]
__contact__ = "pappasbrent@knights.ucf.edu"

import traceback
from contextlib import nullcontext
from typing import List

import begin
import dotenv
from mysql.connector import MySQLConnection, connect
from mysql.connector.cursor import CursorBase
from sshtunnel import (BaseSSHTunnelForwarderError,
                       HandlerSSHTunnelForwarderError, SSHTunnelForwarder)

from util.config import Config, get_config_from_env
from util.custom_types import Metadata, Quote, QuoteMatch
from util.database_ops import (get_metadatum, get_quotes,
                               write_matches_to_database)
from util.string_comp import fuzzy_search_over_corpora


@begin.start(auto_convert=True)
def main(use_ssh_tunnelling=True, corpora_path="./corpora", load_dotenv=True) -> None:
    # TODO: Log errors using the logger module instead
    #       of printing them to the console

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
            print(f"Fetched {len(quotes)} quotes from the database")

            metadatum: List[Metadata] = get_metadatum(cursor)
            print(f"Fetched {len(metadatum)} metadatum from the database")

            for i, quote in enumerate(quotes, 1):
                top_five: List[QuoteMatch] = fuzzy_search_over_corpora(
                    quote, metadatum, corpora_path)
                # write_matches_to_database(top_five, cursor)
                print(
                    f"Wrote top matches for {i}/{len(quotes)} to the database")

            # cursor.commit()
            cursor.close()
            conn.close()

    except (BaseSSHTunnelForwarderError, HandlerSSHTunnelForwarderError) as e:
        print("Unable to connect to the ssh server due to the following error:")
        print(traceback.format_exc())
        print("Please ensure that the correct environment variables are set and that you are connected to the VPN.")
    except Exception:
        print("After successfully opening the ssh tunnel, the following error occurred:")
        print(traceback.format_exc())
