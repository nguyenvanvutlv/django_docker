from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

# models
from blog.models import Reporter
from django.contrib.auth.models import User



# Create your views here.
def home_blog(request):    
    
    # user_1 = User.objects.filter(username= "user_1")
    # reporter = Reporter.objects.filter(reporter_id= user_1[0])[0]
    # reporter.un_follow(id_reporter = "1")

    
    template = loader.get_template("blog/base.html")
    context = {
        "notification" : 1
    }
      
    return HttpResponse(template.render(context, request))


def article_blog(request):    
    
    template = loader.get_template("blog/Article.html")
    context = {
        "notification" : 1
    }
      
    return HttpResponse(template.render(context, request))