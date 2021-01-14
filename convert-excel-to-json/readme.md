# Excel to JSON Module
This module provides functionality for converting the sponsor-provided
quotes Excel sheet into a JSON file for the fuzzy search algorithm
to process more easily

## Dependencies
- Python 3 and pip
- The sponsor-provided Excel file containing all the quotations in
_Johnson's Dictionary_

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
Run the following command in the project directory

    `pipenv run python excel_to_json.py`

## Testing
First ensure that the project's development dependencies are installed:

    `pipenv install --dev`

Then run the following command in the project directory:

    `pipenv run pytest`
