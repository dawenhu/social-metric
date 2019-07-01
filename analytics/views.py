import json
import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, RedirectView

from providers.models import SocialProvider

User = get_user_model()

class AnalyticView(LoginRequiredMixin, TemplateView):

    template_name = 'analytics/providers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        providers = SocialProvider.objects.exclude(user=user)

        context['navigation'] = 'analytics'
        context['providers'] = providers
        context['user'] = user
        return context


class AnalyticDetailView(LoginRequiredMixin, TemplateView):

    template_name = 'analytics/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        provider = get_object_or_404(SocialProvider, name=kwargs.get('name'))
        user = self.request.user
        user.providers.add(provider)
        return context


def analytic_auth_code_view(request, provider):
    state = request.GET.get('state')
    code = request.GET.get('code')

    if state == 'code':
        params = {
            'client_id': '638564016618730',
            'redirect_uri': 'http://localhost:8000/analytics/code/facebook/',
            'client_secret': 'baa9b546e158b586dd60f334c314c2ac',
            'code': code
        }
        url = 'https://graph.facebook.com/v3.3/oauth/access_token'
        res = requests.get(url, params=params)
        auth_token = json.loads(res.content).get('access_token')
        return HttpResponse(f"auth_token: {auth_token}")
    
    return HttpResponse(f"{provider} - {code}")