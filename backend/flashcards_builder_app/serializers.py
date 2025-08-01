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
