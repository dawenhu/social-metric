# Generated by Django 2.2.2 on 2019-06-21 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0003_remove_socialprovider_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialprovider',
            name='color',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='socialprovider',
            name='icon',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]