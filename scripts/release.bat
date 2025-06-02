@echo off
REM This script is used to populate the database with initial data
REM It should be run after deploying to Heroku

echo Running database migrations...
python manage.py migrate

echo Populating historical periods...
python manage.py populate_periods

echo Populating Greek content...
python manage.py populate_greek_content

echo Populating Roman content...
python manage.py populate_roman_content

echo Populating Middle Ages content...
python manage.py populate_middle_ages_content

echo Database population complete!