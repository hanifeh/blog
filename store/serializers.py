from rest_framework import serializers
from store import models


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Order
        fields = [
            'pk',
            'owner',
            'status',
            'orderitem_set',
        ]


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = [
            'pk',
            'order',
            'product',
            'qty',
            'price',
        ]
