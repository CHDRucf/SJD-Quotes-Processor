import os
from typing import Dict, List

import dotenv
import pytest
from mysql.connector import MySQLConnection, connect

import main


def test_get_connection_options_raises_error():
    os.environ["DB_USER"] = ""
    with pytest.raises(EnvironmentError):
        main.get_connection_options_from_env()


@pytest.mark.skip("Database privileges do not currently \
    allow for remote connection")
def test_connection():
    ''' Test connection to project database. Must be on the UCF VPN.'''
    # Need to override due to side effects from other tests
    dotenv.load_dotenv(override=True)
    options: Dict[str, str] = main.get_connection_options_from_env()
    conn: MySQLConnection = connect(**options, connection_timeout=4)
    conn.close()


def test_flatten_quotes():
    headword_quotes: dict = {
        "A": [
            {
                "edition": 1,
                "definition": "The first letter of the European alphabets, A, an article set before nouns of the singular number;  a man, a tree; denoting the number one, or an indefinite indication, A is sometimes a noun; A is placed before a participle, or participial noun; and is considered by Wallis as a contraction of  at, when it is put before a word denoting some action not yet finished;It also seems to be anciently contracted from at, when placed before local surnames;In other cases, it seems to signify to, like the French à. ",
                "quote": "A hunting Chloë went.",
                "title": "",
                "author": "Prior.",
                "flag": False
            },
            {
                "edition": 1,
                "definition": "The first letter of the European alphabets, A, an article set before nouns of the singular number;  a man, a tree; denoting the number one, or an indefinite indication, A is sometimes a noun; A is placed before a participle, or participial noun; and is considered by Wallis as a contraction of  at, when it is put before a word denoting some action not yet finished;It also seems to be anciently contracted from at, when placed before local surnames;In other cases, it seems to signify to, like the French à. ",
                "quote": "And now a breeze from shore began to blow, The sailors ship their oars, and cease to row; Then hoist their yards a-trip, and all their sails Let fall, to court the wind, and catch the gales.",
                "title": "Ceyx and Alcyone.",
                "author": "Dryden’s",
                "flag": False
            },
            {
                "edition": 4,
                "definition": "Letter 'a'",
                "quote": "And now a breeze from shore began to blow, The sailors ship their oars, and cease to row; Then hoist their yards a-trip, and all their sails Let fall, to court the wind, and catch the gales.",
                "title": "",
                "author": "",
                "flag": False
            },
        ]
    }

    expected: List[Dict[str, str]] = [
        {
            "headword": "A",
            "edition": 1,
            "definition": "The first letter of the European alphabets, A, an article set before nouns of the singular number;  a man, a tree; denoting the number one, or an indefinite indication, A is sometimes a noun; A is placed before a participle, or participial noun; and is considered by Wallis as a contraction of  at, when it is put before a word denoting some action not yet finished;It also seems to be anciently contracted from at, when placed before local surnames;In other cases, it seems to signify to, like the French à. ",
            "quote": "A hunting Chloë went.",
            "title": "",
            "author": "Prior.",
            "flag": False
        },
        {
            "headword": "A",
            "edition": 1,
            "definition": "The first letter of the European alphabets, A, an article set before nouns of the singular number;  a man, a tree; denoting the number one, or an indefinite indication, A is sometimes a noun; A is placed before a participle, or participial noun; and is considered by Wallis as a contraction of  at, when it is put before a word denoting some action not yet finished;It also seems to be anciently contracted from at, when placed before local surnames;In other cases, it seems to signify to, like the French à. ",
            "quote": "And now a breeze from shore began to blow, The sailors ship their oars, and cease to row; Then hoist their yards a-trip, and all their sails Let fall, to court the wind, and catch the gales.",
            "title": "Ceyx and Alcyone.",
            "author": "Dryden’s",
            "flag": False
        },
        {
            "headword": "A",
            "edition": 4,
            "definition": "Letter 'a'",
            "quote": "And now a breeze from shore began to blow, The sailors ship their oars, and cease to row; Then hoist their yards a-trip, and all their sails Let fall, to court the wind, and catch the gales.",
            "title": "",
            "author": "",
            "flag": False
        }
    ]

    assert expected == main.flatten_quotes(headword_quotes)
