from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

class AnalyticView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand'] = 'analytics'
        return context
