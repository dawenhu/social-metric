# Generated by Django 2.2.2 on 2019-07-07 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0004_auto_20190621_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialprovider',
            name='token',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
