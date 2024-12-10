from django.db import models
from tunaapi.models import Song
from tunaapi.models import Artist

class ArtistSong(models.Model):

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
