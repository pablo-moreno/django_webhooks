#!/usr/bin/env bash

python manage.py collectstatic --settings=config.settings_prod --no-input && \
python manage.py migrate --settings=config.settings_prod && \
gunicorn -c gunicornconfig.py config.wsgi