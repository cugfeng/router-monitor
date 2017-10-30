FROM python:2

RUN mkdir /app
WORKDIR /app
ADD . /app

RUN cp docker/logging.conf .
RUN pip install -r requirements.txt

CMD python router-monitor.py
