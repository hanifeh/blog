from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'store'
urlpatterns = [
    path('add-to-cart/<int:product_id>', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.view_cart, name='view-cart'),
    path('delete/<int:product_id>', views.delete_row, name='delete-row'),
    path('deduct/', views.deduct_from_cart, name='deduct-from-cart'),
    path('finalize/', views.finalize_order, name='finalize'),
    path('list-orders/', views.ListOrdersView.as_view(), name='list-orders'),
    path('print/<int:pk>', views.PrintOrder.as_view(), name='print-order'),
]
