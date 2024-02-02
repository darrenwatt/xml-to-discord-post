#FROM python:3.6-alpine
FROM python:3.7

RUN /bin/sh -c pip install -r requirements.txt
COPY requirements.txt /
COPY main.py /
COPY bluesky.py /
COPY config.py /

RUN pip install -r requirements.txt

CMD [ "python", "-u", "./main.py" ]
