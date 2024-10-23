from celery import shared_task

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.template.loader import render_to_string
import smtplib
import email_config

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from customers.models import Customer

from email_token.views import generate_token

from rest_framework.response import Response

from customers.serializers import CustomerSerializer
from rest_framework import viewsets




@csrf_exempt
@api_view(['POST'])
def new_user_input(request):
    data = request.data
    try:
        if not data:
            return Response({"error": "Faltan datos"}, status=400)
        # Find if the email is already in use
        if Customer.objects.filter(email=request.data["email"]).exists():
            return Response({"error": "Email ya existe"}, status=400)
        new_user.delay(data)
    except Exception as e:
        print(e)
        return Response({"error": e.args[0]}, status=400)
    
    return Response({"success": "Usuario creado"}, status=200)

@shared_task
def new_user(validated_data):
    try:
        
        serializer = CustomerSerializer(data=validated_data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
    except Exception as e:
        print("No fue posible crear el usuario")
        return Response({"error": e.args[0]}, status=400)
    

    try:
        # Send verification email
        token = generate_token(customer)
        verification_link = f"{settings.FRONTEND_URL}/email/verify/{token}"
        send_verification_email(customer, verification_link)
    except Exception as e:
        print("No fue posible enviar el email de verificación")
        return Response({"error": e.args[0]}, status=400)

    return Response({"success": "Usuario creado, pendiente verificación de email"}, status=200)

def send_verification_email(customer, verification_link):
    try:
        msg = MIMEMultipart()
        msg["subject"] = "Confirma tu Email"
        msg["From"] = "Hotel CTS <hotel.cts@ctsturismo.cl>"
        msg["To"] = customer.email
        html_message = render_to_string(
            "confirm_email.html",
            {
                "name": customer.name,
                "verification_link": verification_link,
            },
        )
        msg.attach(MIMEText(html_message, "html"))

        from_email = "hotelsorteo@ctsturismo.cl"
        to = customer.email

        # Send the email using SMTP
        with smtplib.SMTP(email_config.HOST, email_config.PORT) as server:
            server.login(email_config.USERNAME, email_config.PASSWORD)
            server.sendmail(from_email, to, msg.as_string())
    except Exception as e:
        print(e)
        raise

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

