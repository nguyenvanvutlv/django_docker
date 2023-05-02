from django.db import models
from PIL import Image
import numpy as np
from image_processing.process import ProcessImage
from io import BytesIO
from django.core.files.base import ContentFile

# Create your models here.

Action = (
    ('Brightness', 'b'),
    ('Contrast', 'c'),
    ('Kmeans', 'k')
)


class ImageUpload(models.Model):
    author  = models.CharField(max_length= 150, primary_key=True)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    origin  = models.ImageField(upload_to= "")
    
    # def save(self, *args, **kwargs):
        
    #     current_img = Image.open(self.origin.url)
    #     image = np.array(current_img)
    #     output = ProcessImage(image, self.types).process()
    #     current_img = Image.fromarray(output)
        
    #     buffer = BytesIO()
    #     current_img.save(buffer, format='png')
    #     img_png = buffer.getvalue()
    #     self.process.save(str(self.process), ContentFile(img_png), save=False)

    #     super().save(*args, **kwargs)