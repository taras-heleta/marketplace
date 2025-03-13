<h1 align="center">Hi, This's backend part of the website "Marketplace" 
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>

## Table of contents
* [General info](#general-info)
* [Project Status](#project-Status)
* [Technologies](#technologies)
* [Setup](#setup)
* [Screenshots](#screenshots)


## Link to website
Todo

## General info

* The project is a website "Marketplace". 
* This website project aims to provide a smooth and intuitive user experience for buying and selling items online. 
* This is a backend part website. Frontend part: https://github.com/KaratSergio/Market
	
## Technologies
Project is created with:
asgiref==3.8.1
Django==5.1.6
psycopg==3.2.4
psycopg-binary==3.2.4
sqlparse==0.5.3

<details><summary>Other Technologies (CLICK ME)</summary>
<ul>
<li>example</li>
</ul>
</details>

## Setup
1. install python 13.0.2.
2. install postgres 17.2.
3. In postgres:
   1. create role marketplace_admin
   2. create datebase marketplace_db
4. create folder for marketplace.
5. In terminal:
   1. python3 -m venv python3_13
   2. git clone https://github.com/Oskorbin-work/marketplace.git
   3. cd marketplace/core
6. create file "secret.py" (path – app "core"). Write to file (!!!!!!YOU MUST USE YOUR PASSWORDS!!!!!):
```python
# config settings.py
SECRET_KEY = YOU_secret_key_DJANGO
# postgresql
DB_ENGINE = 'django.db.backends.postgresql'
DB_NAME = 'marketplace_db'
DB_USER = 'marketplace_admin'
DB_PASSWORD = YOU_PASSWORD
DB_HOST = '127.0.0.1'
DB_PORT = '5432'
```
5. python manage.py makemigrations
6. python manage.py migrate
7. python manage.py runserver

# Screenshots
Todo

## Project Status
<i>In development</i>

