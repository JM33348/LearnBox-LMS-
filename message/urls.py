from django.urls import path
from .views import *

urlpatterns = [
    # Add your other URL patterns here
    path('conversation/', conversation, name='conversation'),
    path('send_message/', send_message, name='send_message'),
]
