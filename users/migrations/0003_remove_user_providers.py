# Generated by Django 2.2.2 on 2019-07-07 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_providers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='providers',
        ),
    ]