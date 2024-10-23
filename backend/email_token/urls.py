from django.urls import path
from email_token import views

urlpatterns = [
    path('email/verify/<token>', views.verify_token, name='verify_token'),
]