# Blog cá nhân version 2.0.1

## Cơ sở dữ liệu 

Version 2.0.1: sử dụng sqlite3

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
Version 2.0.2: sử dụng MySQL

- Sẽ cấu hình MySQL[mysqlclient] ở docker

## Dự án Blog cá nhân

- Đăng nhập/Đăng kí [Done]

- Tạo bài viết, chỉnh sửa bài viết [Done]

- Xem bài viết [Done]

- Xoá bài viết