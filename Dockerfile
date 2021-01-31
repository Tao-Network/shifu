FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV DOCKER_CONTAINER 1

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

COPY manage.py /code/manage.py
COPY web /code/
COPY sql /code/
COPY shifu /code/
COPY json /code/
COPY abis /code/
WORKDIR /code/