FROM python:3.11-alpine3.21

RUN apk add postgresql-client build-base postgresql-dev

COPY requirements.txt /temp/requirements.txt
COPY ./src /src

WORKDIR /src

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user

USER service-user

EXPOSE 8000
