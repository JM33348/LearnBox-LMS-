from django.urls import path
from .views import UserListView, ConversationDetailView, send_message

urlpatterns = [
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('conversation_detail/<int:user_id>/', ConversationDetailView.as_view(), name='conversation_detail'),
    path('send_message/<int:user_id>/', send_message, name='send_message'),
]
