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
Run the following command in the project directory

    `pipenv run python main.py`

The program supports the following command line arguments:

| Argument                                         | Meaning                                                                                                                                                                                                           | Default                                      |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| --use-ssh-tunnelling / --no-use-ssh-tunnelling   | Whether or not to use SSH tunneling to connect to the project database                                                                                                                                            | True                                         |
| --corpora-path                                   | Path to the directory containing the corpora to search over                                                                                                                                                       | "./corpora"                                  |
| --load-dotenv / --no-load-dotenv                 | Whether or not to load the environment variables from a .env file                                                                                                                                                 | True                                         |
| --perform-search / --no-perform-search           | Whether or not to actually perform the fuzzy search. If false, then the matches will be read from the JSON file located at the path specified by the --json-path argument                                         | True                                         |
| --use-multiprocessing / --no-use-multiprocessing | Whether or not to use multiprocessing to search for the quotes. Multiprocessing is recommended. Has no effect if the search is not actually performed                                                             | True                                         |
| --num-processes                                  | The number of processes to create for performing the fuzzy search                                                                                                                                                 | The number of CPU cores on the host computer |
| --write-to-json / --no-write-to-json             | Whether or not to write the matches to a JSON file                                                                                                                                                                | True                                         |
| --write-to-database / --no-write-to-database     | Whether or not to write the matches to the project database                                                                                                                                                       | False                                        |
| --json-path                                      | The path to the JSON file to read the matches from if not performing the search, and write the matches to if writing the matches to JSON. Has no effect if performing the search and only writing to the database | "matches.json"                               |
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
