
from email_token.models import EmailToken

from rest_framework_simplejwt.tokens import RefreshToken

import datetime


def generate_token(customer):
    email_token = EmailToken.objects.create(customer=customer)
    token = RefreshToken.for_user(customer)
    email_token.token = str(token)
    email_token.save()
    return str(token)

def verify_token(token):
    email_token = EmailToken.objects.get(token=token)
    if email_token.created_at + datetime.timedelta(minutes=10) < datetime.datetime.now():
        return False
    return True
    

