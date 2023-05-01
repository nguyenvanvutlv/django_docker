FROM python:alpine3.17

WORKDIR /django_project

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add gcc
RUN pip3 install --upgrade pip
RUN pip3 install --extra-index-url https://alpine-wheels.github.io/index numpy
RUN pip3 install --extra-index-url https://alpine-wheels.github.io/index opencv-python

# install dependencies
RUN pip install --upgrade pip 
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt


COPY . /django_project

RUN adduser -D user
USER user

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]