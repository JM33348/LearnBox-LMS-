# custom_admin/views.py

from django.shortcuts import render
from .models import User


def user_list(request):
    users = User.objects.all()
    return render(request, 'custom_admin/user_list.html', {'users': users})
