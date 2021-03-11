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
from typing import Deque, Iterable, List

import begin
import dotenv
from mysql.connector import MySQLConnection, connect
from mysql.connector.cursor import CursorBase
from sshtunnel import (BaseSSHTunnelForwarderError,
                       HandlerSSHTunnelForwarderError, SSHTunnelForwarder)

from fuzzy_search import (fuzzy_search_auto_quick_lookup,
                          fuzzy_search_multiprocessed,
                          fuzzy_search_quick_lookup)
from util.config import Config, get_config_from_env
from util.custom_types import (AuthorsQuotesWorks, Quote, QuoteMatch,
                               WorkMetadata)
from util.database_ops import (get_author_quotes_works_auto_quick_lookup,
                               get_author_quotes_works_manual_quick_lookup,
                               get_non_quick_lookup_quotes, get_works_metadata,
                               write_match_to_database,
                               write_quote_id_to_failed_quick_lookup)

QUICK_LOOKUP_THRESHOLD = 53

logging.basicConfig(level=logging.INFO)


@begin.start(auto_convert=True)
def main(search_quick_lookup=True, quick_lookup_json_dir="./automated-quick-lookup/metadata",
         use_ssh_tunnelling=True, corpora_path="./corpora",
         load_dotenv=True, perform_search=True,
         use_multiprocessing=True, num_processes=cpu_count(),
         write_to_json=True, write_to_database=False,
         json_path='./matches.json', chunk_size=cpu_count(),
         quick_lookup_number=-1, manual_quick_lookup=True) -> None:

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

            quotes: List[Quote]
            work_metadatas: List[WorkMetadata]
            matches: Iterable[QuoteMatch]
            failed_quick_lookup_quote_ids: Deque[int] = None
            # Get the matches, either by searching for them or
            # by reading them from a JSON file
            if perform_search:
                if search_quick_lookup:
                    # Search for quick lookup quotes
                    if manual_quick_lookup:
                        authors_quotes_works: AuthorsQuotesWorks = get_author_quotes_works_manual_quick_lookup(
                            cursor, quick_lookup_number, quick_lookup_json_dir)
                        logging.info(
                            "Got quotes and works for %s authors from the database", len(authors_quotes_works))

                        # Close connection until needed again later
                        cursor.close()
                        conn.close()

                        if use_multiprocessing:
                            matches, failed_quick_lookup_quote_ids = fuzzy_search_quick_lookup(
                                authors_quotes_works, corpora_path,
                                num_processes, chunk_size, QUICK_LOOKUP_THRESHOLD)
                        else:
                            matches, failed_quick_lookup_quote_ids = fuzzy_search_quick_lookup(
                                authors_quotes_works, corpora_path,
                                1, 1, QUICK_LOOKUP_THRESHOLD)
                    else:
                        authors_quotes_works: AuthorsQuotesWorks = get_author_quotes_works_auto_quick_lookup(
                            cursor)
                        logging.info("Got quotes and works for %s authors from the database", len(
                            authors_quotes_works))

                        # Close connection until needed again later
                        cursor.close()
                        conn.close()

                        if use_multiprocessing:
                            matches, failed_quick_lookup_quote_ids = fuzzy_search_auto_quick_lookup(
                                authors_quotes_works, corpora_path,
                                num_processes, chunk_size, QUICK_LOOKUP_THRESHOLD)
                        else:
                            matches, failed_quick_lookup_quote_ids = fuzzy_search_auto_quick_lookup(
                                authors_quotes_works, corpora_path,
                                1, 1, QUICK_LOOKUP_THRESHOLD)

                else:
                    # Search for quotes that either failed the quick lookup or
                    # cannot be searched via quick lookup
                    quotes = get_non_quick_lookup_quotes(cursor)
                    logging.info(
                        "%s quotes obtained from the database", len(quotes))
                    work_metadatas = get_works_metadata(cursor)
                    logging.info(
                        "Metadata for %s works obtained from the database", len(work_metadatas))

                    # Close connection until needed again later
                    cursor.close()
                    conn.close()

                    if use_multiprocessing:
                        matches = fuzzy_search_multiprocessed(
                            quotes, work_metadatas, corpora_path, num_processes, chunk_size)
                    else:
                        matches = fuzzy_search_multiprocessed(
                            quotes, work_metadatas, corpora_path, 1, len(quotes))
            else:
                # If we are not searching, then assume that we are
                # reading the matches from JSON
                with open(json_path, 'r', encoding='utf-8') as fp:
                    matches = [QuoteMatch(**match_)
                               for match_ in json.load(fp)]

                # Close connection until needed again later
                cursor.close()
                conn.close()

            if write_to_json:
                with open(json_path, 'w', encoding='utf-8') as fp:
                    json.dump([match_._asdict()
                               for match_ in matches], fp, ensure_ascii=False)

            # At this pont conn and cursor should be closed, so open them again
            conn = connect(
                **config.my_sql_connection_options, charset="utf8")
            cursor = conn.cursor()

            # Write failed quote ids to the lookup table. This will only happen
            # if the quick search was performed
            # NOTE: Currently, this will be executed even if the user
            # opted to write the matches to JSON instead of SQL.
            # Should this be changed?
            if failed_quick_lookup_quote_ids is not None:
                for i, q_id in enumerate(failed_quick_lookup_quote_ids, 1):
                    write_quote_id_to_failed_quick_lookup(cursor, q_id)
                    logging.info(
                        "Wrote %s / %s failed quick searches to the database", i, len(failed_quick_lookup_quote_ids))
                conn.commit()

            if write_to_database:
                for i, match_ in enumerate(matches, 1):
                    write_match_to_database(cursor, match_)
                    logging.info(
                        "Wrote %s / %s matches to the database", i, len(matches))
            conn.commit()

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
