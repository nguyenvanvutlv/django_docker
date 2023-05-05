from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

# models
from blog.models import Reporter, Article
from django.contrib.auth.models import User



class HomeView(ListView):
    model = Article
    template_name = "blog/index.html"
    context_object_name = "articles"
    # paginate_by = 2






# Create your views here.
def home_blog(request):    
    
    # user_1 = User.objects.filter(username= "user_1")
    # reporter = Reporter.objects.filter(reporter_id= user_1[0])[0]
    # reporter.un_follow(id_reporter = "1")

    
    template = loader.get_template("blog/index.html")
    context = {
        "notification" : 1
    }
      
    return HttpResponse(template.render(context, request))


def article_blog(request):    
    
    
    objects = Article.objects.all()
    # print(objects)
    
    template = loader.get_template("blog/Article.html")
    context = {
        "objects" : objects
    }
      
    return HttpResponse(template.render(context, request))

def article_blogid(request, article_id):    
    
    
    objects = Article.objects.filter(id= article_id)[0]
    # print(objects)
    
    template = loader.get_template("blog/content_article.html")
    context = {
        "objects" : objects
    }
      
    return HttpResponse(template.render(context, request))