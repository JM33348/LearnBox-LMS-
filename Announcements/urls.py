from django.urls import path
from .views import announcements, add_announcement, view_announcement, delete_announcement, edit_announcement

urlpatterns = [
    # Add your other URL patterns here
    path('announcements/', announcements, name='announcements'),
    path('add_announcement/', add_announcement, name='add_announcement'),
    path('view_announcement/<int:announcement_id>/', view_announcement, name='view_announcement'),
    path('delete_announcement/<int:announcement_id>/', delete_announcement, name='delete_announcement'),
    path('edit_announcement/<int:announcement_id>/', edit_announcement, name='edit_announcement'),
]
