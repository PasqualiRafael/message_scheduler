#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting database..."
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done
    echo "Database ready!"
fi
python manage.py create_db
exec "$@"
