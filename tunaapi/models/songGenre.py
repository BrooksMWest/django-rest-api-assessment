from django.db import models
from tunaapi.models import Song
from tunaapi.models import Genre

class SongGenre(models.Model):

    song_id = models.ForeignKey(Song, on_delete=models.CASCADE)
    genre_id =  genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)
