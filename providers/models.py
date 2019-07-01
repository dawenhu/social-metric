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

    def get_oauth_url(self):
        if self.name == 'facebook':
            return 'https://www.facebook.com/v3.3/dialog/oauth?client_id=638564016618730&redirect_uri=http://localhost:8000/analytics/code/facebook/&state=code'
        return "#"
