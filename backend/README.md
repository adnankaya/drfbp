
## Docker Compose
```
docker compose up -d --build 
```
## Installations

```bash
# clone the project
git clone https://github.com/adnankaya/drfbp.git
# go to project directory
cd drfbp
# create venv instance named as env
python3.11 -m venv venv
# for linux/macos users
source venv/bin/activate
# for windows users
.\venv\Scripts\activate
# install packages
pip install -r requirements.txt
# DOCKER
# docker exec -it postgres-drfbp psql -U dbuser
# create database db_drfbp;
# Migrate files
python manage.py migrate
# [Optional] make migrations if necessary
python manage.py makemigrations <app-name>
python manage.py migrate
# init all command
python manage.py init_all
# DEBUG is True
python manage.py init_users

# run project for development mode
python manage.py runserver --settings=src.settings.dev
# run project for production mode
python manage.py runserver --settings=src.settings.prod
# run project for test mode
python manage.py runserver --settings=src.settings.settings_for_test
```
## Static Files
```
python manage.py collectstatic
```

## Internationalization
```
python manage.py makemessages --all --ignore=venv
python manage.py compilemessages
```

---


## Technical Notes

1. Find and remove migration files
```bash

find . -path "*/migrations/*.py" -not -path "./venv/*" -not -name "__init__.py" -delete

```

## Load Test
```bash
# run gunicorn with 4 workers
gunicorn core.wsgi:application -w 4

# new terminal apache bench
ab -n 100 -c 10 http://127.0.0.1:8000/
# This will simulate 100 connections over 10 concurrent threads. That's 100 requests, 10 at a time.
```