from celery import shared_task

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from customers.models import Customer

from email_token.views import generate_token, send_verification_email

from rest_framework.response import Response

from customers.serializers import CustomerSerializer
from rest_framework import viewsets

from rest_framework_simplejwt.tokens import RefreshToken

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.template.loader import render_to_string
import smtplib
import email_config
from django.conf import settings

import uuid


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
        email_token = generate_token(customer)
        send_verification_email(customer, email_token.token)
    except Exception as e:
        print("No fue posible enviar el email de verificación")
        return Response({"error": e.args[0]}, status=400)

    return Response({"success": "Usuario creado, pendiente verificación de email"}, status=200)

@api_view(['POST'])
def set_password(request):
    data = request.data
    try:
        email = data["email"]
        password = data["password"]
    except Exception as e:
        print(e)
        return Response({"error": e.args[0]}, status=400)
    try:
        customer = Customer.objects.filter(email=email).first()
        if customer is None:
            return Response({"error": "Email no encontrado"}, status=400)

        customer.set_password(password)
    except Exception as e:
        print(e)
        return Response({"error": e.args[0]}, status=400)
    return Response({"success": "Contraseña cambiada"}, status=200)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

@csrf_exempt
@api_view(['POST'])
def login(request):
    try:
        data = request.data
        email = data["email"]
        password = data["password"]
    except Exception as e:
        print(e)
        return Response({"error": e.args[0]}, status=400)
    try:
        customer = Customer.objects.filter(email=email).first()
        if customer is None:
            return Response({"error": "Email no encontrado"}, status=400)
        if not customer.check_password(password):
            return Response({"error": "Contraseña incorrecta"}, status=400)
        
        refresh_token = RefreshToken.for_user(customer)
        access_token = str(refresh_token.access_token)
        response = Response({"success": "Sesión iniciada", "access_token": access_token}, status=200)
        response.set_cookie("refresh_token", str(refresh_token), httponly=True, secure=True)
        
    except Exception as e:
        print(e)
        return Response({"error": e.args[0]}, status=400)
    
    return response

def refresh(request):
    try:
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token is None:
            return Response({"error": "No se encontró el refresh token"}, status=400)
        
        refresh_token = RefreshToken(refresh_token)
        new_access_token = refresh_token.refresh_token
        response = Response({"success": "Sesión actualizada", "access_token": new_access_token}, status=200)
    except Exception as e:
        print(e)
        return Response({"error": e.args[0]}, status=400)
    
    return response

def logout(request):
    try:
        response = Response({"success": "Sesión finalizada"}, status=200)
        response.delete_cookie("refresh_token")
    except Exception as e:
        print(e)
        return Response({"error": e.args[0]}, status=400)
    
    return response

def send_password_reset_email(customer):
    token = uuid.uuid4()
    reset_link = f"{settings.FRONTEND_URL}/customers/password_reset/{token}/"

    try:
        customer.password_reset_token = token
        customer.set_password(str(token))
        customer.save()

        msg = MIMEMultipart()
        msg["subject"] = "Restablecer contraseña"
        msg["From"] = "Hotel CTS <hotel.cts@ctsturismo.cl>"
        msg["To"] = customer.email
        html_message = render_to_string(
            "password_reset_email.html",
            {
                "name": customer.name,
                "reset_link": reset_link,
                "password": customer.password_reset_token,
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

@api_view(['POST'])
def password_reset(request):
    try:
        data = request.data
        email = data["email"]
    except Exception as e:
        print(e)
        return Response({"error": e.args[0]}, status=400)
    try:
        customer = Customer.objects.filter(email=email).first()
        if customer is None:
            return Response({"error": "Email no encontrado"}, status=400)
        send_password_reset_email(customer)
        return Response({"success": "Email enviado"}, status=200)
    except Exception as e:
        print(e)
        return Response({"error": e.args[0]}, status=400)


@api_view(['POST'])
def change_password(request):
    try:
        data = request.data
        password = data["password"]
        new_password = data["new_password"]
        confirm_password = data["confirm_password"]
    except Exception as e:
        print(e)
        return Response({"error": e.args[0]}, status=400)
    try:
        customer = Customer.objects.filter(password_reset_token=password).first()
        if customer is None:
            return Response({"error": "Token de restablecimiento de contraseña no válido"}, status=400)
        if not customer.check_password(password):
            return Response({"error": "Contraseña incorrecta"}, status=400)
        if new_password != confirm_password:
            return Response({"error": "Las contraseñas no coinciden"}, status=400)
        customer.set_password(new_password)
        return Response({"success": "Contraseña cambiada"}, status=200)
    except Exception as e:
        print(e)
        return Response({"error": e.args[0]}, status=400)

