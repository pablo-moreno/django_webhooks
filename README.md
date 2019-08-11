# Django Webhooks

[![Build Status](https://travis-ci.com/pablo-moreno/django_webhooks.svg?branch=master)](https://travis-ci.com/pablo-moreno/django_webhooks)
[![CircleCI](https://circleci.com/gh/pablo-moreno/django_webhooks.svg?style=svg)](https://circleci.com/gh/pablo-moreno/django_webhooks)


Django application to perform automatic application deploys using Github Webhooks.

## Requirements

```bash
python3
```

## Setup project

Clone the repo:
```bash
git clone https://github.com/pablo-moreno/github_webhooks.git
```

Create .env file and setup your environment variables:
```bash
cp env.example .env
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Make initial migration to create database:
```bash
python manage.py migrate
```

Run server (with gunicorn)
```bash
sh runserver.sh
```

Development:
```bash
python manage.py runserver
```

## Github

Follow this [instructions](https://developer.github.com/webhooks/creating/) to setup yor Github project with webhooks, pointing to your server.
