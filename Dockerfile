FROM python:2

RUN mkdir /app
WORKDIR /app
ADD . /app

RUN apt-get update
RUN apt-get install -y telnet

RUN cp docker/logging.conf .
RUN pip install -r requirements.txt

CMD python router-monitor.py
