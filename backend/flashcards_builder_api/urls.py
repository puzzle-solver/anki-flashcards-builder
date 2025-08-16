"""
URL configuration for flashcards_builder_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from flashcards_builder_app.views import (
    FlashcardView,
    QueryView,
    WebsiteView,
    create_queries_from_keywords,
    create_websites_from_queries,
    create_flashcards_from_websites,
)


router = DefaultRouter(trailing_slash=False)
router.register("queries", QueryView, basename="queries")
router.register("websites", WebsiteView, basename="websites")
router.register("flashcards", FlashcardView, basename="flashcards")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("queries/generate", create_queries_from_keywords),
    path("websites/generate", create_websites_from_queries),
    path("flashcards/generate", create_flashcards_from_websites),
    path("", include(router.urls)),
]
