# Fuzzy Search Algorithm Module
This module provides functionality for the fuzzy search algorithm

## Dependencies
- Python 3 and pip
- A JSON file that contains the output of running the convert-excel-to-json
module on the sponsor-provided Excel file containing all the quotations

## Set Up
Install [pipenv](https://pypi.org/project/pipenv/):

    `pip install pipenv`

(If the above command does not work, try passing the -U flag to pip)

Open a terminal in this project's directory, and install the rest
of the project's dependencies using pipenv:
    
    `pipenv install`

Place the quotes json file in the project directory and rename it to "quotes.json"

## Usage
Run the following command in the project directory

    `pipenv run python main.py`

## Testing
First ensure that the project's development dependencies are installed:

    `pipenv install --dev`

Then run the following command in the project directory:

    `pipenv run pytest`
