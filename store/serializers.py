from rest_framework import serializers
from store import models
from users.serializers import UserSerializer


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Order
        fields = [
            'pk',
            'owner',
            'status',
        ]
