from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures", null=True, blank=True)
    online_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        Profile.objects.create(user=instance)
