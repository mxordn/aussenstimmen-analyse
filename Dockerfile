FROM python:3.10-slim-buster

WORKDIR /usr/src/app

RUN apt-get -y update \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential \
    && pip install uwsgi \
    && apt-get -y purge --auto-remove build-essential python3-dev

COPY ./app ./app
COPY requirements.txt .
COPY as3.ini .
COPY run.py .
COPY config.py .

RUN pip install -r requirements.txt

EXPOSE 8101
CMD [ "uwsgi", "as3.ini" ]