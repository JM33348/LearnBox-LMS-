from django.shortcuts import render
from schedule.models import Event


def calendar_view(request):
    events = Event.objects.all()
    return render(request, 'Calendar/calendar.html', {'events': events})
