from django.db import models
from django.conf import settings

class SocialProvider(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['id', ]

    def __str__(self):
        return self.name
