'''datbase_ops.py

Functions that interact with the database
'''

from typing import Dict, Tuple

from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import CursorBase

from util.custom_types import Metadata, QuoteDict


def write_to_database(quote: QuoteDict, top_five: Dict[str, float], conn: MySQLConnection) -> None:
    '''
    Args:
        quote:      An dictionary containing all the necessary fields for
                    writing the quote to the quotes table
        top_five:   A dictionary containing the top five matches for the given
                    quote mapped to their metadata
        conn:       The MySQLConnection object representing a connection to the
                    database

    TODO:   Test this. The method for obtaining the correct id for a quote may not work
            Alternatively, we could not query the quote id and just update all quotes
            that match the given quotes info (since in theory they would match anyway).
            This will probably tie into the edition number
    '''
    sql_query_quote_id = ("SELECT id "
                          "FROM quotes "
                          "WHERE quote = %s AND author = %s AND headword = %s;")
    sql_insert_statement = ("INSERT INTO matches(quote_id, metadata_id, rank, score, content)"
                            "VALUES (%s, %s, %s, %s, %s);"
                            )
    cursor: CursorBase = conn.cursor()
    for sentence, metadata in top_five:
        cursor.execute(sql_query_quote_id, (quote.quote,
                                            quote.author, quote.headword))
        quote_id_row: Tuple[int] = cursor.fetchone()
        cursor.execute(sql_insert_statement,
                       (quote_id_row[0], metadata.get("id"), 0, metadata.get("score"), sentence))
        conn.commit()


def get_file_metadata(file_name: str, cursor: CursorBase) -> Metadata:
    '''
    Returns a dict containing the metadata for a written work with
    the given file name

    Args:
        file_name:  The name of the file to obtain the metadata for
        cursor:     The database cursor for performing the metadata query
    # TODO: Test

    Returns:    A dictionary representing the SQL record for the given file's
                metadata
    '''
    sql_query: str = (
        "SELECT id, title, author, url, filepath, lccn "
        "FROM METADATA "
        "WHERE filepath = %s;")

    cursor.execute(sql_query, (file_name,))

    id_, title, author, url, filepath, lccn = cursor.fetchone()
    return {
        "id": id_,
        "title": title,
        "author": author,
        "url": url,
        "filepath": filepath,
        "lccn": lccn
    }
