The Wildlife Transfer Parameter Database Upgrade Project

The Wildlife Transfer Parameter (WTP) is a Django-based web application designed to manage and visualise radioactivity data on wildlife. This README provides instructions on setting up the project locally.


Prerequisites
Before you begin, ensure the wtp file is unzipped and you have the following installed on your system:

Python 3.6 or higher
PostgreSQL - from postgresql.org
pip (Python package installer)
Django - 'pip install django'


1. Setting Up the Virtual Environment and Dependencies
In the project directory, run to create virtual environment:
python -m venv wtp_env

Activate virtual environment:
.\wtp_env\Scripts\activate


2. Install Required Packages:
When the virtual environment is activated, install all necessary packages listed in requirements.txt through:
pip install -r requirements.txt


3. Setting Up PostgreSQL
To create the database, open through the command prompt the PostgreSQL command line:
psql -D postgres

This requires knowledge ot the password from the PostgreSQL installation.

Then, set up the user and database by running all those:
CREATE DATABASE wtp_db;
CREATE USER wtp_user WITH PASSWORD 'wtp_P4$$';
ALTER ROLE wtp_user SET client_encoding TO 'utf8';
ALTER ROLE wtp_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE wtp_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE wtp_db TO wtp_user;
GRANT USAGE, CREATE ON SCHEMA public TO wtp_user;
ALTER DATABASE wtp_db OWNER TO wtp_user;

If you use a different username or password, you need to change this in the database connection information in _wtp/settings.py.


4. Database Migrations
Django knows the database schema (in data_app/models.py). Migrate the database schema to PostgreSQL:
python manage.py makemigrations
python manage.py migrate


5. Testing the Installation
Start the Django development server to test if everything is set up correctly:
python manage.py runserver

Make sure PostgreSQL is running:
pg_ctl -D "C:\Program Files\PostgreSQL\16\data" restart

Access the Application:
Open a browser and go to http://127.0.0.1:8000/ to view the application.

