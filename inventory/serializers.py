from rest_framework import serializers

from inventory import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = [
            'name',
            'description',
            'price',
        ]
