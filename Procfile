release: python manage.py migrate --noinput
web: daphne ghp_message.asgi:application --port $PORT --bind 0.0.0.0
