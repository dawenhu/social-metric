from django.contrib import admin

from .models import SocialProvider, AccessToken, Page, Follower, WeeklyMetric, DailyMetric

@admin.register(SocialProvider)
class SocialProviderAdmin(admin.ModelAdmin):
    pass


@admin.register(AccessToken)
class AccessTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    pass


@admin.register(WeeklyMetric)
class WeeklyMetricAdmin(admin.ModelAdmin):
    pass


@admin.register(DailyMetric)
class DailyMetricAdmin(admin.ModelAdmin):
    pass
