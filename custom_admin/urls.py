from . import views
from django.urls import path

app_name = 'custom_admin'

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    # Add more URL patterns as needed
]