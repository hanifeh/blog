from rest_framework import serializers
from store import models


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = [
            'pk',
            'owner',
            'status',
        ]
