# Generated by Django 2.2.2 on 2019-06-21 19:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('providers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialprovider',
            name='users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
