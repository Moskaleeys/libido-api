from rest_framework import serializers
from libido_contents.models import Content


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"
