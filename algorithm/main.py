'''main.py

Entry point for the fuzzy search program
'''

__authors__ = ["Jacob Hofstein", "Brent Pappas"]
__contact__ = "pappasbrent@knights.ucf.edu"

from typing import List

from contextlib import nullcontext
import begin
import dotenv
from sshtunnel import SSHTunnelForwarder
from mysql.connector import MySQLConnection, connect
from mysql.connector.cursor import CursorBase

from util.config import Config, get_config_from_env
from util.custom_types import Quote, QuoteMatch
from util.database_ops import get_quotes, write_to_matches_to_database
from util.misc import get_filepaths
from util.string_comp import fuzzy_search_over_corpora


@begin.start(auto_convert=True)
def main(use_ssh_tunnelling=True, corpora_path="./corpora", load_dotenv=True) -> None:
    # TODO: Log errors using the logger module instead
    #       of printing them to the console

    if load_dotenv:
        dotenv.load_dotenv(override=True)

    config: Config = get_config_from_env()

    try:
        ssh_context_manager = SSHTunnelForwarder(
            **config.ssh_connection_options) if use_ssh_tunnelling else nullcontext()

        with ssh_context_manager as tunnel:
            if use_ssh_tunnelling:
                config.my_sql_connection_options["port"] = tunnel.local_bind_port

            conn: MySQLConnection = connect(
                **config.my_sql_connection_options)
            cursor: CursorBase = conn.cursor()

            # quotes: List[Quote] = get_quotes(cursor)
            # print(f"Fetched {len(quotes)} quotes from the database")

            # filepaths: List[str] = get_filepaths(corpora_path)
            # print(f"Fetched {len(filepaths)} filepaths from {corpora_path}")

            # for i, quote in enumerate(quotes, 1):
            #     top_five: List[QuoteMatch] = fuzzy_search_over_corpora(
            #         quote.get("quote"), filepaths, cursor)
            #     write_to_matches_to_database(top_five, cursor)
            #     print(
            #         f"Wrote top matches for {i}/{len(quotes)} to the database")

            cursor.commit()
            cursor.close()
            conn.close()

    except Exception as e:
        print("Unable to connect to the database due to the following error:")
        print(e)
        print("Please ensure that the correct environment variables are set and that you are connected to the VPN")
