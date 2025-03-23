from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    is_group_chat = models.BooleanField(default=False)
    users = models.ManyToManyField(User, related_name="chatrooms")

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    content = models.TextField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited_timestamp = models.DateTimeField(null=True, blank=True)


class Reaction(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="reactions"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reactions")
    emoji = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)


class Reply(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="replies"
    )
    reply_to = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="reply_to_messages"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="replies")
    content = models.TextField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited_timestamp = models.DateTimeField(null=True, blank=True)
