from django.db import models
from django.utils.timezone import now


class Flashcard(models.Model):
    keyword = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=now)
    front = models.TextField()
    back = models.TextField()


class Query(models.Model):
    keyword = models.CharField(max_length=255)
    text = models.TextField()
