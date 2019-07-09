import datetime
from django.db import models
from django.conf import settings

date = datetime.date.today()
start_week = date - datetime.timedelta(date.weekday())
this_week = start_week + datetime.timedelta(7)
last_week = start_week - datetime.timedelta(7)

today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
yesterday_min = today_min - datetime.timedelta(1)
yesterday_max = today_max - datetime.timedelta(1)

class SocialProvider(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['id', ]

    def __str__(self):
        return self.name

    def get_oauth_url(self):
        if self.name in ['facebook', 'instagram']:
            endpoint = 'https://www.facebook.com/v3.3/dialog/oauth?'
            client_id = 638564016618730
            # redirect_uri = 'http://localhost:8000/analytics/code/facebook/'
            'redirect_uri': 'https://www.patchdash.com/analytics/code/facebook/'
            response_type = 'code'
            state = self.name
            scope='instagram_basic,pages_show_list,instagram_manage_insights'
            return f'{endpoint}client_id={client_id}&redirect_uri={redirect_uri}&response_type={response_type}&scope={scope}&state={state}'
        return "#"


class AccessToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    provider = models.ForeignKey('providers.SocialProvider', on_delete=models.CASCADE, blank=True, null=True)
    token = models.CharField(max_length=250, blank=True, null=True)
    valid = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.provider.name


class Page(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    provider = models.ForeignKey('providers.SocialProvider', on_delete=models.CASCADE, blank=True, null=True)
    token = models.CharField(max_length=250, blank=True, null=True)
    page_id = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    ig_id = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.page_id


class Follower(models.Model):
    page = models.ForeignKey('providers.Page', on_delete=models.CASCADE, blank=True, null=True)
    count = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.count)

    @classmethod
    def get_followers(cls, user):
        this_week_followers = cls.get_current_week_follower(user)
        last_week_followers = cls.objects.filter(page__user=user, created__range=[last_week, start_week])
        if last_week_followers.exists():
            increase = this_week_followers.first().count - last_week_followers.first().count
            rate = round(this_week_followers.first().count / last_week_followers.first().count, 2)
            return (increase, rate)
        return (0, 0)

    @classmethod
    def get_current_week_follower(cls, user):
        followers = cls.objects.filter(page__user=user, created__range=[start_week, this_week])
        return followers        


class WeeklyMetric(models.Model):
    REACH = 'reach'
    IMPRESSION = 'impression'

    TYPES = (
        (REACH, REACH),
        (IMPRESSION, IMPRESSION),
    )

    page = models.ForeignKey('providers.Page', on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(blank=False, null=False, choices=TYPES, max_length=250, default=IMPRESSION)
    count = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.page.page_id

    @classmethod
    def get_reaches(cls, user):
        this_week_reaches = cls.get_current_week_reaches(user)
        last_week_reache = cls.objects.filter(type=cls.REACH, page__user=user, created__range=[last_week, start_week])

        if last_week_reache.exists():
            increase = this_week_reaches - last_week_reache.first().count
            rate = round(this_week_reaches / last_week_reache.first().count, 2)
            return (increase, rate)
        return (0, 0)

    @classmethod
    def get_current_week_reaches(cls, user):
        reach = cls.objects.filter(type=cls.REACH, page__user=user, created__range=[start_week, this_week])
        if reach.exists():
            return reach.first().count
        return 0

    @classmethod
    def get_impressions(cls, user):
        this_week_impressions = cls.get_current_week_impressions(user)
        last_week_impression = cls.objects.filter(type=cls.IMPRESSION, page__user=user, created__range=[last_week, start_week])

        if last_week_impression.exists():
            increase = this_week_impressions - last_week_impression.first().count
            rate = round(this_week_impressions / last_week_impression.first().count, 2)
            return (increase, rate)
        return (0, 0)

    @classmethod
    def get_current_week_impressions(cls, user):
        impression = cls.objects.filter(type=cls.IMPRESSION, page__user=user, created__range=[start_week, this_week])
        if impression.exists():
            return impression.first().count
        return 0


class DailyMetric(models.Model):
    CLICK = 'click'
    VIEW = 'view'

    TYPES = (
        (CLICK, CLICK),
        (VIEW, VIEW),
    )

    page = models.ForeignKey('providers.Page', on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(blank=False, null=False, choices=TYPES, max_length=250, default=CLICK)
    count = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.page.page_id

    @classmethod
    def get_clicks(cls, user):
        today_clicks = cls.get_current_clicks(user)
        yesterday_click = cls.objects.filter(type=cls.CLICK, page__user=user, created__range=[yesterday_min, yesterday_max])

        if yesterday_click.exists():
            increase = today_clicks - yesterday_click.first().count
            rate = round(today_clicks / yesterday_click.first().count, 2)
            return (increase, rate)
        return (0, 0)

    @classmethod
    def get_current_clicks(cls, user):
        click = cls.objects.filter(type=cls.CLICK, page__user=user, created__range=[today_min, today_max])
        if click.exists():
            return click.first().count
        return 0

    @classmethod
    def get_views(cls, user):
        today_views = cls.get_current_views(user)
        yesterday_view = cls.objects.filter(type=cls.VIEW, page__user=user, created__range=[yesterday_min, yesterday_max])

        if yesterday_view.exists():
            increase = today_views - yesterday_view.first().count
            rate = round(today_views / yesterday_view.first().count, 2)
            return (increase, rate)
        return (0, 0)

    @classmethod
    def get_current_views(cls, user):
        view = cls.objects.filter(type=cls.VIEW, page__user=user, created__range=[today_min, today_max])
        if view.exists():
            return view.first().count
        return 0

