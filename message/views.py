from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from message.models import Message, Conversation

User = get_user_model()

def send_message(request, user_id):
    if request.method == 'POST':
        other_user = get_object_or_404(User, id=user_id)
        content = request.POST['content'].strip()  # Remove leading and trailing whitespaces

        if not content:
            # Content is empty, raise a validation error
            return render(request, 'message/conversation_detail.html', {'error': 'Message content cannot be empty'})

        try:
            # Validate the content length
            Message.full_clean(fields=['content'], exclude=None)
        except ValidationError as e:
            return render(request, 'message/conversation_detail.html', {'error': f'Invalid message content: {e.message}'})

        message = Message.objects.create(sender=request.user, receiver=other_user, content=content)

        conversation, created = Conversation.objects.get_or_create(
            messages__receiver=other_user, messages__sender=request.user
        )
        conversation.messages.add(message)

    return redirect(reverse('conversation_detail', args=[user_id]))

class UserListView(View):
    template_name = 'message/user_list.html'

    def get(self, request):
        query = request.GET.get('q', '')
        users = User.objects.exclude(id=request.user.id)

        if query:
            users = users.filter(email__icontains=query)

        return render(request, self.template_name, {'users': users, 'query': query})


class ConversationDetailView(View):
    template_name = 'message/conversation_detail.html'

    def get(self, request, user_id):
        other_user = get_object_or_404(User, id=user_id)

        conversations = Conversation.objects.filter(messages__receiver=other_user, messages__sender=request.user)

        if conversations.exists():
            conversation = conversations.first()
        else:
            # If the conversation does not exist, create a new one
            conversation = Conversation.objects.create()

        # Ensure that both the sender and receiver messages are loaded
        messages = conversation.messages.order_by('timestamp') | Message.objects.filter(
            receiver=request.user, sender=other_user
        ).order_by('timestamp')

        return render(
            request,
            self.template_name,
            {'other_user': other_user, 'messages': messages},
        )

    def post(self, request, user_id):
        other_user = get_object_or_404(User, id=user_id)
        content = request.POST['content']

        message = Message.objects.create(sender=request.user, receiver=other_user, content=content)

        # Use filter instead of get to handle multiple conversations
        conversations = Conversation.objects.filter(
            messages__receiver=other_user, messages__sender=request.user
        )

        if conversations.exists():
            conversation = conversations.first()
        else:
            # If the conversation does not exist, create a new one
            conversation = Conversation.objects.create()

        conversation.messages.add(message)

        return HttpResponseRedirect(reverse('conversation_detail', args=[user_id]))
