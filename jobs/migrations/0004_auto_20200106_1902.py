# Generated by Django 2.2.7 on 2020-01-06 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_auto_20180226_0615'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='image',
        ),
        migrations.AddField(
            model_name='job',
            name='project',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='job',
            name='summary',
            field=models.TextField(),
        ),
    ]