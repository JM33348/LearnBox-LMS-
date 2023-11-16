# urls.py
from django.urls import path
from .views import register_view, login_view, logout_view, profile_view, edit_profile

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('<int:user_id>/', profile_view, name='profile'),
    path('<int:user_id>/edit_profile/', edit_profile, name='edit_profile'),
]
