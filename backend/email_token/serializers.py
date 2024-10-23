from rest_framework import serializers
from email_token.models import EmailToken
from customers.models import Customer

class EmailTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailToken
        fields = ('id', 'token', 'created_at', 'used')
        extra_kwargs = {
            'customer': {'write_only': True},
        }

