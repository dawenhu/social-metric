from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

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
        return context


class AnalyticDetailView(LoginRequiredMixin, TemplateView):

    template_name = 'analytics/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        provider = get_object_or_404(SocialProvider, pk=kwargs.get('pk'))
        user = self.request.user
        user.providers.add(provider)
        return context
