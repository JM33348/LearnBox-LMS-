from django.shortcuts import render, redirect
from .models import Announcement
from .forms import AnnouncementForm

def announcements(request):
    announcements = Announcement.objects.all().order_by('-date_posted')[:5]
    return render(request, 'announcements/announcements.html', {'announcements': announcements})

def add_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('announcements')
    else:
        form = AnnouncementForm()

    return render(request, 'announcements/add_announcement.html', {'form': form})

def view_announcement(request, announcement_id):
    announcement = Announcement.objects.get(id=announcement_id)
    return render(request, 'announcements/view_announcement.html', {'announcement': announcement})

def delete_announcement(request, announcement_id):
    announcement = Announcement.objects.get(id=announcement_id)
    announcement.delete()
    return redirect('announcements')

def edit_announcement(request, announcement_id):
    announcement = Announcement.objects.get(id=announcement_id)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('announcements')
    else:
        form = AnnouncementForm(instance=announcement)

    return render(request, 'announcements/edit_announcement.html', {'form': form, 'announcement': announcement})