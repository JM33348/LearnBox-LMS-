from django.urls import path
from . import views

urlpatterns = [
    #path('', views.calendar, name="calendar"),
    path('<int:year>/<str:month>/', views.Calendar, name="calendar")
]