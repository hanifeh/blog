from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'users'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/', views.EditUserProfile.as_view(), name='edit-profile'),
]
