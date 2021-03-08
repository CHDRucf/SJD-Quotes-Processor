'''main.py

Entry point for the fuzzy search program
'''

__authors__ = ["Jacob Hofstein", "Brent Pappas"]
__contact__ = "pappasbrent@knights.ucf.edu"

import json
import logging
import traceback
from collections import deque
from contextlib import nullcontext
from multiprocessing import cpu_count
from typing import Deque, Dict, Iterable, List, Tuple

import begin
import dotenv
from mysql.connector import MySQLConnection, connect
from mysql.connector.cursor import CursorBase
from sshtunnel import (BaseSSHTunnelForwarderError,
                       HandlerSSHTunnelForwarderError, SSHTunnelForwarder)

import constants
from fuzzy_search import fuzzy_search_multiprocessed
from util.config import Config, get_config_from_env
from util.custom_types import Quote, QuoteMatch, WorkMetadata
from util.database_ops import (get_non_quick_lookup_quotes,
                               get_quotes_by_author, get_works_metadata,
                               write_match_to_database,
                               write_quote_id_to_failed_quick_lookup)
from util.misc import get_quick_lookup_works_for_author

QUICK_LOOKUP_THRESHOLD = 53

logging.basicConfig(level=logging.INFO)


# TODO: Add flag for specifying which quick lookup to perform
@begin.start(auto_convert=True)
def main(search_quick_lookup=True, quick_lookup_json_dir="./automated-quick-lookup/metadata",
         use_ssh_tunnelling=True, corpora_path="./corpora",
         load_dotenv=True, perform_search=True,
         use_multiprocessing=True, num_processes=cpu_count(),
         write_to_json=True, write_to_database=False,
         json_path='./matches.json', chunk_size=cpu_count(),
         quick_lookup_number=-1) -> None:

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
            failed_quick_lookup_quote_ids: Deque[int] = deque()
            # Get the matches, either by searching for them or
            # by reading them from a JSON file
            if perform_search:
                if search_quick_lookup:
                    # Get all quotes up front so that a persistent
                    # database connection is not required
                    quick_lookup_dict: Dict[str, str]
                    if quick_lookup_number == 1:
                        quick_lookup_dict = constants.QUICK_LOOKUP_AUTHORS_AND_WORKS
                    elif quick_lookup_number == 2:
                        quick_lookup_dict = constants.SECOND_ROUND_QUICK_LOOKUP
                    # elif quick_lookup_number == 3:
                    #     quick_lookup_dict = constants.THIRD_ROUND_QUICK_LOOKUP
                    else:
                        logging.error(
                            f"Invalid quick lookup number specified: {quick_lookup_number}")
                        return
                    authors_quotes_works: List[Tuple[str, List[Quote], List[WorkMetadata]]] = [
                        (
                            author,
                            get_quotes_by_author(cursor, author),
                            get_quick_lookup_works_for_author(
                                quick_lookup_json_dir, works_list_json_fp)
                        ) for author, works_list_json_fp
                        in quick_lookup_dict.items()
                    ]
                    # Close connection until needed again later
                    cursor.close()
                    conn.close()

                    matches = deque()
                    for i, (author, quotes, work_metadatas) in enumerate(authors_quotes_works, 1):
                        author_matches: List[QuoteMatch]

                        if use_multiprocessing:
                            author_matches = fuzzy_search_multiprocessed(
                                quotes, work_metadatas, corpora_path, num_processes, chunk_size)
                        else:
                            author_matches = fuzzy_search_multiprocessed(
                                quotes, work_metadatas, corpora_path, 1, len(quotes))

                        # Need to check if any of the matches for each quote
                        # passed the threshold, and mark the ones without any
                        # passing matches as failed
                        quote_id_to_passing_status: Dict[int, False] = {
                            q.id: False for q in quotes
                        }
                        for m in author_matches:
                            # If at least one of the matches passes the
                            # threshold, then the quote passes
                            passing: bool = quote_id_to_passing_status[m.quote_id]
                            quote_id_to_passing_status[m.quote_id] = passing or m.score >= QUICK_LOOKUP_THRESHOLD

                        # Add quote ids of quotes that failed the quick lookup
                        # to the failed quotes deque
                        failed_quick_lookup_quote_ids.extend([
                            q_id for q_id, passing
                            in quote_id_to_passing_status.items()
                            if not passing
                        ])

                        # Only add passing matches to the matches table
                        matches.extend([
                            match_ for match_
                            in author_matches
                            if quote_id_to_passing_status[match_.quote_id] == True]
                        )
                        logging.info(
                            "Finished quick lookup for %s / %s authors (%s)", i, len(constants.QUICK_LOOKUP_AUTHORS_AND_WORKS), author)
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

            if write_to_json:
                with open(json_path, 'w', encoding='utf-8') as fp:
                    json.dump([match_._asdict()
                               for match_ in matches], fp, ensure_ascii=False)

            # Write failed quote ids to the lookup table
            # TODO: Currently, this will be executed even if the user
            # opted to write the matches to JSON instead of SQL.
            # Should this be changed?
            conn = connect(**config.my_sql_connection_options, charset="utf8")
            cursor = conn.cursor()
            logging.info("Connected to database %s",
                         config.my_sql_connection_options.get("database"))

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
