from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

app_name = 'inventory'
urlpatterns = [
    path('', views.ListProductView.as_view(), name='list'),
    path('<int:pk>', cache_page(60 * 5)(views.DetailProductView.as_view()), name='detail'),
    path('api/v1/', views.ProductList.as_view())
]
