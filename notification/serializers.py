from rest_framework import serializers
from notification.models import Notification, NotificationMessage
from user.models import CustomUser

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email"]

class SimpleMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationMessage 
        fields = ["id", "message_text", "created_at"]


class NotificationSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    message = SimpleMessageSerializer()
    class Meta:
        model = Notification
        fields = ["id", "user", "message", "is_read"]
        read_only_fields = ["is_read"]