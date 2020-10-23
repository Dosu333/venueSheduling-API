#!/bin/sh


if ["$DATABASE"="postgres"]
then
    echo "Waiting for response"

    while !nc-z $DB_HOST $DB_PORT;
do
        sleep 0.1
    done
    
    echo "PostgreSQL Started!"

fi

python manage.py makemigrations --no-input
python manage.py migrate --no-input
exec "$@"

# echo "Waiting for postgres..."

# while ! nc -z db 5432; do
#   sleep 0.1
# done

# echo "PostgreSQL started"

# python manage.py flush --no-input
# python manage.py migrate
# python manage.py collectstatic --no-input --clear

# exec "$@"