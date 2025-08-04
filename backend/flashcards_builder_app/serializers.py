from rest_framework import serializers

from .models import Flashcard, Query, WebsiteModel


class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = "__all__"


class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = "__all__"


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteModel
        fields = "__all__"


# Serializers for some requests view inputs

class QueryViewInputSerializer(serializers.Serializer):
    keywords = serializers.ListField(
        child=serializers.CharField(max_length=255),
        min_length=1,
    )


class WebsiteViewInputSerializer(serializers.Serializer):
    keywords = serializers.ListField(
        child=serializers.CharField(max_length=255),
        min_length=1,
    )
    num_websites = serializers.IntegerField(min_value=1, default=10)


class FlashcardViewInputSerializer(serializers.Serializer):
    keywords = serializers.ListField(
        child=serializers.CharField(max_length=255),
        min_length=1,
    )
    target_front = serializers.BooleanField()
