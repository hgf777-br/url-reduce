release: python manage.py migrate --noinput
release: python manage.py loaddata url/fixtures/db.json
web: gunicorn url.wsgi --log-file -