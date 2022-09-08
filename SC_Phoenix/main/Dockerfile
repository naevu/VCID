FROM python:3.9.13-slim

ENV APP_HOME=/app
WORKDIR $APP_HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
	apt-get install -y gcc

COPY ./static ./static
COPY ./templates ./templates
COPY /home/naveen_n/VCID/SC_Phoenix/run.py .
COPY ./requirements.txt .

RUN pip install -r requirements.txt
