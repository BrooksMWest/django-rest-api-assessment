from django.db import models
from tunaapi.models import Song
from tunaapi.models import Genre

class SongGenre(models.Model):

    song= models.ForeignKey(Song, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
