from __future__ import absolute_import, unicode_literals
import json
import datetime
import requests
from celery import current_app, shared_task
from celery.result import AsyncResult
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

from providers.models import AccessToken, Page, Follower, WeeklyMetric, DailyMetric

@shared_task(bind=True)
def task_instagram_follower(self):
    print('task_instagram_follower ---------- started')
    pages = Page.objects.filter(provider__name='instagram').exclude(ig_id__isnull=True)
    for page in pages:
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)

        url = f'https://graph.facebook.com/v3.2/{page.ig_id}'
        params = {
            'fields': 'biography, followers_count',
            'access_token': page.token,
        }
        res = requests.get(url, params=params)
        cnt = json.loads(res.content).get('followers_count')
        follower, created = Follower.objects.update_or_create(
            page=page, created__range=[start_week, end_week], defaults={ 'count': cnt }
        )
        print(created, '~~~~~')


@shared_task(bind=True)
def task_instagram_weekly_metric(self):
    print('task_instagram_weekly_metric ---------- started')
    pages = Page.objects.filter(provider__name='instagram').exclude(ig_id__isnull=True)
    for page in pages:
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)
        url = f'https://graph.facebook.com/v3.2/{page.ig_id}/insights'
        params = {
            'access_token': page.token,
            'metric': 'impressions,reach',
            'period': 'week',
        }
        res = requests.get(url, params=params)
        data = json.loads(res.content).get('data')

        for metric in data:
            if metric.get('name') == 'impressions':
                impression, created = WeeklyMetric.objects.update_or_create(
                    page=page, type='impression', created__range=[start_week, end_week],
                    defaults={ 'count': metric.get('values')[1].get('value'), 'type': 'impression' }
                )
                print(created, '~~~~~')
            else:
                reach, created = WeeklyMetric.objects.update_or_create(
                    page=page, type='reach', created__range=[start_week, end_week],
                    defaults={ 'count': metric.get('values')[1].get('value'), 'type': 'reach' }
                )
                print(created, '~~~~~')


@shared_task(bind=True)
def task_instagram_daily_metric(self):
    print('task_instagram_daily_metric ---------- started')
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    pages = Page.objects.filter(provider__name='instagram').exclude(ig_id__isnull=True)
    for page in pages:
        url = f'https://graph.facebook.com/v3.2/{page.ig_id}/insights'
        params = {
            'access_token': page.token,
            'metric': 'website_clicks,profile_views',
            'period': 'day',
        }
        res = requests.get(url, params=params)
        data = json.loads(res.content).get('data')
        
        for metric in data:
            if metric.get('name') == 'website_clicks':
                click, created = DailyMetric.objects.update_or_create(
                    page=page, type='click', created__range=[today_min, today_max],
                    defaults={ 'count': metric.get('values')[1].get('value'), 'type': 'click' }
                )
                print(created, '~~~~~')
            else:
                view, created = DailyMetric.objects.update_or_create(
                    page=page, type='view', created__range=[today_min, today_max],
                    defaults={ 'count': metric.get('values')[1].get('value'), 'type': 'view' }
                )
                print(created, '~~~~~')
