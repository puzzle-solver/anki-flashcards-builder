from django.contrib import admin

from .models import Flashcard, Query, WebsiteModel


admin.site.register(Flashcard)
admin.site.register(Query)
admin.site.register(WebsiteModel)
