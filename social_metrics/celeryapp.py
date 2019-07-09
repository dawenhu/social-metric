import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_metrics.settings')

app = Celery('social_metrics')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.redbeat_redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
app.conf.broker_pool_limit = 1
app.conf.broker_heartbeat = None
app.conf.broker_connection_timeout = 30
app.conf.worker_prefetch_multiplier = 1

app.conf.beat_schedule = {
    'facebook_update_token': {
        'task': 'providers.tasks.task_facebook_update_token',
        # 'schedule': crontab(),
        'schedule': crontab(0, 0, day_of_month='2'),
        'options': { 'queue': 'analytic', 'expires': 10500.0 }
    },
    'instagram_follower': {
        'task': 'analytics.tasks.task_instagram_follower',
        'schedule': crontab(hour=0, minute=1, day_of_week=1),
        'options': { 'queue': 'analytic', 'expires': 10500.0 }
    },
    'instagram_weekly_metric': {
        'task': 'analytics.tasks.task_instagram_weekly_metric',
        'schedule': crontab(hour=0, minute=1, day_of_week=1),
        'options': { 'queue': 'analytic', 'expires': 10500.0 }
    },
    'instagram_daily_metric': {
        'task': 'analytics.tasks.task_instagram_daily_metric',
        'schedule': crontab(minute=0, hour=1),
        'options': { 'queue': 'analytic', 'expires': 10500.0 }
    },
}

app.conf.timezone = 'UTC'
