#!/bin/sh

# Do not touch
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Clean the database and remove all tables
python manage.py flush --noinput


# Generate new database tables
python manage.py migrate

# Generate static files
python manage.py collectstatic --noinput

# Generate superuser
export DJANGO_SUPERUSER_PASSWORD="password"
export DJANGO_SUPERUSER_USERNAME="admin"
export DJANGO_SUPERUSER_EMAIL="testmail@example.com"
python manage.py createsuperuser --noinput


exec "$@"