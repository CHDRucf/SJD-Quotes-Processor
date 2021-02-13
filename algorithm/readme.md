# Fuzzy Search Algorithm Module
This module provides functionality for the fuzzy search algorithm

## Dependencies
- Python 3 and pip
- A JSON file that contains the output of running the convert-excel-to-json
module on the sponsor-provided Excel file containing all the quotations
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

Place the quotes json file in the project directory and rename it to "quotes.json"

If you are running this program on a device that is not on the UCF
private network, then ensure that you are connected to the [UCF VPN](https://ucf.service-now.com/ucfit?id=kb_article&sys_id=ff89f4764f45e200be64f0318110c763)

Finally, please ensure that the following command line arguments have been set
for connecting to the database:

| Environment variable 	| Meaning                                                                                                                                                                	|
|----------------------	|------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| DB_USER              	| Username for the MySQL user                                                                                                                                            	|
| DB_PASS              	| Password for the MySQL user                                                                                                                                            	|
| DB_HOST              	| Name of the MySQL database to connect to                                                                                                                               	|
| DB_DB                	| Hostname or IP address of the server that the database is hosted on. If SSH tunneling is being used, this will most likely need to be set to the localhost (127.0.0.1) 	|
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
