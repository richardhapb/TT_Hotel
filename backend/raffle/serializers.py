from rest_framework import serializers
from raffle.models import Raffle
from customers.models import Customer

class RaffleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raffle
        fields = ('id', 'name', 'description', 'start_date', 'end_date', 'winner')
        extra_kwargs = {
            'winner': {'write_only': True},
        }