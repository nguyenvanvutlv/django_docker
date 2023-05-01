from django.contrib import admin
from image_processing.models import ImageUpload
# Register your models here.

class ImageUploadAdmin(admin.ModelAdmin):
    pass


admin.site.register(ImageUpload, ImageUploadAdmin)
