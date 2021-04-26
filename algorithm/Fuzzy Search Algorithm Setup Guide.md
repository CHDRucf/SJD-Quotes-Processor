# Fuzzy Search Algorithm Setup Guide

## Setup Steps
1. Export the project database to a .sql file using PHPMyAdmin
(not needed if running directly on the UCF dev server)
2. Transfer the the db export file to the server that the
algorithm will be running on
   - This will take a while
   - Again, not needed if running the program on the UCF dev server
3. SSH into the server and run the following commands:
```bash
# Install Python3.8
sudo apt update
sudo apt -y install python3.8
sudo apt -y install python3-distutils
sudo apt -y install python3-apt
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.8 get-pip.py
python3.8 -m pip install --upgrade pip
python3.8 -m pip install pipenv

# Install MySQL 8 - Not needed if running on UCF dev server
wget https://dev.mysql.com/get/mysql-apt-config_0.8.16-1_all.deb
sudo dpkg -i mysql-apt-config_0.8.16-1_all.deb
# choose ok
sudo apt-get update
sudo apt -y install mysql-client mysql-community-server mysql-server
# set password to root, select ok

# Set up database - Not needed if running on UCF dev server
mysql -u root --password=root
create database SJDquotes;
create user 'sjd_quotes'@'localhost' identified by 'SJDquotes2020';
GRANT ALL PRIVILEGES ON SJDquotes.* TO 'sjd_quotes'@'localhost';
flush privileges;
exit;
mysql -D SJDquotes -u sjd_quotes --password=SJDquotes2020
source SJDquotes.sql;
# this will take a little while to load but not too long
exit;

# Set up project repo
sudo apt -y install git
git clone https://github.com/ucfcs/fall2020_group2.git
# Enter login credentials to clone the project repo
cd fall2020_group2/algorithm
git checkout algorithm
wget https://files.pythonhosted.org/packages/4e/84/b1942b3bf4fb822af9cf9ca72d625745f5dbbfb90a3c48b334b00a1e9afb/rapidfuzz-1.3.3-cp38-cp38-manylinux1_x86_64.whl
python3.8 -m pip install rapidfuzz-1.3.3-cp38-cp38-manylinux1_x86_64.whl
pipenv install --dev
# Errors may appear when installing python-levenshtein - These can be ignored
```
4. With SSH still open, WinSCP (if on Windows) or SCP (if on Linux) the corpora
into the algorithm directory
   - This will take several hours
   - Again, this is not necessary on the UCF dev server as the corpora
   is installed to Christopher Melton's home directory (cmelton)

5. Run these commands on the server:
```bash
nano .env
```

Paste the following into the file:
```
DB_USER=sjd_quotes
DB_PASS=SJDquotes2020
DB_HOST=127.0.0.1
DB_DB=SJDquotes
DB_PORT=3306

SSH_HOST=10.173.204.216
SSH_PORT=22
SSH_USER="user"
SSH_PASS="pass"
_REMOTE_BIND_ADDRESS=127.0.0.1
_REMOTE_MYSQL_PORT=3306
```
_Note that the ssh info does not matter since we will be connecting to our
own local copy of the database, and not using ssh_

Save and exit the file.

6. There are two ways to run the algorithm.
   1) Perform the automated quick search. Using this method, the algorithm will
   attempt to search for quotes only in works written by the authors the quotes
   were attributed to by SJD. This is orders of magnitude faster than
   searching for each quote across the entire corpora, but will not return
   matches whose score does not meet the threshold value (currently 53).
   To perform this search, run the following command, being sure to replace the
   placeholder values in all capital letters with the correct values:

   ```bash
   nohup pipenv run python main.py --search-quick-lookup --no-manual-quick-lookup --write-to-json --no-write-to-database --no-use-ssh-tunnelling --num-processes=16 --chunk-size=16 --corpora-path="PATH_TO_CORPORA_DIRECTORY" &
   ```

   2) Search for a specific set of quotes over the entire corpora. This is
   much slower, but is guaranteed to return matches. To run this search, first
   create a JSON file in the algorithm directory. Populate this file with a
   single array of numbers. These numbers are the IDs of the quotes in the
   database that you would like the algorithm to search for over all the
   corpora. For instance, if you wanted to search for the quotes with the
   database IDs of 2, 821, and 22203, the file you would place in the algorithm
   directory would look like this:
   ```JSON
   [
      2,
      821,
      22203
   ]
   ```
   After the file is created, run the the following command, being sure to
   replace the placeholder values in all capital letters with the
   correct values:
   ```bash
   nohup pipenv run python main.py --perform-search --no-search-quick-lookup --corpora-path="PATH_TO_CORPORA_DIRECTORY" --quote-ids-filepath="FAILED_QUOTES_FILENAME" --write-to-json --no-write-to-database --no-use-ssh-tunnelling --num-processes=16 --chunk-size=128 &
   ```

7. The algorithm should now be running.
Run the following command in the project directory to check its progress:
```bash
clear ; ps -e | grep "python$" ; tail nohup.out
```

8. Once the algorithm is finished, copy the resulting matches.json file onto
the UCF dev server and run the following command in the project directory
to write the results to the database.
Be sure to replace the placeholder values in all capital letters
with the correct values:
```bash
pipenv run python main.py --no-perform-search --no-write-to-json --write-to-database --no-use-ssh-tunnelling --corpora-path="PATH_TO_CORPORA_DIRECTORY"
```
