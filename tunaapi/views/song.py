"""View module for handling requests about song genres"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song
from tunaapi.models import Artist
from tunaapi.models import SongGenre


class SongView(ViewSet):
    """Tuna Piano song view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single song

        Returns:
            Response -- JSON serialized game
        """
        song = Song.objects.get(pk=pk)
        serializer = SongSerializer(song)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all songs

        Returns:
            Response -- JSON serialized list of songs
        """
        songs = Song.objects.all()
        song_genre = request.query_params.get('genre', None)
        if song_genre is not None:
            songs = songs.filter(song_genre_id=song_genre)

        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
             Response -- JSON serialized song instance
        """
        artist = Artist.objects.get(pk=request.data["artist_id"])
        ##song_genre = SongGenre.objects.get(pk=request.data["song_genre"])

        song = Song.objects.create(
            title=request.data["title"],
            artist_id=artist,
            album=request.data["album"],
            length=request.data["length"]
            ##song_genre=song_genre
        )
        serializer = SongSerializer(song)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        song = Song.objects.get(pk=pk)
        song.title = request.data["title"]
        song.artist = request.data["artist_id"]
        song.album = request.data["album"]
        song.length = request.data["length"]

        song_genre = SongGenre.objects.get(pk=request.data["song_genre"])
        song.song_genre = song_genre
        song.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        song = Song.objects.get(pk=pk)
        song.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        


class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for song genres
    """
    class Meta:
        model = Song
        depth =2
        fields = ('id', 'title', 'artist_id', 'album', 'length')
