# Dự án Django_docker


## Cách chạy dự án
### Chạy dự án từ github

``` bash
# clone github về máy
(env) $ git clone https://github.com/nguyenvanvutlv/django_docker.git
(env) $ cd django_docker
```

``` bash
# cài đặt thư viện từ file requirements.txt
(env) $ pip install -r requirements.txt
```

``` bash
# chạy lệnh thực thi trên cơ sở dữ liệu
(env) $ python manage.py makemigrations
(env) $ python manage.py migrate
```

``` bash
# chạy dự án
(env) $ python manage.py runserver [mặc định: 127.0.0.0:8000]
```


### Chạy dự án từ docker

- Yêu cầu máy có docker, cài đặt tại đây [Docker](https://www.docker.com/)

``` bash
# Kéo docker container về máy
$ docker pull toilavu/app:django_project
```

``` bash
# chạy images
$ docker run -dp 8000:8000 toilavu/app:django_project
$ docker run toilavu/app:django_project
```
- truy cập http://localhost:8000/


-----------------------------------------------------

## Database (Cơ sở dữ liệu)

### version 1: 2/5/2023

- Sử dụng sqlite3 được hỗ trợ sẵn từ django
``` python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### version 2: update dự kiến sẽ dùng MySQL

``` python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "haui_project",
        "USER": "root",
        "PASSWORD": "root",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}
```

---------------------------------------

## Dự án

### Image_processing (Xử lý ảnh cơ bản)

- Tăng giảm độ sáng
- Tìm biên bằng ngưỡng tự động và sobel kernel
- Phân vùng ảnh (Kmeans)

Các chương trình này nằm trong file [process.py](image_processing/process.py) ở thư mục image_processing, các thư viện dùng trong phần này đó là:

- Pillow, opencv-python: đọc ảnh
- numpy, scipy: tính toán các phép tính trên ma trận, vector
- base64: dùng để hiển thị ảnh trên website

```
Các hàm được viết thủ công chỉ dùng thư viện tính toán
```


### Machine_learning [Update]