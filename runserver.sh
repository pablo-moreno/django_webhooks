#!/usr/bin/env bash

python manage.py collectstatic --settings=config.settings_prod --no-input && \
python manage.py migrate --settings=config.settings_prod && \
gunicorn -w 4 -t 180 -b 0.0.0.0:4567 config.wsgi