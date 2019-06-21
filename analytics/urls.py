from django.urls import path, include
from analytics import views

urlpatterns = [
    path('', views.AnalyticView.as_view(), name='overview'),
]
