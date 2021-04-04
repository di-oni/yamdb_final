FROM python:3.8.5

WORKDIR /code

RUN apt update && apt upgrade 

COPY . /code

RUN pip install -r requirements.txt

CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000