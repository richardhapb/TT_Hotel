
from email_token.models import EmailToken
from rest_framework.response import Response
from customers.models import Customer
from rest_framework.decorators import api_view
import uuid
import datetime

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.template.loader import render_to_string
import smtplib
import email_config
from django.conf import settings

def generate_token(customer):
    email_token = EmailToken.objects.create(customer=customer)
    return email_token

@api_view(['GET'])
def verify_token(_, token):
    email_token = EmailToken.objects.get(token=token)
    if email_token.created_at.timestamp() + 600 < datetime.datetime.now().timestamp():
        refresh_token(token)
        send_verification_email(email_token.customer, token)
        return Response({"error": "Token expirado"}, status=400)
    
    try:
        response = verify_email(email_token.customer.email)
        email_token.used = True
        email_token.save()
    except Exception as e:
        print(e)
        return Response({"error": e.args[0]}, status=400)
    return response

def refresh_token(token):
    email_token = EmailToken.objects.get(token=token)
    if email_token.used:
        return Response({"error": "Token ya utilizado"}, status=400)
    
    email_token.token = uuid.uuid4()
    email_token.save()
    return str(email_token.token)

def verify_email(email):
    customer = Customer.objects.filter(email=email).first()
    if customer is None:
        return Response({"error": "Email no encontrado"}, status=400)
    
    email_token = EmailToken.objects.filter(customer=customer).first()
    if email_token is None:
        return Response({"error": "Token no encontrado"}, status=400)
    
    customer.email_confirmed = True
    customer.save()
    return Response({"success": "Email confirmado"}, status=200)
    

def send_verification_email(customer, token):
    try:
        msg = MIMEMultipart()
        msg["subject"] = "Confirma tu Email"
        msg["From"] = "Hotel CTS <hotel.cts@ctsturismo.cl>"
        msg["To"] = customer.email
        verification_link = f"{settings.FRONTEND_URL}/email/verify/{token}"
        html_message = render_to_string(
            "confirm_email.html",
            {
                "name": customer.name,
                "verification_link": verification_link,
            },
        )
        msg.attach(MIMEText(html_message, "html"))

        # Send the email using SMTP
        with smtplib.SMTP(email_config.HOST, email_config.PORT) as server:
            server.login(email_config.USERNAME, email_config.PASSWORD)
            server.sendmail(msg["From"], customer.email, msg.as_string())
    except Exception as e:
        print(e)
        raise
        
