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
from image_processing.process import ProcessImage, Kmeans
from io import BytesIO
# for processing image





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
    image = ProcessImage(origin, img.types).brightness(alpha, C)
    ret, frame_buff = cv2.imencode('.jpg', image)
    frame_b64 = base64.b64encode(frame_buff).decode('utf-8')
    return frame_b64


@login_required
def upload(request):       
    template = loader.get_template("images/upload.html")
    context = {
        "form" : 1
    }
      
    return HttpResponse(template.render(context, request))


@login_required
def home(request):    
    print(request.session.keys())
    print(request.session.items())  
    # request.session.set_expiry(60)  
    template = loader.get_template("images/base.html")
    context = {
        
    }
      
    return HttpResponse(template.render(context, request))


@login_required
def brightness(request):   
    user = request.session['_auth_user_id']
    users = User.objects.filter(id = user)
    if len(users) > 0:
        user = users[0].get_username()
        
        img = ImageUpload.objects.filter(author=user)[0]
        
        frame = cv2.imread(img.origin.url[1:])
        # frame = frame.astype(np.int16)
        frame_b64 = change_brightness(frame, img, 1, 0)

        
        current_value_range = 0
        current_alpha = 1
        
        if request.method == "POST":
            current_value_range = int(request.POST['rangeValue_in'])
            current_alpha = int(request.POST['alpha'])
            frame_b64 = change_brightness(frame, img, current_alpha, current_value_range)
        


    template = loader.get_template("images/brightness.html")    

    context = {
        "brightness" : frame_b64,
        "current_range" : current_value_range,
        "current_alpha" : current_alpha
    }
    print(- np.max(frame))
    return HttpResponse(template.render(context, request))


@login_required
def contrast(request):       
    template = loader.get_template("images/contrast.html")    
    context = {
        
    }
      
    return HttpResponse(template.render(context, request))



@login_required
def kmeans(request):    
    # get current user are login this session
    user = request.session['_auth_user_id']
    username = User.objects.filter(id = user)[0].get_username()
    Author = ImageUpload.objects.filter(author= username)[0]
    # get image from database
    current_k = 1
    if request.method == "POST":
        current_k = int(request.POST['k_centroids'])
    
    
    frame = cv2.imread(Author.origin.url[1:])
    frame = cv2.resize(frame, (512, 512))
    frame_b64 = Kmeans(image= frame, k_centroids= current_k, theta= 500, types= 'RGB').changeBGR2frameb64()
    
    
    template = loader.get_template("images/kmeans.html")    
    context = {
        "url_image" : frame_b64,
        "current_k" : current_k
    }

    return HttpResponse(template.render(context, request))