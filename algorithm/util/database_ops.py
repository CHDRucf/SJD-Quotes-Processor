'''datbase_ops.py

Functions that interact with the database
'''

from typing import Iterable, List

from mysql.connector.cursor import CursorBase

from util.custom_types import Metadata, Quote, QuoteMatch


def write_matches_to_database(matches: Iterable[QuoteMatch], cursor: CursorBase) -> None:
    '''
    Args:
        matches:    An iterable of quote matches to write to the database
        conn:       The MySQLConnection object representing a connection to the
                    database
    '''
    sql_insert_statement = (
        "INSERT INTO `matches`(`quote_id`, `metadata_id`, `rank`, `score`, `content`) "
        "VALUES (%s, %s, %s, %s, %s);"
    )
    cursor.executemany(sql_insert_statement, matches)


def get_metadatum(cursor: CursorBase) -> Metadata:
    '''
    Gets all the metadatum from the MySQL database
    TODO: Add filters to only search over specific metadatum

    Args:
        cursor: The database cursor for performing the metadata query

    Returns:    A list of the Metadata objects representing the metadatum found
    '''
    sql_query: str = (
        "SELECT id, title, author, url, filepath, lccn "
        "FROM metadata;")
    cursor.execute(sql_query)
    return [Metadata(*row) for row in cursor.fetchall()]


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
