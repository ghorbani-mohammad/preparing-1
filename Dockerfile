FROM python:3.10-alpine
RUN apk add build-base postgresql-dev python3-dev libpq

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt