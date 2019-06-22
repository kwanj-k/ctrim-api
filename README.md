[![Build Status](https://travis-ci.com/kwanj-k/ctrim-api.svg?branch=master)](https://travis-ci.com/kwanj-k/ctrim-api) [![![Coverage Status][![Coverage Status](https://coveralls.io/repos/github/kwanj-k/ctrim-api/badge.svg)](https://coveralls.io/github/kwanj-k/ctrim-api)
## Getting started
These instructions will get you a copy of the project up and running in your local machine for development and testing purposes.

## Prerequisites
- [Git](https://git-scm.com/download/)
- [Python 3.6 and above](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/)


## Installing
### Setting up the database
- Start your database server and create your database

### Setting up and Activating a Virtual Environment
- Create a working space in your local machine
- Clone this [repository](https://github.com/kwanj-k/ctrim-api.git) `git clone https://github.com/kwanj-k/ctrim-api.git`
- Navigate to the project directory
- Create a virtual environment `python3 -m venv name_of_your_virtual_environment`
- Create a .env file and put these key=values in it:
```
source name_of_your_virtual_environment/bin/activate
source venv/bin/activate
export DB_NAME="your_db_name"
export DB_USER="your_postgres_username"
export DB_PASS="your_postgres_password"
export DB_HOST="localhost or any other host name"
export DB_PORT="port_number"
```
- Load the environment variable `source .env`
- Install dependencies to your virtual environment `pip install -r requirements.txt`
- Migrate changes to the newly created database `python manage.py makemigrations` then `python manage.py migrate`

## Starting the server
- Ensure you are in the project directory on the same level with `manage.py` and the virtual environment is activated
- Run the server `python manage.py runserver`


## Run Tests
-Run your tests `pytest --cov-report term-missing --cov=apps -p no:warnings`

## API Spec
