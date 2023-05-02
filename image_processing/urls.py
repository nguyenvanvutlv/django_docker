"""haui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views as img_p
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", img_p.home, name="session"),
    path("brightness/", img_p.brightness, name="brightness"),
    path("edges/", img_p.edges, name="edges"),
    path("kmeans/", img_p.kmeans, name="kmeans"),
    path("upload/", img_p.upload, name="upload"),
    path("login/", img_p.login_function, name="login_function"),
    path("logout/", img_p.logout_function, name="logout_function"),
    # path('logout/', auth_views.LogoutView.as_view(template_name='images/login_function.html'), name='logout'),
]
