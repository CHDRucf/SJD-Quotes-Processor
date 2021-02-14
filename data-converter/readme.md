# Excel to JSON Module
This module provides functionality for converting the sponsor-provided
quotes Excel sheet into a JSON file for the fuzzy search algorithm
to process more easily, and for exporting that JSON file to
the project database

## Dependencies
- Python 3 and pip
- The sponsor-provided Excel file containing all the quotations in
_Johnson's Dictionary_

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
set in a .env file and placed in the `data-converter` folder (next to
this readme file). Please remember, _do not commit the .env file_
to version control (check that the name `.env` is included
in the .gitignore file)

## Set Up
Install [pipenv](https://pypi.org/project/pipenv/):

    `pip install pipenv`

(If the above command does not work, try passing the -U flag to pip)

Open a terminal in this project's directory, and install the rest
of the project's dependencies using pipenv:
    
    `pipenv install`

Place the sponsor-provided quotes Excel file into the project directory
and rename it to "FullQuotes.xlsx"

## Usage
To run the program without performing any conversion (no action is performed):
    `pipenv run python main.py`

To run the excel-to-json converter:
    `pipenv run python main.py --excel-to-json`

To run the json-to-sql converter (writes the quotes to the database):
    `pipenv run python main.py --json-to-sql`

Both flags can be supplied to first perform the json conversion and
then write the results to the database

Lastly, the `--help` flag can be run for more info

## Testing
First ensure that the project's development dependencies are installed:

    `pipenv install --dev`

Then run the following command in the project directory:

    `pipenv run pytest`
