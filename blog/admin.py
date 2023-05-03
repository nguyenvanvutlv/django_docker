from django.contrib import admin
from blog.models import Reporter, Article, Question
# Register your models here.

admin.site.register(Reporter)
admin.site.register(Article)
admin.site.register(Question)