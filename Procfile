web: gunicorn manage:app
release: python manage.py db migrate
release: python manage.py db upgrade