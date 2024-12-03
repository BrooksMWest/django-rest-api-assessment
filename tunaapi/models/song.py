from django.db import models
from tunaapi.models.artist import Artist

class Song (models.Model):

    title = models.CharField(max_length=50)
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.CharField(max_length=50)
    length = models.CharField(max_length=50)