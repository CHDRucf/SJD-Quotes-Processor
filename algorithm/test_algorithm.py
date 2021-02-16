import os

import dotenv
import pytest
import sshtunnel
from mysql.connector import MySQLConnection, connect

from util.config import (Config, get_config_from_env,
                         get_database_connection_options_from_env,
                         get_ssh_connection_options_from_env)
from util.misc import get_filepaths, weighted_average
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
        get_database_connection_options_from_env(get_port=False)


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
    ''' 
    Test connection to project database using SSH tunnelling.
    Must be on the UCF VPN.
    '''

    # Need to override due to side effects from other tests
    dotenv.load_dotenv(override=True)

    config: Config = get_config_from_env(use_ssh_tunnelling=True)
    with sshtunnel.SSHTunnelForwarder(**config.ssh_connection_options, ) as tunnel:
        conn: MySQLConnection = connect(
            **config.my_sql_connection_options,
            port=tunnel.local_bind_port, connection_timeout=3)
        conn.close()


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


def test_get_filepaths():
    filepaths = [f'test-corpora{os.sep}dir1{os.sep}1.txt',
                 f'test-corpora{os.sep}dir2{os.sep}2.txt']
    if not all(os.path.isfile(filepath) for filepath in filepaths):
        pytest.skip("Directory 'test-corpora' could not be found")
    assert filepaths == get_filepaths("test-corpora")
