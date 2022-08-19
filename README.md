# Job Vacancy Database

## Overview
This is an academic project of Database Management System which is taught in the sixth semester of Bachelor's Degree in Tribhuvan University. This project has been written with Django as the backend framework and PostgreSQL as the database management system and HTML, CSS and vanilla JavaScript in the frontend.

## Installation Instructions

### Dependencies
PostgreSQL is required for running this project, you can install PostgreSQL for your appropriate operating system family from [here](https://www.postgresql.org/download/). The basic setup required for the database server to be running in your machine can be followed from the [PostgreSQL documentation](https://www.postgresql.org/docs/) of the appropriate version. The version used for this project is PostgreSQl v13, which is recommended.

This project uses `python` libraries, therefore creating a separate virtual environment using the native `venv` module or using a package management system such as `conda` is recommended. For installing the dependencies of the project, the following command must be executed in a terminal. (For those using virtual environment, all the commands must be executed after activating the virtual environment)
```
$ pip install -r requirements.txt
```

### Setup
Firstly, login to the PostgreSQL shell and create a new database named **jobcv** in your machine using the following command.
```
postgres=# CREATE DATABASE jobcv; 
```
Django requires the username and password for the user accessing the database. Creating a new user for the database is recommended to isolate the permissions. Therefore, create a new user and give permissions to access the newly created database **jobcv** using the following commands. The alterations of role are [recommended by Django](https://docs.djangoproject.com/en/3.1/ref/databases/#optimizing-postgresql-s-configuration) for optimizing PostgreSQL's configuration.

```
postgres=# CREATE USER jobcv WITH PASSWORD 'jobcvdatabase';
postgres=# ALTER ROLE jobcv SET client_encoding TO 'utf8';
postgres=# ALTER ROLE jobcv SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE jobcv SET timezone TO 'UTC';
```
You can use your own name for database and user but you will have to change the corresponding configurations in the file `db.json` as well.

### Database Dump
The file `address.psql` contains the insertion in the address table of the database. This file populates the tables related to address (which is always fixed) of the users and leaves all the other tables blank. Therefore, at least importing the records from this file is recommended. If you require some sample data on all the tables, then it can be imported from the file `sample-data.psql`. Execute the following command as the PostgreSQL default user according to your requirement to import the data.
```
$ psql jobcv < address.psql
```
OR
```
$ psql jobcv < sample-data.psql
```
If you want an empty database without any records, then you can execute the following commands
```
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py shell
>>> from records.models import Admin
>>> admin = Admin(username='admin', password='admin')
>>> admin.save()
```
By this point, now you have a new database along with its user created and you have an account to access the admin panel. The credentials of the account to access the admin panel is
```
username: admin
password: admin
```

## Running the Project
If you executed all the installation commands without any errors, the project is ready to be served from the `localhost`. Execute this command in the terminal.
```
$ python manage.py runserver
```
Now, the portal can be accessed from\
http://localhost:8000

Similarly, the admin panel can be accessed from\
http://localhost:8000/admin
