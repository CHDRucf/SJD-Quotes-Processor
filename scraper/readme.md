# Corpora Scraper Module
This module provides functionality for extracting the metadata and full texts of literature contained within
online corpora. The current corpora being processed are the [Library of Congress](https://loc.gov/),
[HathiTrust Digital Library](https://hathitrust.org/), [Online Library of Liberty](https://oll.libertyfund.org/),
and [Project Gutenberg](https://gutenberg.org/).

## Dependencies
- Python 3 and pip
- Working Internet connection
- MySQL set up on _localhost_
- Chrome web driver downloaded ([link](https://sites.google.com/a/chromium.org/chromedriver/))
- Project Gutenberg downloaded (see below)

## Downloading and Extracting Project Gutenberg
First, use this command to download the corpus in its entirety:

    `wget -w 2 -m -H "http://www.gutenberg.org/robot/harvest?filetypes[]=html&langs[]=en"`

Now we need to extract the zip files and relocate the HTML files to one directory.
First navigate to the directory that the download was stored in, then extract the zip files like so:

    `find . -name '*zip' -exec unzip -o {} -d ./extracted \;`
 
Then move the extracted HTML files to a localized directory:

    `mkdir html_files`
    `find . -name '*.htm*' -exec cp {} ./html_files \;`

## Set Up
Install [pipenv](https://pypi.org/project/pipenv/):

    `pip install pipenv`

(If the above command does not work, try passing the -U flag to pip)

Open a terminal in this project's directory, and install the rest
of the project's dependencies using pipenv:
    
    `pipenv install`

Start up MySQL and run these commands to create the required database and table:

    `CREATE DATABASE test;`
    `CREATE TABLE work_metadata(id int NOT NULL AUTO_INCREMENT, title VARCHAR(255) NOT NULL, author VARCHAR(255) NOT NULL, url TEXT NOT NULL, filepath TEXT NOT NULL, lccn VARCHAR(12) NOT NULL)`

Move the Chrome webdriver to your system path:
- Linux: move the downloaded file to ~/.local/bin
- Windows and Mac: see instructions [here](https://zwbetz.com/download-chromedriver-binary-and-add-to-your-path-for-automated-functional-testing/)

Create a file named '.env' and add the following lines to it:
    
    `USER="UCF_username"`
    `PASS="UCF_password"`
    `DB_USER="mysql_username"`
    `DB_PASS="mysql_password"`
    `DB_IP="database_ip"`
    `DB_DB="test"`

## Usage
Run the following command in the scraper/ directory

    `pipenv run python loc_scraper.py`

`loc_scraper.py` can be replaced with any of the `*_scraper.py` files.

## Testing
First ensure that the project's development dependencies are installed:

    `pipenv install --dev`

Then run the following command in the project directory:

    `pipenv run pytest`

