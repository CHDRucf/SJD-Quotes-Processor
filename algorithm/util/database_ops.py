'''datbase_ops.py

Functions that interact with the database
'''

from typing import List

from mysql.connector.cursor import CursorBase

from util.custom_types import Quote, QuoteMatch, WorkMetadata


def write_match_to_database(cursor: CursorBase, match_: QuoteMatch) -> None:
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


def get_quotes_by_author(cursor: CursorBase, author: str) -> List[Quote]:
    '''
    Gets all the quotes ascribed to a certain author in the MySQL database

    Args:
        cursor: The database cursor for performing the quote query
        author: The name of the author to obtains quotes for

    Returns:    A list of Quote objects representing the quotes found
    '''

    select_quotes_by_author_sql = (
        '''
        SELECT `id`, `content`
        FROM `quotes`
        WHERE id IN (
            SELECT `quote_id`
            FROM `quote_metadata`
            WHERE `author` = %s
            );
        '''
    )

    cursor.execute(select_quotes_by_author_sql)
    return [Quote(*row) for row in cursor.fetchall((author,))]


def get_quotes(cursor: CursorBase, use_quick_lookup: bool) -> List[Quote]:
    '''
    Gets all the quotes from the MySQL database

    Args:
        cursor:             The database cursor for performing the quote query
        use_quick_lookup:   Whether to search for the quotes by an author for
                            whom a list of works already exists for quick
                            lookup, or to search for all other quotes (or
                            quotes which failed quick lookup) over all the
                            entire corpora


    Returns:    A list of Quote objects representing the quotes found
    '''
    select_quotes_quick_lookup_sql = (
        """
        SELECT `id`, `content` 
        FROM `quotes` 
        WHERE id IN (
            SELECT `quote_id`
            FROM `quote_metadata`
            WHERE `author` IN (
            "Shakesp.",
            "Dryden.",
            "Shakespeare.",
            "Bible",
            "Milton.",
            "Pope.",
            "Locke.",
            "Swift.",
            "Shakespeare's",
            "Bacon.",
            "Dryden's",
            "Bacon's",
            "Addison.",
            "Milton's",
            "Hooker.",
            "Prior.",
            "Spenser.",
            "Addison's",
            "South.",
            "Brown's",
            "Shak.",
            "Sidney.",
            "L'Estrange.",
            "Dryd.",
            "Boyle.",
            "Pope's",
            "Arbuthnot",
            "Shakes.",
            "Arbuthnot.",
            "South's",
            "Waller.",
            "Clarendon.",
            "Brown.",
            "Denham.",
            "\"Hooker,\"",
            "Atterbury.",
            "Temple.",
            "Watts.",
            "Addison",
            "Donne.",
            "Tillotson.",
            "Wotton.",
            "Mortimer's",
            "Woodward.",
            "Watts's",
            "Ray",
            "Milt.",
            "Hayward.",
            "Bentley.",
            "Swift's"
            )
        );
        """
    )
    select_quotes_nonquick_lookup_sql = (
        """
        SELECT `id`, `content` 
        FROM `quotes` 
        WHERE `id` NOT IN (
            SELECT `quote_id`
            FROM `quote_metadata`
            WHERE `author` IN (
            "Shakesp.",
            "Dryden.",
            "Shakespeare.",
            "Bible",
            "Milton.",
            "Pope.",
            "Locke.",
            "Swift.",
            "Shakespeare's",
            "Bacon.",
            "Dryden's",
            "Bacon's",
            "Addison.",
            "Milton's",
            "Hooker.",
            "Prior.",
            "Spenser.",
            "Addison's",
            "South.",
            "Brown's",
            "Shak.",
            "Sidney.",
            "L'Estrange.",
            "Dryd.",
            "Boyle.",
            "Pope's",
            "Arbuthnot",
            "Shakes.",
            "Arbuthnot.",
            "South's",
            "Waller.",
            "Clarendon.",
            "Brown.",
            "Denham.",
            "\"Hooker,\"",
            "Atterbury.",
            "Temple.",
            "Watts.",
            "Addison",
            "Donne.",
            "Tillotson.",
            "Wotton.",
            "Mortimer's",
            "Woodward.",
            "Watts's",
            "Ray",
            "Milt.",
            "Hayward.",
            "Bentley.",
            "Swift's"
            )
        )
        OR `id` IN (
            SELECT `quote_id`
            FROM `failed_quick_lookup`
        );
        """
    )

    if use_quick_lookup:
        cursor.execute(select_quotes_quick_lookup_sql)
    else:
        cursor.execute(select_quotes_nonquick_lookup_sql)
    return [Quote(*row) for row in cursor.fetchall()]


def write_quote_id_to_failed_quick_lookup(cursor: CursorBase, quote_id: int) -> None:
    '''
    Inserts a quote id that failed the quick lookup to the failed_quick_lookup
    table in the MySQL database

    Args:
        cursor:     The database cursor for performing the insertion
        quote_id:   The id of the quote that failed the quick lookup

    TODO: Complete. Make sure that failed quotes that are already present
    are not inserted again

    insert into failed_quick_lookup (quote_id) select( 1 )
    where not exists (select quote_id from failed_quick_lookup where quote_id = 1)

    '''
    insert_into_failed_if_not_exists_sql = (
        '''
        INSERT INTO `failed_quick_lookup`(`quote_id`)
        SELECT (%s)
        WHERE NOT EXISTS (
            SELECT `quote_id`
            FROM `failed_quick_lookup`
            WHERE `quote_id` = %s
        );
        '''
    )
    cursor.execute(insert_into_failed_if_not_exists_sql, (quote_id, quote_id))
