'''test_config.py

Tests for the config module
'''

import os

import dotenv
import pytest
import sshtunnel
from mysql.connector import MySQLConnection, connect
from util.config import (Config, get_config_from_env,
                         get_database_connection_options_from_env,
                         get_ssh_connection_options_from_env)


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
