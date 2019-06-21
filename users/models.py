from django.contrib.auth.models import AbstractUser
from django.db import models

from providers.models import SocialProvider

class User(AbstractUser):
    """
    User class
    """
    providers = models.ManyToManyField('providers.SocialProvider', blank=True)