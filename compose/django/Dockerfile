FROM python:3.5

ENV PYTHONUNBUFFERED 1

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements

# Install spatialite
RUN apt-get update && apt-get install --no-install-recommends -y \
	gettext spatialite-bin libsqlite3-dev gdal-bin libgdal-dev python3-gdal \
	&& rm -rf /var/lib/apt/lists/*

RUN pip install -r /requirements/production.txt \
    && groupadd -r django \
    && useradd -r -g django django

COPY . /app
RUN chown -R django /app

COPY ./compose/django/gunicorn.sh /gunicorn.sh
COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh \
    && sed -i 's/\r//' /gunicorn.sh \
    && chmod +x /entrypoint.sh \
    && chown django /entrypoint.sh \
    && chmod +x /gunicorn.sh \
    && chown django /gunicorn.sh \
    && mkdir -m 777 /staticfiles \
    && mkdir -p /media \
    && chmod -R 770 /media

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
