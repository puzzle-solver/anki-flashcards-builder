import asyncio
import logging

from asgiref.sync import async_to_sync
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema

from flashcards_builder.phrase_creator import (
    create_queries,
    extract_websites_from_query, create_phrases_from_website,
)
from flashcards_builder.web_scraping import Website
from .models import Flashcard, Query, WebsiteModel
from .serializers import FlashcardSerializer, QuerySerializer, WebsiteSerializer, QueryGenerateInputSerializer, WebsiteGenerateInputSerializer, FlashcardGenerateInputSerializer


logger = logging.getLogger(__name__)


class QueryView(viewsets.ModelViewSet):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer
    filterset_fields = ["keyword"]


@extend_schema(
    request=QueryGenerateInputSerializer,
    responses={201: QuerySerializer(many=True)},
)
@api_view(['POST'])
async def create_queries_from_keywords(request):
    """
    Given a list of keywords, generates a set of queries for each of them.
    """
    serializer = QueryGenerateInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    keywords = serializer.data["keywords"]
    logger.info("Started creating queries...")
    queries_texts = await asyncio.gather(
        *[create_queries(keyword) for keyword in keywords]
    )
    logger.info("Finished creating queries")
    queries = [
        Query(keyword=keyword, text=text)
        for keyword, query_data in zip(keywords, queries_texts)
        for text in query_data
    ]
    await Query.objects.abulk_create(queries)
    items = QuerySerializer(queries, many=True).data
    return Response(items, status=status.HTTP_201_CREATED)


class WebsiteView(viewsets.ModelViewSet):
    queryset = WebsiteModel.objects.all()
    serializer_class = WebsiteSerializer
    filterset_fields = ["query"]


@extend_schema(
    request=WebsiteGenerateInputSerializer,
    responses={201: WebsiteSerializer(many=True)},
)
@api_view(['POST'])
async def create_websites_from_queries(request):
    """
    Given a list of queries, browses Internet to extract matching websites (googlesearch)
    """
    serializer = WebsiteGenerateInputSerializer(request.data)
    serializer.is_valid(raise_exception=True)
    keywords = serializer.data["keywords"]
    queries = [query for keyword in keywords async for query in Query.objects.filter(keyword=keyword)]
    logger.info(f"Found {len(queries)} queries")
    logger.info("Started extracting websites...")
    websites_list = await asyncio.gather(
        *[extract_websites_from_query(query, num_websites=serializer.data["num_websites"]) for query in queries]
    )
    logger.info("Done extracting websites")
    websites_objects = [
        WebsiteModel(url=website.url, text=website.text, query=query.text, keyword=query.keyword)
        for query, websites in zip(queries, websites_list)
        for website in websites
    ]
    await WebsiteModel.objects.abulk_create(websites_objects)
    items = WebsiteSerializer(websites_objects, many=True).data
    return Response(items, status=status.HTTP_201_CREATED)


class FlashcardView(viewsets.ModelViewSet):
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer

@extend_schema(
        request=FlashcardGenerateInputSerializer,
        responses={201: FlashcardSerializer(many=True)},
)
@api_view(['POST'])
async def create_flashcards_from_websites(request):
    """
    Given a list of websites, generates a list of flashcards from each of them.
    """
    serializer = FlashcardGenerateInputSerializer(request.data)
    serializer.is_valid(raise_exception=True)
    keywords = serializer.data["keywords"]
    websites_objects = [website for keyword in keywords async for website in
                        WebsiteModel.objects.filter(keyword=keyword)]
    websites = [Website(url=website.url, text=website.text) for website in websites_objects]
    logger.info(f"Found {len(websites)} websites")
    logger.info("Started creating phrases...")
    phrases_list = await asyncio.gather(*[
        create_phrases_from_website(website) for website in websites
    ])
    logger.info("Finished creating phrases")
    flashcards = list()
    for website, phrases in zip(websites_objects, phrases_list):
        for phrase in phrases:
            front, back = (phrase.phrase, phrase.translation) if serializer.data["target_front"] else (
                phrase.translation, phrase.phrase)
            flashcard = Flashcard(
                front=front, back=f"{back} \n\n Explanation:\n{phrase.explanation}", keyword=website.keyword,
                url=website.url,
            )
            flashcards.append(flashcard)
    await Flashcard.objects.abulk_create(flashcards)
    items = FlashcardSerializer(flashcards, many=True).data
    return Response(items, status=status.HTTP_201_CREATED)
