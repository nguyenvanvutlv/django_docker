from django.contrib import admin
from blog.models import Reporter, Article, Commented, Groups_User
from mdeditor.widgets import MDEditorWidget
from django.db import models
# Register your models here.


@admin.register(Groups_User)
class Group_UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Reporter)
class ReporterAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        print(request.session)
        return [  "title", 
                  "reporter",
                  "pub_date",
                  "types_blog"]
        
    formfield_overrides = {
        models.TextField: {'widget': MDEditorWidget}
    }
    pass


@admin.register(Commented)
class CommentedAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': MDEditorWidget}
    }
    pass