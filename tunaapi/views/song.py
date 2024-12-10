"""View module for handling requests about song genres"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song
from tunaapi.models import Artist
from tunaapi.models import SongGenre
from tunaapi.models import Genre

class SongView(ViewSet):
    """Tuna Piano song view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single song

        Returns:
            Response -- JSON serialized game
        """
        try:
            song = Song.objects.select_related('artist').prefetch_related('songgenre_set__genre').get(pk=pk)
            serializer = SongSerializer(song)
            return Response(serializer.data)
        except Song.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all songs

        Returns:
            Response -- JSON serialized list of songs
        """
        songs = Song.objects.select_related('artist').prefetch_related('songgenre_set__genre')
        genre_id = request.query_params.get('genre', None)
        if genre_id is not None:
            songs = songs.filter(song_genre__genre_id=genre_id)

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
        artist=artist,
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
        try:
        # Fetch the song by primary key
            song = Song.objects.get(pk=pk)
            artist = Artist.objects.get(pk=request.data["artist_id"])

            song = Song.objects.get(pk=pk)
            song.title = request.data["title"]
            song.artist = artist
            song.album = request.data["album"]
            song.length = request.data["length"]

            ##song_genre = SongGenre.objects.get(pk=request.data["song_genre"])
            ##song.song_genre = song_genre
            song.save()

            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Artist.DoesNotExist:
            return Response(
            {"message": "Artist not found."},
            status=status.HTTP_404_NOT_FOUND
            )
        except Song.DoesNotExist:
            return Response(
                {"message": "Song not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except KeyError as e:
            return Response(
                {"message": f"Missing required field: {e.args[0]}"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def destroy(self, request, pk):
        song = Song.objects.get(pk=pk)
        song.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

class ArtistSerializer(serializers.ModelSerializer):
    """Serializer for Artist"""
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio')

class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre"""
    class Meta:
        model = Genre
        fields = ('id', 'description')
class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for song genres
    """
    artist = ArtistSerializer()  # Nested Artist
    genres = serializers.SerializerMethodField()  # Genres through join table
    class Meta:
        model = Song
        depth =2
        fields = ('id', 'title', 'artist', 'album', 'length', 'genres')
        
    def get_genres(self, obj):
        # Fetch genres through the SongGenre join table
        genres = Genre.objects.filter(songgenre__song=obj)
        return GenreSerializer(genres, many=True).data
