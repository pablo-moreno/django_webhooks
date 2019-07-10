#!/usr/bin/env bash

gunicorn -w 4 -t 180 -b 0.0.0.0:4567 github_webhooks.wsgi