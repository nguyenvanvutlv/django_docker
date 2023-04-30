# django_docker

edit

# step-by-step to use this project

- clone project
```
$ git clone https://github.com/nguyenvanvutlv/django_docker.git
$ cd django_docker
```


- create database, this project use MySQL

```
CREATE SCHEMA `haui_project` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;

```
haui_project, you can change it in settings.py


- create env from file yml
```
$ [mamba or conda] docker create -f log.yml
```

- run server : 
```
python manage.py runserver
```

this command is run on 127.0.0.1:8000, to change port, add port after
command runserver like this

```
python manage.py runserver [your port]
```

- account admin: root/root


you can create account by admin