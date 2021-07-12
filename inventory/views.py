from django.views.generic import ListView, DetailView
from rest_framework import generics

from . import models, serializers


class ListProductView(ListView):
    """
    Shows a list of active products
    """
    paginate_by = 10
    queryset = models.Product.objects.filter(
        is_active=True
    )


class DetailProductView(DetailView):
    model = models.Product
    template_name = 'inventory/detail-product.html'


class ProductList(generics.ListAPIView):
    queryset = models.Product.objects.filter(is_active=True)
    serializer_class = serializers.ProductSerializer
