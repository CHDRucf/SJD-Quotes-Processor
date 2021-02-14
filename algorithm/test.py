import os
from typing import Dict, List, Union

import dotenv
import pytest
import sshtunnel
from mysql.connector import MySQLConnection, connect

import main
from util.config import (get_database_connection_options_from_env,
                         get_ssh_connection_options_from_env)
from util.misc import flatten_quotes, weighted_average
from util.string_comp import jaccard_index


def test_get_ssh_connection_options_raises_error():
    '''
    Test that an error is raised if an environment variable
    relating to the ssh connection is not set
    '''
    os.environ["SSH_HOST"] = ""
    with pytest.raises(EnvironmentError):
        get_ssh_connection_options_from_env()


def test_get_database_connection_options_raises_error_no_port():
    '''
    Test that an error is raised if an environment variable
    relating to the database connection is not set
    (get_port=False)
    '''
    os.environ["DB_USER"] = ""
    with pytest.raises(EnvironmentError):
        get_database_connection_options_from_env()


def test_get_database_connection_options_raises_error_port():
    '''
    Test that an error is raised if an environment variable
    relating to the database connection is not set
    (get_port=True)
    '''
    os.environ["DB_PORT"] = ""
    with pytest.raises(EnvironmentError):
        get_database_connection_options_from_env(get_port=True)


@pytest.mark.db_connection
def test_database_connection():
    ''' Test connection to project database. Must be on the UCF VPN.'''

    # Need to override due to side effects from other tests
    dotenv.load_dotenv(override=True)

    ssh_options: Dict[str, Union[str, int]
                      ] = get_ssh_connection_options_from_env()

    with sshtunnel.SSHTunnelForwarder(**ssh_options) as tunnel:
        mysql_options: Dict[str,
                            str] = main.get_database_connection_options_from_env()
        conn: MySQLConnection = connect(
            **mysql_options, port=tunnel.local_bind_port, connection_timeout=4)
        conn.close()


def test_flatten_quotes():
    '''
    Test that quotes JSON file is correctly flattened after being deserialized
    '''
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

    assert expected == flatten_quotes(headword_quotes)


def test_jaccard_index():
    sets_and_j_values = [
        ({1, 2, 3}, {4, 5, 6}, 0),
        ({1, 2, 3}, {3, 5, 6}, (1/5)),
        ({'c', 'a', 'r'}, {'b', 'a', 'r'}, (2/4)),
        ({'u', 'c', 'f'}, {'u', 's', 'f'}, (2/4))
    ]
    for set1, set2, expected in sets_and_j_values:
        assert jaccard_index(set1, set2) == expected


def test_weighted_average():
    values_averages = [
        ([(1, 0.5), (1, 0.5)], 1),
        ([(3, 0.15), (5, 0.5), (10, 0.05), (4, 0.3)], 4.65)
    ]
    for values, expected in values_averages:
        assert weighted_average(values) == expected


def test_weighted_average_raises_error():
    weights_do_not_add_up_to_1 = [
        (1, 0.5), (2, 0.3), (4, 0.6)
    ]
    with pytest.raises(ValueError):
        weighted_average(weights_do_not_add_up_to_1)