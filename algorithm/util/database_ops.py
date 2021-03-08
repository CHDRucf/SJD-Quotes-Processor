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

    cursor.execute(select_quotes_by_author_sql, (author,))
    return [Quote(*row) for row in cursor.fetchall()]


def get_quick_lookup_quotes(cursor: CursorBase, quick_lookup_number: int) -> List[Quote]:
    '''
    Gets the quotes for the specified round of quick lookup

    Args:
        cursor:                 The database cursor for performing the quote query
        quick_lookup_number:   The quick lookup number to perform

    Returns:    A list of Quote objects representing the quotes found
    '''
    select_quotes_quick_lookup_sql_1 = (
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
            "Hooker,",
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
    select_quotes_quick_lookup_sql_2 = (
        """
        SELECT `id`, `content` 
        FROM `quotes` 
        WHERE id IN (
            SELECT `quote_id`
            FROM `quote_metadata`
            WHERE `author` IN (
                'Raleigh.',
                'Rogers.',
                'Davies.',
                'Thomson.',
                'Gay.',
                'Wiseman\'s',
                'Raleigh\'s',
                'Philips.',
                'Spenser\'s',
                'Newton\'s',
                'Mortimer.',
                'Ayliffe\'s',
                'King Charles.',
                'Roscommon.',
                'Ray.',
                'Taylor.',
                'Hale.',
                'Blackmore.',
                'Sidney,',
                'Hale\'s',
                'Grew\'s',
                'Addis.',
                'Cowley.',
                'Taylor\'s',
                'Knolles\'s',
                'Thomson\'s',
                'Burnet\'s',
                'Woodward\'s',
                'Stillingfleet.',
                'Bentley\'s',
                'Knolles.',
                'Hammond.',
                'Spenser',
                'Sandys.',
                'Ben. Johnson.',
                'Miller.',
                'Fairfax.',
                'Granville.',
                'Grew.',
                'Glanville.',
                'Sh.',
                'Wiseman.',
                'Carew.',
                'Glanville\'s',
                'Tusser.',
                'Rowe.',
                'Atterbury\'s',
                'Harvey',
                'Collier',
                'Carew\'s',
                'Burnet.',
                'Daniel.',
                'Glanv.',
                'Peacham.',
                'Peacham',
                'More.',
                'Ayliffe.',
                'Cleaveland.',
                'Wilkins.',
                'Phillips.',
                'Davies',
                'Arbuthnot\'s',
                'Rogers\'s',
                'Collier.',
                'Harvey.',
                'Chapman.',
                'Woodward',
                'Bacon\'s',
                'Clarendon,',
                'Holder.',
                'Crashaw.',
                'Cheyne.',
                'Suckling.',
                'Locke',
                'Shakespeare\'s',
                'Gay\'s',
                'Newton.',
                'Hammond\'s',
                'Ben. Johnson\'s',
                'Howel.',
                'Camden\'s',
                'Wotton\'s',
                'Broome.',
                'Garth.',
                'Herbert.',
                'Arbuth.',
                'Moxon\'s',
                'L\'Estr.',
                'Brown\'s',
                'Norris.',
                'Howel\'s',
                'Milton\'s',
                'Denham\'s',
                'Cheyne\'s',
                'More\'s',
                'Young.',
                'Wilkins\'s',
                'Smith.',
                'Law.',
                'Dry.'
            )
        );
        """
    )
    select_quotes_quick_lookup_sql_3 = (
        """
        SELECT `id`, `content` 
        FROM `quotes` 
        WHERE id IN (
            SELECT `quote_id`
            FROM `quote_metadata`
            WHERE `author` IN (
                'Derham.',
                'Dryden\'s',
                'Digby',
                'Boyle',
                'Derham\'s',
                'Walton\'s',
                'Camden.',
                'Add.',
                'L\'Estrange\'s',
                'Sharp\'s',
                'Bac.',
                'Tillotson\'s',
                'Woodw.',
                'Spens.',
                'K. Charles.',
                'Digby.',
                'Boyle\'s',
                'Bacon,',
                'King.',
                'Holder\'s',
                'Moxon.',
                'Drayton.',
                'Swift',
                'Creech.',
                'Daniel\'s',
                'Ascham\'s',
                'Addison\'s',
                'Chapman\'s',
                'Fell.',
                'Holder',
                'Tillotson,',
                'Harte.',
                'Sandys\'s',
                'Hakewill',
                'B. Johnson.',
                'Tickell.',
                'Evelyn\'s',
                'Abbot.',
                'Rowe\'s',
                'Arb.',
                'Walton.',
                'Arbuthn.',
                'Graunt.',
                'Quincy.',
                'Floyer',
                'Watts',
                'Graunt\'s',
                'Hakewill.',
                'Mort.',
                'Baker.',
                'Abbot\'s',
                'Spratt.',
                'Felton',
                'Wake.',
                'Floyer.',
                'Sprat.',
                'Atterb.',
                'Tickel.',
                'L\'Estrange,',
                'Sharp.',
                'Arbuthnot and Pope.',
                'Otway.',
                'Ascham.',
                'Sha.',
                'Broome\'s',
                'Hook.',
                'Wake\'s',
                'Pope\'s',
                'L\'Estrange.',
                'Fairfax,',
                'South\'s',
                'May\'s',
                'Temple\'s',
                'Sprat\'s',
                'Pope',
                'Spratt\'s',
                'Blackm.',
                'Whitgifte.',
                'Newt.',
                'Rogers,',
                'Tusser\'s',
                'Milton',
                'Drayton\'s',
                'White.',
                'Felton.',
                'Congreve.',
                'Evelyn.',
                'Hammond',
                'B. Johns.',
                'Southern.',
                'Garth\'s',
                'Calamy\'s',
                'Baker',
                'Hale\'s',
                'Sanderson.',
                'Waterland.',
                'Holyday.',
                'King\'s',
                'Dennis.',
                'Hill\'s'
            )
        );
        """
    )
    if quick_lookup_number == 1:
        cursor.execute(select_quotes_quick_lookup_sql_1)
    elif quick_lookup_number == 2:
        cursor.execute(select_quotes_quick_lookup_sql_2)
    elif quick_lookup_number == 3:
        cursor.execute(select_quotes_quick_lookup_sql_3)
    else:
        raise ValueError(f"Invalid quick lookup error: {quick_lookup_number}")
    return [Quote(*row) for row in cursor.fetchall()]


def get_non_quick_lookup_quotes(cursor: CursorBase) -> List[Quote]:
    '''
    Gets all the quotes that are either in the failure queue or are
    attributed to authors not in the quick lookup lists
    '''
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
            "Hooker,",
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
            "Swift's",
            'Raleigh.',
            'Rogers.',
            'Davies.',
            'Thomson.',
            'Gay.',
            'Wiseman\'s',
            'Raleigh\'s',
            'Philips.',
            'Spenser\'s',
            'Newton\'s',
            'Mortimer.',
            'Ayliffe\'s',
            'King Charles.',
            'Roscommon.',
            'Ray.',
            'Taylor.',
            'Hale.',
            'Blackmore.',
            'Sidney,',
            'Hale\'s',
            'Grew\'s',
            'Addis.',
            'Cowley.',
            'Taylor\'s',
            'Knolles\'s',
            'Thomson\'s',
            'Burnet\'s',
            'Woodward\'s',
            'Stillingfleet.',
            'Bentley\'s',
            'Knolles.',
            'Hammond.',
            'Spenser',
            'Sandys.',
            'Ben. Johnson.',
            'Miller.',
            'Fairfax.',
            'Granville.',
            'Grew.',
            'Glanville.',
            'Sh.',
            'Wiseman.',
            'Carew.',
            'Glanville\'s',
            'Tusser.',
            'Rowe.',
            'Atterbury\'s',
            'Harvey',
            'Collier',
            'Carew\'s',
            'Burnet.',
            'Daniel.',
            'Glanv.',
            'Peacham.',
            'Peacham',
            'More.',
            'Ayliffe.',
            'Cleaveland.',
            'Wilkins.',
            'Phillips.',
            'Davies',
            'Arbuthnot\'s',
            'Rogers\'s',
            'Collier.',
            'Harvey.',
            'Chapman.',
            'Woodward',
            'Bacon\'s',
            'Clarendon,',
            'Holder.',
            'Crashaw.',
            'Cheyne.',
            'Suckling.',
            'Locke',
            'Shakespeare\'s',
            'Gay\'s',
            'Newton.',
            'Hammond\'s',
            'Ben. Johnson\'s',
            'Howel.',
            'Camden\'s',
            'Wotton\'s',
            'Broome.',
            'Garth.',
            'Herbert.',
            'Arbuth.',
            'Moxon\'s',
            'L\'Estr.',
            'Brown\'s',
            'Norris.',
            'Howel\'s',
            'Milton\'s',
            'Denham\'s',
            'Cheyne\'s',
            'More\'s',
            'Young.',
            'Wilkins\'s',
            'Smith.',
            'Law.',
            'Dry.',
            'Derham.',
            'Dryden\'s',
            'Digby',
            'Boyle',
            'Derham\'s',
            'Walton\'s',
            'Camden.',
            'Add.',
            'L\'Estrange\'s',
            'Sharp\'s',
            'Bac.',
            'Tillotson\'s',
            'Woodw.',
            'Spens.',
            'K. Charles.',
            'Digby.',
            'Boyle\'s',
            'Bacon,',
            'King.',
            'Holder\'s',
            'Moxon.',
            'Drayton.',
            'Swift',
            'Creech.',
            'Daniel\'s',
            'Ascham\'s',
            'Addison\'s',
            'Chapman\'s',
            'Fell.',
            'Holder',
            'Tillotson,',
            'Harte.',
            'Sandys\'s',
            'Hakewill',
            'B. Johnson.',
            'Tickell.',
            'Evelyn\'s',
            'Abbot.',
            'Rowe\'s',
            'Arb.',
            'Walton.',
            'Arbuthn.',
            'Graunt.',
            'Quincy.',
            'Floyer',
            'Watts',
            'Graunt\'s',
            'Hakewill.',
            'Mort.',
            'Baker.',
            'Abbot\'s',
            'Spratt.',
            'Felton',
            'Wake.',
            'Floyer.',
            'Sprat.',
            'Atterb.',
            'Tickel.',
            'L\'Estrange,',
            'Sharp.',
            'Arbuthnot and Pope.',
            'Otway.',
            'Ascham.',
            'Sha.',
            'Broome\'s',
            'Hook.',
            'Wake\'s',
            'Pope\'s',
            'L\'Estrange.',
            'Fairfax,',
            'South\'s',
            'May\'s',
            'Temple\'s',
            'Sprat\'s',
            'Pope',
            'Spratt\'s',
            'Blackm.',
            'Whitgifte.',
            'Newt.',
            'Rogers,',
            'Tusser\'s',
            'Milton',
            'Drayton\'s',
            'White.',
            'Felton.',
            'Congreve.',
            'Evelyn.',
            'Hammond',
            'B. Johns.',
            'Southern.',
            'Garth\'s',
            'Calamy\'s',
            'Baker',
            'Hale\'s',
            'Sanderson.',
            'Waterland.',
            'Holyday.',
            'King\'s',
            'Dennis.',
            'Hill\'s'
            )
        )
        OR `id` IN (
            SELECT `quote_id`
            FROM `failed_quick_lookup`
        );
        """
    )
    cursor.execute(select_quotes_nonquick_lookup_sql)
    return [Quote(*row) for row in cursor.fetchall()]


def write_quote_id_to_failed_quick_lookup(cursor: CursorBase, quote_id: int) -> None:
    '''
    Inserts a quote id that failed the quick lookup to the failed_quick_lookup
    table in the MySQL database

    Args:
        cursor:     The database cursor for performing the insertion
        quote_id:   The id of the quote that failed the quick lookup

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
