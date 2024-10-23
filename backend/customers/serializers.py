from rest_framework import serializers

from customers.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'email', 'phone')
        extra_kwargs = {
            'password': {'write_only': True},
            'email_confirmed': {'write_only': True},
        }

        

