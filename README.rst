Ojoalplato
==============================

Ojo al plato

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django


LICENSE: MIT


Settings
------------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Initial Migrations
^^^^^^^^^^^^^^^^^^

* First migrate **sites**, **auth** and **user** apps:

    $ python manage.py migrate users
    $ python manage.py migrate sites
    $ python manage.py migrate auth

* Then create default users **admin** and **paco**:

    $ python manage.py createsuperuser

* Finally run all migrations

    $ python manage.py migrate

Initial Setup
^^^^^^^^^^^^^

* Migrate mysql database::

    $ mysqldump wordpress  --default-character-set=latin1  -h localhost -u wordpress -p -r mysql.dump
    # Remove the SET NAMES='latin1' comment at the top of the dump.
    $ docker-compose build mysql
    $ docker-compose up -d mysql
    $ docker exec -it <container_id> bash
    root@<container_id>:# mysql -uojoalplato -p --default-character-set=utf8 wordpress
    mysql> SET names 'utf8';
    mysql> source mysql.dump;

* Clone models from mysql::

    $ docker-compose run django python manage.py clonemodels

* Move from ng-gallery to blog images::

    $ docker-compose run django python manage.py escapeng

* Load restaurant database::

    $ docker cp restaurant_with_coords.json <container_id>:/app/restaurant_with_coords.json
    $ docker-compose run django_ojoalplato python manage.py load_restaurants


Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ py.test


Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html




Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd ojoalplato
    celery -A ojoalplato.taskapp worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.





Email Server
^^^^^^^^^^^^

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server `MailHog`_ with a web interface is available as docker container.

.. _mailhog: https://github.com/mailhog/MailHog

Container mailhog will start automatically when you will run all docker containers.
Please check `cookiecutter-django Docker documentation`_ for more details how to start all containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to ``http://127.0.0.1:8025``





Sentry
^^^^^^

Sentry is an error logging aggregator service. You can sign up for a free account at  https://getsentry.com/signup/?code=cookiecutter  or download and host it yourself.
The system is setup with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.




Deployment
----------





Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html


