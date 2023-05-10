FROM python:3.10-slim

WORKDIR /user/src/django_project
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip3 install --upgrade pip
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y


COPY ./requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /user/src/django_project

RUN adduser user
RUN chown -R user:user /user/src/django_project
USER user
EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]