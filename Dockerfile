FROM python:3.11-alpine3.21

COPY requirements.txt /temp/requirements.txt
COPY ./src /src

WORKDIR /src

RUN pip install -r /temp/requirements.txt

EXPOSE 8000
