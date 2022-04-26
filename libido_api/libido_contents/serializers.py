from rest_framework import serializers
from libido_contents.models import Content, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class ContentSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, allow_null=True)

    class Meta:
        model = Content
        fields = "__all__"
