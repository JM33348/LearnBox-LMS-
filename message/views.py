from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

from message.models import Message, Conversation

# Create your views here.
User = get_user_model()
def send_message(request):
    if request.method == 'POST':
        # receiver = User.objects.get(username=receiver_username)
        receiver = request.POST['receiver']
        receiver_obj = User.objects.get(email=receiver)
        content = request.POST['content']
        Message.objects.create(sender=request.user, receiver=receiver_obj, content=content)

        conversation, created = Conversation.objects.get_or_create(messages__receiver=receiver_obj)
        conversation.messages.add(Message.objects.last())

    return redirect('conversation')


def conversation(request):
    sent_messages = Message.objects.filter(sender=request.user)
    received_messages = Message.objects.filter(receiver=request.user)

    messages = sent_messages | received_messages
    messages = messages.order_by('timestamp')

    return render(request, 'message/conversation.html', {'messages': messages})