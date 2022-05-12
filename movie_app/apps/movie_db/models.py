from django.db import models
from django.db.models import TextField


class Movie(models.Model):
    title = models.CharField(max_length=255)  # null=False is deafult so empty title will throw an error
    description = TextField()
    created_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
