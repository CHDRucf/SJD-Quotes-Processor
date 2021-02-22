'''datbase_ops.py

Functions that interact with the database
'''

from typing import List, Union

from mysql.connector.cursor import CursorBase

from util.custom_types import Quote, QuoteMatch, WorkMetadata


def write_match_to_database(match_: QuoteMatch, cursor: CursorBase) -> None:
    '''
    Args:
        matches:    An quote matche to write to the database
        conn:       The MySQLConnection object representing a connection to the
                    database
    '''
    sql_insert_statement = (
        "INSERT INTO `matches`(`quote_id`, `work_metadata_id`, `rank`, `score`, `content`) "
        "VALUES (%s, %s, %s, %s, %s);"
    )
    cursor.execute(sql_insert_statement, match_)


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


def get_quotes(cursor: CursorBase, start_quote_id: int, end_quote_id: Union[int, None]) -> List[Quote]:
    '''
    Gets all the quotes from the MySQL database

    Args:
        cursor:         The database cursor for performing the quote query
        start_quote_id: The ID of the first quote to search for
        end_quote_id:   The ID of the last quote to search for. If set to None,
                        then the search will run until all quotes have been
                        searched for

    Returns:    A list of Quote objects representing the quotes found
    '''
    select_quotes_sql = (
        "SELECT `id`, `content` "
        "FROM `quotes` "
        "WHERE `id` >= %s"
    )
    if end_quote_id is not None:
        select_quotes_sql += " AND `id` <= %s;"
        cursor.execute(select_quotes_sql, (start_quote_id, end_quote_id))
    else:
        select_quotes_sql += ';'
        cursor.execute(select_quotes_sql, (start_quote_id,))
    return [Quote(*row) for row in cursor.fetchall()]
