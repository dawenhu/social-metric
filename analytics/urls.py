from django.urls import path, include
from analytics import views

urlpatterns = [
    path('', views.AnalyticView.as_view(), name='overview'),
    path('provider/<int:pk>', views.AnalyticDetailView.as_view(), name='detail'),
]
