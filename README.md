# Ojoalplato

Blog de Gastronomía y Vinos

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Initial Migrations

- First migrate **sites**, **auth** and **user** apps:

    $ python manage.py migrate users
    $ python manage.py migrate sites
    $ python manage.py migrate auth

### Setting Up Your Users

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.


- Finally run all migrations

    $ python manage.py migrate

### Initial Setup

Migrate mysql database:

    $ mysqldump wordpress  --default-character-set=latin1  -h localhost -u wordpress -p -r mysql.dump
    Remove the SET NAMES='latin1' comment at the top of the dump.
    $ docker-compose build mysql
    $ docker-compose up -d mysql
    $ docker exec -it <container_id> bash
    root@<container_id>:# mysql -uojoalplato -p --default-character-set=utf8 wordpress
    mysql> SET names 'utf8';
    mysql> source mysql.dump;

Clone models from mysql:

    $ docker-compose run django python manage.py clonemodels

Move from ng-gallery to blog images:

    $ docker-compose run django python manage.py escapeng

Load restaurant database:

    $ docker cp restaurant_with_coords.json <container_id>:/app/restaurant_with_coords.json
    $ docker-compose run django_ojoalplato python manage.py load_restaurants



### Type checks

Running type checks with mypy:

    $ mypy ojoalplato

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd ojoalplato
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd ojoalplato
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd ojoalplato
celery -A config.celery_app worker -B -l info
```

### Email Server

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server [Mailpit](https://github.com/axllent/mailpit) with a web interface is available as docker container.

Container mailpit will start automatically when you will run all docker containers.
Please check [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html) for more details how to start all containers.

With Mailpit running, to view messages that are sent by your application, open your browser and go to `http://127.0.0.1:8025`

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
