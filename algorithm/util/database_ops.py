'''datbase_ops.py

Functions that interact with the database
'''

from typing import Iterable, List

from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import CursorBase

from util.custom_types import Metadata, Quote, QuoteMatch


def write_to_matches_to_database(matches: Iterable[QuoteMatch], cursor: CursorBase) -> None:
    '''
    Args:
        matches:    An iterable of quote matches to write to the database
        conn:       The MySQLConnection object representing a connection to the
                    database
    '''
    sql_insert_statement = (
        "INSERT INTO matches(quote_id, metadata_id, rank, score, content)"
        "VALUES (%s, %s, %s, %s, %s);"
    )
    cursor.executemany(sql_insert_statement, matches)


def get_file_metadata(file_name: str, cursor: CursorBase) -> Metadata:
    '''
    Returns a dict containing the metadata for a written work with
    the given file name

    Args:
        file_name:  The name of the file to obtain the metadata for
        cursor:     The database cursor for performing the metadata query
    # TODO: Test

    Returns:    A Metadata object representing the metadata found
    '''
    sql_query: str = (
        "SELECT id, title, author, url, filepath, lccn "
        "FROM METADATA "
        "WHERE filepath = %s;")
    cursor.execute(sql_query, (file_name,))
    return Metadata(cursor.fetchone())


def get_quotes(cursor: CursorBase) -> List[Quote]:
    '''
    Gets all the quotes from the MySQL database
    TODO: Add filters to only obtain specific quotes

    Args:
        cursor: The database cursor for performing the quote query

    Returns:    A list of Quote objects representing the quotes found
    '''
    select_quotes_sql = (
        "SELECT id, headword, quote, title, author "
        "FROM quotes;"
    )
    cursor.execute(select_quotes_sql)
    return [Quote(*row) for row in cursor.fetchall()]
