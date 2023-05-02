from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# for processing image
from django.core.files.base import ContentFile
import numpy as np
import cv2
import base64
from PIL import Image
from image_processing.models import ImageUpload
from image_processing.process import ProcessImage, Kmeans, Edges
from io import BytesIO
# for processing image

from .forms import UploadForm





from django.contrib.auth import authenticate, login, logout # for authen login
# from django.contrib.auth import logout
# Create your views here.






def login_function(request):

    
    if request.method == 'POST':
        # get username, password
        username = request.POST['Username']
        password = request.POST['Password']
        
        # check user login [Username, Password] from database
        user = authenticate(username= username, password= password)
        
        if user is not None: 
            # save sessionid to cookie about user
            login(request, user)
            return redirect('/')
            


    # when login faile or user access this website
    template = loader.get_template("images/login_imgp.html")
    context = {
        
    }
    return HttpResponse(template.render(context, request))       
    
    




def logout_function(request):
    logout(request)
    return redirect('/')







def change_brightness(origin, img, alpha, C):
    image = ProcessImage(origin).brightness(alpha, C)
    ret, frame_buff = cv2.imencode('.jpg', image)
    frame_b64 = base64.b64encode(frame_buff).decode('utf-8')
    return frame_b64


@login_required
def upload(request):       
    alert = False
    content = ""
    if request.method == "POST":
        submitted_form = UploadForm(request.POST, request.FILES)
        # return id user -> change to username
        user = request.session['_auth_user_id']
        username = User.objects.filter(id = user)[0].get_username()
        
        # get author has upload image
        Author = ImageUpload.objects.filter(author= str(username))
        if username == request.POST['author']:
            if len(Author) > 0:
                Author[0].delete()
            if submitted_form.is_valid():
                submitted_form.save()
        else:
            alert = True
            content = "False"
        
        
    template = loader.get_template("images/upload.html")
    context = {
        "alert" : alert,
        "content" : content
    }
      
    return HttpResponse(template.render(context, request))


@login_required
def home(request):    
    # print(request.session.keys())
    # print(request.session.items())  
    # request.session.set_expiry(60)  
    template = loader.get_template("images/base.html")
    context = {
        
    }
      
    return HttpResponse(template.render(context, request))


@login_required
def brightness(request):   
    # get current user are login this session
    user = request.session['_auth_user_id']
    username = User.objects.filter(id = user)[0].get_username()
    Author = ImageUpload.objects.filter(author= username)
    
    
    current_range = 0
    current_alpha = 1
    frame_b64 = ""
    is_image = False
    if request.method == "POST":
        current_range = int(request.POST['rangeValue_in'])
        current_alpha = int(request.POST['show_alpha'])
        
    if len(Author) > 0:
        # get image from database
        frame = cv2.imread(Author[0].origin.url[1:])
        frame = cv2.resize(frame, (512, 512))
        frame_b64 = change_brightness(frame, Author[0], current_alpha, current_range)
        is_image = True
    
    
    template = loader.get_template("images/brightness.html")    
    context = {
        "brightness" : frame_b64,
        "current_range" : current_range,
        "current_alpha" : current_alpha,
        "is_image"  : is_image
    }

    return HttpResponse(template.render(context, request))


@login_required
def edges(request):  
    
    # lấy tên người dùng ở phiên đăng nhập hiện tại
    user = request.session['_auth_user_id']
    username = User.objects.filter(id = user)[0].get_username()
    Author = ImageUpload.objects.filter(author= username)
    frame_b64 = ""
    frame = ""
    origin_image = ""
    is_image = False
    if len(Author) > 0:
        # get image from database
        frame = cv2.imread(Author[0].origin.url[1:])
        frame = cv2.resize(frame, (512, 512))
        origin_image = frame.copy()
        frame_b64 = Edges(frame).process()
        is_image = True
        
        
        _, frame_buff = cv2.imencode('.jpg', origin_image)
        origin_image = base64.b64encode(frame_buff).decode('utf-8')
        
         
         
    
    template = loader.get_template("images/edges.html")    
    context = {
        "origin_image" : origin_image,
        "frame_b64" : frame_b64,
        "is_image"  : is_image
    }
      
    return HttpResponse(template.render(context, request))



@login_required
def kmeans(request):    
    # get current user are login this session
    user = request.session['_auth_user_id']
    username = User.objects.filter(id = user)[0].get_username()
    Author = ImageUpload.objects.filter(author= username)
    # get image from database
    current_k = 1
    frame_b64 = ""
    is_image = False
    if request.method == "POST":
        current_k = int(request.POST['k_centroids'])
    
    if len(Author) > 0:
        frame = cv2.imread(Author[0].origin.url[1:])
        frame = cv2.resize(frame, (512, 512))
        frame_b64 = Kmeans(image= frame, k_centroids= current_k, theta= 500, types= 'RGB').changeBGR2frameb64()
        is_image = True
    
    
    template = loader.get_template("images/kmeans.html")    
    context = {
        "url_image" : frame_b64,
        "current_k" : current_k,
        "is_image"  : is_image
    }

    return HttpResponse(template.render(context, request))