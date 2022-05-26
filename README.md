# assign-teacher
Assign teachers to educational establishment

Asignación de Docentes a Establecimientos Educativos: Un Enfoque Multi-objetivo

Horacio Villalba-Martí

# Data Set
To configure the data set used, perform the following tasks:
  * Install PostgreSQL
  * Create a user tfm with password Tfm123456 (Roles: Login and Create Database)
  * Create a database tfmdb (owner tfm)
  * Create a schame tfm (CREATE SCHEMA tfm AUTHORIZATION tfm;)
  * Connect with the user created
  * run the input/script.sql file

# Run the algorithm

* Install Python

Install Python dependencies

* pip install -U pymoo
* pip install geopy
* pip install psycopg2

py src/assignTeacher.py
