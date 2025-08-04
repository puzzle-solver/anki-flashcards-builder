import asyncio

from asgiref.sync import async_to_sync
from django.http import HttpResponseBadRequest
from pydantic import BaseModel, ValidationError
from rest_framework import viewsets, status
from rest_framework.response import Response

from flashcards_builder.phrase_creator import create_queries
from .models import Flashcard, Query
from .serializers import FlashcardSerializer, QuerySerializer


class FlashcardView(viewsets.ModelViewSet):
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer
    filterset_fields = ["keyword"]

    def create(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, dict):
            serializer = self.get_serializer(data=request.data)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class Keywords(BaseModel):
    keywords: list[str]
    num_websites: int = 10


class QueryView(viewsets.ModelViewSet):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer
    filterset_fields = ["keyword"]

    @async_to_sync
    async def create(self, request, *args, **kwargs):
        try:
            keywords_data = Keywords(**request.data)
        except ValidationError as e:
            return HttpResponseBadRequest(content=f"Invalid request: {e.errors()}")
        keywords = keywords_data.keywords
        queries_texts = await asyncio.gather(
            *[
                create_queries(keyword, keywords_data.num_websites)
                for keyword in keywords_data.keywords
            ]
        )
        queries = [
            Query(keyword=keyword, text=text)
            for keyword, query_data in zip(keywords, queries_texts)
            for text in query_data
        ]
        await Query.objects.abulk_create(queries)
        items = QuerySerializer(queries, many=True).data
        return Response(items, status=status.HTTP_201_CREATED)
