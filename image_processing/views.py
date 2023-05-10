from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

from blog.models import Groups_User, Reporter


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

from .forms import UploadForm





from django.contrib.auth import authenticate, login, logout # for authen login
# from django.contrib.auth import logout
# Create your views here.

def process_name(name: str):
    try:
        name = name.strip()
        name = name.split()
        first, last = " ".join(name[:-1]), name[-1]
    except Exception as error:
        return (False, error)
    # print(first, last)
    return first, last



def register(request):
    errors = None
    if request.method == "POST":
        # print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        rpassword = request.POST['rpassword']
        name = request.POST['name']
        email = request.POST['email']
        
        phone = request.POST['phone']
        address = request.POST['address']
        company = request.POST['company']
        gender = request.POST['gender']
        # print(phone, address, company, gender)
        
        
        if rpassword == password:
            pass
        else:
            errors = "Mật khẩu nhập lại không đúng"
        
        first_result, last_result = process_name(name)
        if first_result != False:
            try:
                _users = User(username= username,
                        email= email, 
                        first_name= last_result,
                        last_name= first_result)
                _users.set_password(raw_password= password)
                _users.save()
                new_userblog = Groups_User(user= _users, group_name= "blog")
                new_userblog.save()
                
                
                new_reporter = Reporter(reporter_id= _users,
                                        gender= gender,
                                        phone_number= phone,
                                        address= address,
                                        company= company)
                new_reporter.save()
                errors = True
                
            except Exception as error:
                errors = error
        else:
            errors = "Tên không đúng"
    template = loader.get_template("images/register.html")
    context = {
        "errors": errors
    }
    return HttpResponse(template.render(context, request)) 


def login_function(request):
    
    error = False
    if request.method == 'POST':
        # get username, password
        username = request.POST['Username']
        password = request.POST['Password']
        
        # check user login [Username, Password] from database
        user = authenticate(username= username, password= password)
        # print(user)
        if user is not None: 
            # save sessionid to cookie about user
            login(request, user)
            groups_user = Groups_User.objects.filter(user= user)[0]
            # print(groups_user)
            if groups_user.group_name != "image_processing":
                return redirect("/" + groups_user.group_name + "/")
            elif groups_user.group_name == "image_processing":
                return redirect('/')
        else:
            error = True


    # when login faile or user access this website
    template = loader.get_template("images/login_imgp.html")
    context = {
        "errors" : error
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
    user = request.session['_auth_user_id']
    user = User.objects.filter(id = user)[0]  
    groups = Groups_User.objects.filter(user= user)[0]
    if groups.group_name != "image_processing":
        redirect("/" + groups.group_name + "/")  
    alert = False
    content = ""
    if request.method == "POST":
        submitted_form = UploadForm(request.POST, request.FILES)
        # print(request.FILES)
        # print(request.POST)
        # print(submitted_form)
        # submitted_form.fields['author'] = 'root'
        user = request.session['_auth_user_id']
        username = User.objects.filter(id = user)[0].get_username()
        # print("USERNAME: ", username)
        # print("AUTHOR, ", request.POST['author'])
        if username == request.POST['author']:
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
    user = request.session['_auth_user_id']
    user = User.objects.filter(id = user)[0]  
    groups = Groups_User.objects.filter(user= user)[0]
    if groups.group_name != "image_processing":
        return redirect("/" + groups.group_name + "/")  
    # print(request.session.keys())
    # print(request.session.items())  
    # request.session.set_expiry(60)  
    template = loader.get_template("images/base.html")
    context = {
        
    }
      
    return HttpResponse(template.render(context, request))


@login_required
def brightness(request):   
    user = request.session['_auth_user_id']
    user = User.objects.filter(id = user)[0]  
    groups = Groups_User.objects.filter(user= user)[0]
    if groups.group_name != "image_processing":
        return redirect("/" + groups.group_name + "/") 
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
        if frame is not None:
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
def contrast(request): 
    user = request.session['_auth_user_id']
    user = User.objects.filter(id = user)[0]  
    groups = Groups_User.objects.filter(user= user)[0]
    if groups.group_name != "image_processing":
        return redirect("/" + groups.group_name + "/")       
    template = loader.get_template("images/contrast.html")    
    context = {
        
    }
      
    return HttpResponse(template.render(context, request))



@login_required
def kmeans(request):  
    user = request.session['_auth_user_id']
    user = User.objects.filter(id = user)[0]  
    groups = Groups_User.objects.filter(user= user)[0]
    if groups.group_name != "image_processing":
        return redirect("/" + groups.group_name + "/")   
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
        if frame is not None:
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