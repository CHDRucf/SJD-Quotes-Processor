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

## Usage
Here is are the command line arguments for running the program
| Environment variable 	| Meaning | Default Value |
|----------------------	|-------- | ------------- |
| quotes-filepath | The filepath of the JSON file to write the converted quotes to | 'quotes.json'
| excel-filepath | The filepath to the sponsor-provided excel spreadsheet containing all the quotes | 'FullQuotes.xlsx'
| excel-to-json | Whether or not to convert the excel spreadsheet to JSON. This takes about a minute| False |
| write-to-db | This flag must be enabled to perform any operations on the database | False
| delete-quotes | Whether or not to delete all the records from the quotes table (this will be done before writing quote records) | False
| write-quotes | Whether or not to write all the quotes to the project database. This takes about 3 hours | False
| delete-metadata | Whether or not to delete all the records from the quote metadata table (this will be done before writing metadata records) | False
| insert-and-link-metadata | Whether or not to insert all the quote metadata records into the project database and link them to their respective quotes. This takes between 5 and 6 hours | False
| update_edition_numbers | Whether or not to update the edition number of each quote metadata record that appears in both the first and fourth edition of *Samuel Johnson's Dictionary* to "both". This takes about 1 hour | False
| use-ssh-tunnelling | Whether or not to use SSH tunnelling to connect to the project database. This should only be set to false if this program is being run on the project server itself | True
| help | View the list of command line arguments | N/A

The `--help` flag can be run for more info

Please note that all the database operations require a reliable database
connection for the entire length of the operation, and each operation gets
committed to the database after completion. For example, to insert and link
the metadata records, one would need 6 hours of uninterrupted Internet
connection. If at any point the connection drops, the *entire operation*
will need to be restarted. This requirement may be circumvented by running
the program directly on the project server.

## Testing
First ensure that the project's development dependencies are installed:

    `pipenv install --dev`

Then run the following command in the project directory:

    `pipenv run pytest`
