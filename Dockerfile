#
FROM python:3.11.2-slim-buster

#
WORKDIR /usr/src/app

#
COPY ./requirements.txt /usr/src/requirements.txt

RUN pip install --upgrade pip

#
RUN pip install -r /usr/src/requirements.txt

#
COPY ./app /usr/src/app

