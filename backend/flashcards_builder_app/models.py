from django.db import models
from django.utils.timezone import now


class Query(models.Model):
    keyword = models.CharField(max_length=255, db_index=True)
    text = models.TextField()


class WebsiteModel(models.Model):
    url = models.CharField(max_length=255)
    text = models.TextField()
    query = models.CharField(max_length=255)
    keyword = models.CharField(max_length=255, db_index=True)


class Flashcard(models.Model):
    front = models.TextField()
    back = models.TextField()
    created_at = models.DateTimeField(default=now)
    keyword = models.CharField(max_length=255, db_index=True)
    url = models.CharField(max_length=255)

    def __str__(self):
        return f'Flashcard(front="{self.front}")'
