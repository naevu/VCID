FROM python:3.8

ENV HOST 0.0.0.0
WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 5000

CMD [ "python3", "run.py" ]
