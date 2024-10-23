from django.urls import path
from email_token import views


urlpatterns = [
    path('verify/<token>/', views.verify_token, name='verify_token'),
    path('refresh/<token>/', views.refresh_token, name='refresh_token'),
]