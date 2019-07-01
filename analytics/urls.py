from django.urls import path, include
from analytics import views

urlpatterns = [
    path('', views.AnalyticView.as_view(), name='overview'),
    path('<str:name>', views.AnalyticDetailView.as_view(), name='detail'),

    path('code/<str:provider>/', views.analytic_auth_code_view, name='oauth-code'),
]
