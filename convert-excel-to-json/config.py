'''config.py:

Module for obtaining configuration options from environment variables
'''

from os import getenv
from typing import Dict, List, Union


def get_ssh_connection_options_from_env() -> Dict[str, Union[str, int]]:
    '''
    Loads the SSH connection options from the current environment
    into a dictionary suitable for being passed into the
    ssh.SSHTunnelForwarder method (ideally used as a context manager
    with the "with" keyword)

    Raises: EnvironmentError if any of the connection options are not found
    '''
    required_env_vars: List[str] = ["SSH_HOST", "SSH_PORT", "SSH_USER", "SSH_PASS",
                                    "_REMOTE_BIND_ADDRESS", "_REMOTE_MYSQL_PORT"]

    for var in required_env_vars:
        val = getenv(var)
        if not val:
            raise EnvironmentError(f"Environment variable {var} not set")

    return {
        "ssh_address_or_host": (getenv("SSH_HOST"), int(getenv("SSH_PORT"))),
        "ssh_username": getenv("SSH_USER"),
        "ssh_password": getenv("SSH_PASS"),
        "remote_bind_address": (getenv("_REMOTE_BIND_ADDRESS"), int(getenv("_REMOTE_MYSQL_PORT"))),
    }


def get_database_connection_options_from_env(get_port: bool = False) -> Dict[str, str]:
    '''
    Loads the database connection options from the current environment
    into a dictionary suitable for being passed into the
    mysql.connector.connect method.

    Args:
        get_port:   Whether or not to read the database port number from the
                    environment. This should be false if accessing the database
                    via an SSH tunnel

    Raises: EnvironmentError if any of the connection options are not found
    '''
    opt_env_var: Dict[str, str] = {
        "user": "DB_USER",
        "password": "DB_PASS",
        "host": "DB_HOST",
        "database": "DB_DB",
    }
    if get_port:
        opt_env_var["port"] = "DB_PORT"

    result: Dict[str, str] = {
        opt: getenv(env_var)
        for opt, env_var in opt_env_var.items()
    }

    for key, val in result.items():
        if not val:
            raise EnvironmentError(
                f"Environment variable {opt_env_var[key]} not set")
    return result
