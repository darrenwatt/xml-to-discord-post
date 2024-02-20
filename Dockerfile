FROM python:3.8-alpine

RUN apk add gcc musl-dev libffi-dev \
&& pip install --upgrade pip

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD [ "python", "-u", "./main.py" ]
