# Fuzzy Search Algorithm Module
This module provides functionality for the fuzzy search algorithm

## Dependencies
- Python 3 and pip
- A corpora directory containing the works to search over.
The path to each of these works _must_ match the path to each work's
corresponding metadata record in the project database.
- A connection to the project database, which will most likely require
being on the [UCF VPN](https://ucf.service-now.com/ucfit?id=kb_article&sys_id=ff89f4764f45e200be64f0318110c763)
and having a user account on the project server for SSH tunnelling purposes
- The rapidfuzz Python module, which the algorithm uses for its fuzzy search, has additional dependencies. These can be found on its [PyPi page](https://pypi.org/project/rapidfuzz/) (scroll to the section labeled "Requirements") or its [GitHub page](https://github.com/maxbachmann/rapidfuzz#requirements) (direct link)
- The python-Levenshtein and rapidfuzz modules may not initially work. If they throw errors, the C++14 redistributables may need to be installed if on Windows. See the rapidfuzz modules [PyPI page](https://pypi.org/project/rapidfuzz/) for more information. If on Linux, the rapidfuzz library can be installed with pip via a wheel file (this will have to be done manually but is not hard. Here is a link to the wheel files for the [rapidfuzz](https://pypi.org/project/rapidfuzz/#modal-close)). For Levenshtein, [this PyPI project](https://pypi.org/project/python-Levenshtein-wheels/) can be used instead

## Set Up
Install [pipenv](https://pypi.org/project/pipenv/):

    `pip install pipenv`

(If the above command does not work, try passing the -U flag to pip)

Open a terminal in this project's directory, and install the rest
of the project's dependencies using pipenv:
    
    `pipenv install`

If you are running this program on a device that is not on the UCF
private network, then ensure that you are connected to the [UCF VPN](https://ucf.service-now.com/ucfit?id=kb_article&sys_id=ff89f4764f45e200be64f0318110c763)

Please ensure that the following environment variables have been set
for connecting to the database:

| Environment variable 	| Meaning                                                                                                                                                                	|
|----------------------	|------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| DB_USER              	| Username for the MySQL user                                                                                                                                            	|
| DB_PASS              	| Password for the MySQL user                                                                                                                                            	|
| DB_HOST              	| Hostname or IP address of the server that the database is hosted on. If SSH tunneling is being used, this will most likely need to be set to the localhost (127.0.0.1)   	|
| DB_DB                	| Name of the MySQL Database to Connect to                                                                                                                                  |
| SSH_HOST             	| Hostname or IP address of the server to be connected to if using SSH tunneling                                                                                         	|
| SSH_PORT             	| Port to use for SSH tunneling. Will most likely be 22                                                                                                                  	|
| SSH_USER             	| Username for the SSH user                                                                                                                                              	|
| SSH_PASS             	| Password for the SSH user                                                                                                                                              	|
| _REMOTE_BIND_ADDRESS 	| Set to 127.0.0.1                                                                                                                                                       	|
| _REMOTE_MYSQL_PORT   	| Set to 3306                                                                                                                                                            	|

If you are running this program on a personal device, these variables can be
set in a .env file and placed in the `algorithm` folder (next to
this readme file). Please remember, _do not commit the .env file_
to version control (check that the name `.env` is included
in the .gitignore file)

## Usage
Run the following command in the project directory to search for the quick lookup quotes:

    `pipenv run python main.py --search-quick-lookup=True`

This should take approximately 30 hours to run to completion if running on a single processor. The runtime can be improved by assigning multiple processors to the program. This should divide the runtime by a factor equal to about the number of processors assigned to the program. Once finished, the results will be written to a JSON file. To write the results in that JSON file to the database, run this command:

    `pipenv run python main.py --search-quick-lookup=True --perform-search=False --write-to-database=True`

This will not actually search for quotes, it will only read the matches from in the matches json file (see below), and write those matches to the database.

The program supports the following command line arguments:

| Argument                                         | Meaning                                                                                                                                                                                                           | Default                                      |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| --search-quick-lookup / --no-search-quick-lookup | Whether to search only for the quick lookup quotes, or the non quick lookup quotes / quotes that failed the quick lookup search                                                                                   | True                                         |
| --quick-lookup-json-dir                          | The path to the directory containing the JSON files specifying the quick lookup locations for the quick lookup quotes                                                                                             | "./quick-lookup-metadata"                    |
| --use-ssh-tunnelling / --no-use-ssh-tunnelling   | Whether or not to use SSH tunneling to connect to the project database                                                                                                                                            | True                                         |
| --corpora-path                                   | Path to the directory containing the corpora to search over                                                                                                                                                       | "./corpora"                                  |
| --load-dotenv / --no-load-dotenv                 | Whether or not to load the environment variables from a .env file                                                                                                                                                 | True                                         |
| --perform-search / --no-perform-search           | Whether or not to actually perform the fuzzy search. If false, then the matches will be read from the JSON file located at the path specified by the --json-path argument                                         | True                                         |
| --use-multiprocessing / --no-use-multiprocessing | Whether or not to use multiprocessing to search for the quotes. Multiprocessing is recommended. Has no effect if the search is not actually performed                                                             | True                                         |
| --num-processes                                  | The number of processes to create for performing the fuzzy search                                                                                                                                                 | The number of CPU cores on the host computer |
| --write-to-json / --no-write-to-json             | Whether or not to write the matches to a JSON file                                                                                                                                                                | True                                         |
| --write-to-database / --no-write-to-database     | Whether or not to write the matches to the project database                                                                                                                                                       | False                                        |
| --json-path                                      | The path to the JSON file to read the matches from if not performing the search, and write the matches to if writing the matches to JSON. Has no effect if performing the search and only writing to the database | "./matches.json"                             |
| --chunk-size                                     | The size of the chunks to break the quotes into when performing multiprocessing. Multiprocessing will be performed on each chunk of quotes.                                                                       | The number of CPU cores on the host computer |
| --quick-lookup-number | Which round of quick lookup to perform. Raises an error if an invalid value is passed and quick lookup is enabled. Defaults to an invalid value. | -1
| --manual-quick-lookup / --no-manual-quick-lookup | Whether to perform the quick search on the quotes for which a manual quick lookup list has been compiled, or on all the other quotes (not including the ones in the failure table). If this is set to True, then a valid value must be passed to --quick-lookup-number | True
| --help                                           | Display a list of the program's command line arguments                                                                                                                                                            | N/A                                          |
## Testing
First ensure that the project's development dependencies are installed:

    `pipenv install --dev`

You should now be able to run the tests. Some of the tests require a connection
to the database. If you would like to skip those tests, you can do so by
just running pytest normally;

    `pipenv run pytest`

If you would like to run all the tests, including, those that require a
connection to the database, run this command:

    `pipenv run pytest --run-connection-tests`

If you would like to only run the file fuzzy search tests, run this command:

    `pipenv run pytest -k over_file`

If several tests fail, the above command may print enough debug messages to the console to delay the presentation of the test results. This can be circumvented by passing the `--no-summary` flag, like so:

    `pipenv run pytest -k over_file --no-summary`
