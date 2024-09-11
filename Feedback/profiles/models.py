from django.db import models

# Create your models here.


class UserProfile(models.Model):
    image = models.FileField(upload_to="files")    #this is a file path, subfolder of uploads folder (which we configured in settings.py)
    