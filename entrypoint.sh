#!bin

if ["$DATABASE"="postgres"]
then
    echo "Waiting for response"

    while !nc-z $DB_HOST $DB_PORT;
do
        sleep 0.1
    done
    
    echo "PostgreSQL Started!"

fi

python manage.py mkemigrations --no-input
python manage.py migrate --no-input
exec "$@"
