from rest_framework import serializers

from .models import Flashcard, Query


class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = "__all__"


class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = "__all__"
