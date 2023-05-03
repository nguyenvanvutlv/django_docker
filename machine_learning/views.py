from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

def home_ml(request):    
    template = loader.get_template("ml/base.html")
    context = {
        
    }
      
    return HttpResponse(template.render(context, request))