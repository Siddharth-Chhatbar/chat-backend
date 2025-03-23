from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ChatRoom, Message, Reaction, Reply


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class ChatRoomSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ("id", "name", "is_group_chat", "users")


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ("id", "room", "sender", "content", "timestamp", "edited_timestamp")


class ReactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Reaction
        fields = ("id", "message", "user", "emoji", "timestamp")


class ReplySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Reply
        fields = (
            "id",
            "message",
            "reply_to",
            "user",
            "content",
            "timestamp",
            "edited_timestamp",
        )
