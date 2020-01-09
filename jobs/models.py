from django.db import models
from tinymce import HTMLField

class Job(models.Model):
    image = models.ImageField(upload_to='images/')
    summary = HTMLField('Content')
