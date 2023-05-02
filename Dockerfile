FROM python:3.10-slim

WORKDIR /user/src/django_project
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
COPY ./requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /user/src/django_project
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]


# FROM python:alpine3.17

# WORKDIR /usr/src/django_project

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# RUN apk update
# RUN pip3 install --upgrade pip

# RUN apk add --no-cache --virtual .build-deps gcc g++ build-base freetype-dev libpng-dev openblas-dev py3-scipy
# RUN pip3 install numpy scipy

# RUN pip3 install --extra-index-url https://alpine-wheels.github.io/index numpy
# RUN pip3 install --extra-index-url https://alpine-wheels.github.io/index opencv-python
# RUN pip3 install --extra-index-url https://alpine-wheels.github.io/index Pillow

# # install dependencies
# RUN pip3 install --upgrade pip 
# COPY ./requirements.txt /requirements.txt
# RUN pip3 install --no-cache-dir -r /requirements.txt


# COPY . /django_project

# RUN adduser -D user
# RUN chown -R user:user /usr/src/django_project
# # USER user
# EXPOSE 8000

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]