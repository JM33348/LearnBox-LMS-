from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()
# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.sender)


class Conversation(models.Model):
    messages = models.ManyToManyField(Message)

    def __str__(self):
        return f'Conversation {self.id}'

