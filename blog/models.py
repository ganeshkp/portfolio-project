from django.db import models
from ckeditor.fields import RichTextField
from django.conf import settings
from datetime import timedelta, datetime

User = settings.AUTH_USER_MODEL


class Blog(models.Model):
    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.SET_NULL)
    title = models.CharField(max_length=255, unique=True)
    created_datetime = models.DateTimeField(null=True)
    pub_date = models.DateTimeField()
    body = RichTextField(blank=True, null=True)
    # image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:100]

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')

    def get_absolute_url(self):
        return f"/blogs/"

    class Meta:
        ordering = ["-pub_date"]
