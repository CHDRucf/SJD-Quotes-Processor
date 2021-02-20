'''database_ops.py

Functions for clearing the quotes table and writing
the quotes to the database
'''

from typing import List, Set

from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import CursorBase

from excel_to_json import QuoteMetadata


def write_quotes_to_database(quotes: Set[str], cursor: CursorBase):
    '''
    Writes the set of quotes to the database dictionary

    Does not commit this action.
    '''
    '''Some quotes have minor differences in punctuation and character casing.
    SQL ignores these differences and thus would otherwise allow duplicates,
    so we use a select clause to prevent this from happening
    
    It may be better to remove values that SQL would consider duplicates
    in Python beforehand to avoid needing the where cause in this statement'

    OR: Could try the follwing SQL to remove duplicates after inserting quotes,
    but before linking metadata:
    
    DELETE FROM `quotes`
    WHERE ID NOT IN (
        SELECT MAX(ID) AS MaxRecordID
        FROM `quotes`
        GROUP BY `content`);
    
    '''
    insert_quote_sql = (
        "INSERT INTO `quotes`(`content`) "
        "SELECT (%s) "
        "WHERE NOT EXISTS (SELECT ID FROM `quotes` WHERE `content` = %s);"
    )

    for i, quote in enumerate(quotes, 1):
        cursor.execute(insert_quote_sql, (quote, quote))
        print(f"Finished writing {i}/{len(quotes)} quotes to the database")


def delete_quotes_from_db(cursor: CursorBase):
    '''
    Deletes all quotes from the quotes table and resets the autoincrement
    on the quotes table.

    Does not commit this action.
    '''
    delete_quotes_sql = 'DELETE FROM `quotes`;'
    reset_quotes_auto_increment_sql = 'ALTER TABLE `quotes` AUTO_INCREMENT = 1;'

    cursor.execute(delete_quotes_sql)
    cursor.execute(reset_quotes_auto_increment_sql)


def delete_quote_metadata_from_db(cursor: CursorBase):
    '''
    Deletes all quote metadata from the quotes table and resets the
    autoincrement on the quotes metadata table.

    Does not commit this action.
    '''
    delete_quote_metadata_sql = 'DELETE FROM `quote_metadata`;'
    reset_quote_metadata_auto_increment_sql = 'ALTER TABLE `quote_metadata` AUTO_INCREMENT = 1;'

    cursor.execute(delete_quote_metadata_sql)
    cursor.execute(reset_quote_metadata_auto_increment_sql)


def get_quote_id(quote_text: str, cursor: CursorBase) -> int:
    '''
    Returns the ID of the record in the quotes table that has
    quote_text as its contents
    '''
    get_quote_sql = (
        "SELECT ID "
        "FROM `quotes` "
        "WHERE `content` = %s;"
    )

    cursor.execute(get_quote_sql, (quote_text,))
    result = cursor.fetchone()
    if result is None:
        raise LookupError(f"Could not find quote with text:\n{quote_text}")
    return result[0]


def insert_quote_metadatas_and_link_to_quotes(quote_metadatas: List[QuoteMetadata], cursor: CursorBase) -> None:
    '''
    Inserts each quote metadata record into the quote_metadata table and links
    each record to its corresponding quote in the quotes table.

    Does not commit this action.
    '''
    insert_quote_metadata_sql = (
        "INSERT INTO `quote_metadata`(`headword`, `title`, `author`, `quote_id`) "
        "VALUES (%s, %s, %s, %s);"
    )
    prev_quote: str = None
    quote_id: int = None
    for i, quote_metadata in enumerate(quote_metadatas, 1):
        # Optimization: Records with the same quote are likely to be
        # next to each other, so only look up quote if we have to
        if quote_metadata.quote != prev_quote:
            quote_id = get_quote_id(quote_metadata.quote, cursor)

        prev_quote = quote_metadata.quote
        cursor.execute(insert_quote_metadata_sql, (quote_metadata.headword,
                                                   quote_metadata.title, quote_metadata.author, quote_id))
        print(f"Inserted {i}/{len(quote_metadatas)} quote metadata records")


def reset_db_quotes(quotes_metadatas: List[QuoteMetadata], conn: MySQLConnection, delete_quotes: bool, write_quotes: bool, delete_metadata: bool, insert_and_link_metadata: bool):

    cursor: CursorBase = conn.cursor()

    if delete_quotes:
        delete_quotes_from_db(cursor)
        conn.commit()

    if write_quotes:
        q_texts = set(quote_metadata.quote
                      for quote_metadata in quotes_metadatas)
        write_quotes_to_database(q_texts, cursor)
        conn.commit()

    if delete_metadata:
        delete_quote_metadata_from_db(cursor)
        conn.commit()

    if insert_and_link_metadata:
        insert_quote_metadatas_and_link_to_quotes(quotes_metadatas, cursor)
        conn.commit()

    cursor.close()
