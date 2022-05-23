from rest_framework import serializers
from libido_chats.models import Message
from libido_users.serializers import UserLightSerializer


class MessageSerializer(serializers.ModelSerializer):
    user = UserLightSerializer(allow_null=True)

    class Meta:
        model = Message
        fields = "__all__"
