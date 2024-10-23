
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets

from raffle.models import Raffle
from raffle.serializers import RaffleSerializer

from django.http import JsonResponse

import random
from customers.models import Customer
from customers.serializers import CustomerSerializer

@api_view(['GET'])
def get_raffles(request):
    raffles = Raffle.objects.all()
    return JsonResponse({"success": "Listo", "raffles": RaffleSerializer(raffles, many=True).data}, status=200)

@api_view(['POST'])
def create_raffle(request):
    data = request.data
    try:
        name = data["name"]
        description = data["description"] if "description" in data else None
        start_date = data["start_date"] if "start_date" in data else None
        end_date = data["end_date"] if "end_date" in data else None
        winner = None
    except Exception as e:
        print(e)
        return Response({"error": e.args[0]}, status=400)
    try:
        raffle = Raffle.objects.create(name=name, description=description, start_date=start_date, end_date=end_date, winner=winner)
        return Response({"success": "Rifa creada"}, status=200)
    except Exception as e:
        print(e)
        return Response({"error": e.args[0]}, status=400)

@api_view(['GET'])
def finish_raffle(request, raffle_id):
    try:
        customers = Customer.objects.all()
        customers = customers.order_by("?")
        winner_id = customers[0].id

        raffle = Raffle.objects.get(id=raffle_id)
        raffle.winner = Customer.objects.get(id=winner_id)
        raffle.save()

    except Exception as e:
        print(e)
        return JsonResponse({"error": e.args[0]}, status=400)

    return JsonResponse({"success": "Rifa terminada", "winner": CustomerSerializer(customers, many=True).data}, status=200)
    

