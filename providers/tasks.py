from __future__ import absolute_import, unicode_literals
import json
import requests
from celery import current_app, shared_task
from celery.result import AsyncResult
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

from providers.models import AccessToken

@shared_task(bind=True)
def task_facebook_update_token(self):
    print('task_facebook_update_token ---------- started')
    users = User.objects.filter(accesstoken__provider__name__in=['facebook', 'instagram'])
    for user in users:
        facebook = user.accesstoken_set.filter(provider__name='facebook')
        instagram = user.accesstoken_set.filter(provider__name='instagram')

        if facebook.exists():
            obj = facebook.first()
            token = obj.token
            url = 'https://graph.facebook.com/v3.3/oauth/access_token'
            params = {
                'grant_type': 'fb_exchange_token',
                'client_id': '638564016618730',
                'client_secret': 'baa9b546e158b586dd60f334c314c2ac',
                'fb_exchange_token': token,
            }
            res = requests.get(url, params=params)
            long_term_token = json.loads(res.content).get('access_token')

            obj.token = long_term_token
            obj.save()

            if instagram.exists():
                obj = instagram.first()
                obj.token = long_term_token
                obj.save()
                continue

            continue

        if instagram.exists():
            obj = instagram.first()
            token = obj.token
            url = 'https://graph.facebook.com/v3.3/oauth/access_token'
            params = {
                'grant_type': 'fb_exchange_token',
                'client_id': '638564016618730',
                'client_secret': 'baa9b546e158b586dd60f334c314c2ac',
                'fb_exchange_token': token,
            }
            res = requests.get(url, params=params)
            long_term_token = json.loads(res.content).get('access_token')

            obj.token = long_term_token
            obj.save()

            if facebook.exists():
                obj = facebook.first()
                obj.token = long_term_token
                obj.save()
                continue

            continue
