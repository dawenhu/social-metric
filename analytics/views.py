import json
import datetime
import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import resolve
from django.views.generic import TemplateView, RedirectView

from providers.models import SocialProvider, AccessToken, Page, Follower, WeeklyMetric, DailyMetric

User = get_user_model()

class AnalyticView(LoginRequiredMixin, TemplateView):

    template_name = 'analytics/providers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        selected = user.accesstoken_set.values_list('provider', flat=True)
        providers = SocialProvider.objects.exclude(id__in=selected)
        menus = SocialProvider.objects.filter(id__in=selected)
        # providers = SocialProvider.objects.all()

        context['navigation'] = 'analytics'
        context['providers'] = providers
        context['user'] = user
        context['menus'] = menus
        return context


class AnalyticDetailView(LoginRequiredMixin, TemplateView):

    template_name = 'analytics/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        provider = get_object_or_404(SocialProvider, name=kwargs.get('name'))
        user = self.request.user
        selected = user.accesstoken_set.values_list('provider', flat=True)
        providers = SocialProvider.objects.exclude(id__in=selected)
        menus = SocialProvider.objects.filter(id__in=selected)

        if provider.name == 'instagram':
            follower_increase, follower_rate = Follower.get_followers(user)
            reach_increase, reach_rate = WeeklyMetric.get_reaches(user)
            impression_increase, impression_rate = WeeklyMetric.get_impressions(user)
            click_increase, click_rate = DailyMetric.get_clicks(user)
            view_increase, view_rate = DailyMetric.get_views(user)

            context['followers'] = follower_increase
            context['followers_rate'] = follower_rate
            context['reaches'] = follower_increase
            context['reaches_rate'] = follower_rate
            context['impressions'] = impression_increase
            context['impressions_rate'] = impression_rate
            context['clicks'] = click_increase
            context['clicks_rate'] = click_rate
            context['views'] = view_increase
            context['views_rate'] = view_rate

        context['providers'] = providers
        context['user'] = user
        context['menus'] = menus
        return context


def analytic_auth_code_view(request, provider):
    user = request.user
    code = request.GET.get('code')
    state = request.GET.get('state')

    if state:
        params = {
            'client_id': '638564016618730',
            # 'redirect_uri': 'http://localhost:8000/analytics/code/facebook/',
            'redirect_uri': 'https://app.patchdash.com/analytics/code/facebook/',
            'client_secret': 'baa9b546e158b586dd60f334c314c2ac',
            'code': code,
            'scope': 'instagram_basic,pages_show_list,instagram_manage_insights'
        }
        url = 'https://graph.facebook.com/v3.3/oauth/access_token'
        res = requests.get(url, params=params)
        auth_token = json.loads(res.content).get('access_token')

        params = {
            'grant_type': 'fb_exchange_token',
            'client_id': '638564016618730',
            'client_secret': 'baa9b546e158b586dd60f334c314c2ac',
            'fb_exchange_token': auth_token,
        }
        res = requests.get(url, params=params)
        long_term_token = json.loads(res.content).get('access_token')

        provider = SocialProvider.objects.get(name=state)
        token, created = AccessToken.objects.update_or_create(
            user=user, provider=provider, defaults={'token': long_term_token, 'valid': True}
        )
        return redirect('analytics:analytic-page', provider=provider.name, token_id=token.id)
    return HttpResponse(f"short term code : {provider} - {code}")


def analytic_page(request, provider, token_id):
    user = request.user
    provider = SocialProvider.objects.get(name=provider)

    if provider.name == 'instagram':
        token = AccessToken.objects.get(pk=token_id)
        params = {
            'access_token': token.token
        }
        url = 'https://graph.facebook.com/v3.2/me/accounts'
        res = requests.get(url, params=params)
        pages = json.loads(res.content).get('data')

        for page in pages:
            page, created = Page.objects.get_or_create(
                user=user, provider=provider, page_id=page.get('id'),
                defaults={ 'token': page.get('access_token'), 'page_id': page.get('id'), 'name': page.get('name') }
            )
            url = f'https://graph.facebook.com/v3.2/{page.page_id}'
            params = {
                'fields': 'instagram_business_account',
                'access_token': page.token
            }
            res = requests.get(url, params=params)
            ig = json.loads(res.content).get('instagram_business_account')
            
            if ig:
                page.ig_id=ig.get('id')
                page.save()

                # GET followers

                date = datetime.date.today()
                start_week = date - datetime.timedelta(date.weekday())
                end_week = start_week + datetime.timedelta(7)
                today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
                today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

                url = f'https://graph.facebook.com/v3.2/{page.ig_id}'
                params = {
                    'fields': 'biography, followers_count',
                    'access_token': page.token,
                }
                res = requests.get(url, params=params)
                followers = json.loads(res.content).get('followers_count')
                follower, created = Follower.objects.update_or_create(
                    page=page, created__range=[start_week, end_week], defaults={ 'count': followers }
                )

                # GET Weekly metrics

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
                    else:
                        reach, created = WeeklyMetric.objects.update_or_create(
                            page=page, type='reach', created__range=[start_week, end_week],
                            defaults={ 'count': metric.get('values')[1].get('value'), 'type': 'reach' }
                        )

                # GET Daily metrics
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
                    else:
                        view, created = DailyMetric.objects.update_or_create(
                            page=page, type='view', created__range=[today_min, today_max],
                            defaults={ 'count': metric.get('values')[1].get('value'), 'type': 'view' }
                        )
        return redirect('analytics:detail', name=provider.name)    
    return HttpResponse('This is for getting analytic pages.')
