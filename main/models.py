from django.db import models
import random
from datetime import datetime

# class ExampleModel(models.Model):
#     model_pic = models.ImageField(upload_to = 'media/', default = 'media/None/no-img.jpg')

def directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    today = datetime.today()
    cur_date = datetime(today.year, today.month, today.day).strftime('%y_%m_%d')
    return 'uploads/{0}/{1}.xls'.format(cur_date,random.randint(1000,9999))

class Document(models.Model):
    class Meta:
        verbose_name_plural = 'users'

    # docfile = models.FileField(upload_to='documents/')
    docfile = models.FileField(upload_to=directory_path)

    def __str__(self):
        return str(self.docfile)
