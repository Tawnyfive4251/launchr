FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# copy the entrypoint script
COPY ./docker/app/shared/entrypoint.sh /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
RUN apt-get install -y swig
RUN apt-get install -y libasound2-dev
# Requirements are installed here to ensure they will be cached.
RUN apt-get install -y python-dev bison autoconf libtool-bin libpulse-dev
COPY ./requirements /requirements
RUN pip install -r /requirements/dev.txt
RUN apt-get install -y rabbitmq-server

#install ffmpeg


WORKDIR /app
ENTRYPOINT ["/entrypoint"]
