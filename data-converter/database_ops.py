'''database_ops.py

Functions for clearing the quotes table and writing
the quotes to the database
'''

from typing import Dict, Union

from mysql.connector.cursor import CursorBase


def write_quotes_to_database(quotes: Dict[str, Union[str, int]], cursor: CursorBase):
    '''
    Writes a dictionary of quotes to the project database.
    The quotes dictionary must follow the schema outlined in
    excel_to_json.py.

    Does not commit this action.
    '''
    insert_quote_sql = (
        "INSERT INTO `quotes`(`headword`, `quote`, `title`, `author`) "
        "VALUES (%s, %s, %s, %s);"
    )

    fields = ["quote", "title", "author"]
    for i, headword in enumerate(quotes, 1):
        for quote in quotes.get(headword):
            quote_text, title, author, = [quote.get(field) for field in fields]
            cursor.execute(insert_quote_sql,
                           (headword, quote_text, title, author))
        print(f"Finished writing all quotes for {i}/{len(quotes)} headwords")


def delete_quotes_from_db(cursor: CursorBase):
    '''
    Deletes all quotes from the quotes table.
    
    Does not commit this action.
    '''
    delete_quotes_sql = 'DELETE FROM `quotes`;'
    cursor.execute(delete_quotes_sql)
