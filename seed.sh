#!/bin/bash

rm -rf dailybabyapi/migrations
rm db.sqlite3
python3 manage.py migrate
python3 manage.py makemigrations dailybabyapi
python3 manage.py migrate dailybabyapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata daily_users
python3 manage.py loaddata prompts
python3 manage.py loaddata relationships
python3 manage.py loaddata babies
python3 manage.py loaddata user_babies
python3 manage.py loaddata entries
python3 manage.py loaddata comments
python3 manage.py loaddata photos