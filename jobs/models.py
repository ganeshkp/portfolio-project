from django.db import models
from ckeditor.fields import RichTextField

class Job(models.Model):
    image = models.ImageField(upload_to='images/')
    summary=RichTextField(blank=True, null=True)
