# Generated by Django 4.1.3 on 2023-01-21 20:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blog_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='created_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 21, 20, 11, 1, 355884)),
        ),
    ]