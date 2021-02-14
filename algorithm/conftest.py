'''conftest.py

Pytest reads this module before running tests to apply
custom user configuration as to how they are run

In this case, command line options have been added for specifying
whether or not to run certain tests

See https://docs.pytest.org/en/stable/example/simple.html#control-skipping-of-tests-according-to-command-line-option
'''
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--run-connection-tests", action="store_true", default=False, help="run tests that require a connection to the database"
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "db_connection: mark test as requiring a database connection")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-connection-tests"):
        # --run-connection-tests given in cli: do not skip tests that
        # require a db connection
        return
    skip_conn_tests = pytest.mark.skip(
        reason="need --run-connection-tests option to run")
    for item in items:
        if "db_connection" in item.keywords:
            item.add_marker(skip_conn_tests)
