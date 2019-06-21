from django.db import models

class SocialProvider(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['id', ]

    def __str__(self):
        return self.name
