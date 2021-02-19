'''datbase_ops.py

Functions that interact with the database
'''

from typing import List

from mysql.connector.cursor import CursorBase

from util.custom_types import Quote, QuoteMatch, WorkMetadata


def write_matches_to_database(matches: List[QuoteMatch], cursor: CursorBase) -> None:
    '''
    Args:
        matches:    An list of quote matches to write to the database
        conn:       The MySQLConnection object representing a connection to the
                    database
    '''
    sql_insert_statement = (
        "INSERT INTO `matches`(`quote_id`, `work_metadata_id`, `rank`, `score`, `content`) "
        "VALUES (%s, %s, %s, %s, %s);"
    )
    cursor.executemany(sql_insert_statement, matches)


def get_works_metadata(cursor: CursorBase) -> List[WorkMetadata]:
    '''
    Gets all the metadata for all the works from the MySQL database
    TODO: Add filters to only search over specific metadata

    Args:
        cursor: The database cursor for performing the metadata query

    Returns:    A list of the Metadata objects representing the metadata found
    '''
    sql_query: str = (
        "SELECT `id`, `title`, `author`, `url`, `filepath`, `lccn` "
        "FROM `work_metadata`;")
    cursor.execute(sql_query)
    return [WorkMetadata(*row) for row in cursor.fetchall()]


def get_quotes(cursor: CursorBase) -> List[Quote]:
    '''
    Gets all the quotes from the MySQL database
    TODO: Add filters to only obtain specific quotes

    Args:
        cursor: The database cursor for performing the quote query

    Returns:    A list of Quote objects representing the quotes found
    '''
    select_quotes_sql = (
        "SELECT `id`, `content` "
        "FROM `quotes`;"
    )
    cursor.execute(select_quotes_sql)
    return [Quote(*row) for row in cursor.fetchall()]
