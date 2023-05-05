from django.contrib import admin
from blog.models import Reporter, Article, Commented
from mdeditor.widgets import MDEditorWidget
from django.db import models
# Register your models here.


@admin.register(Reporter)
class ReporterAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     ("Section title", {
    #         "classes": ("collapse", "expanded"),
    #         "fields": (...),
    #     }),
    # ]
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
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