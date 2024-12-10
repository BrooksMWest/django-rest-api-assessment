"""View module for handling requests about genres"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre, Song



class GenreView(ViewSet):
    """Level up genres view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single genre
      
        Returns:
            Response -- JSON serialized genre
        """
        try:
            genre = Genre.objects.prefetch_related('songgenre_set__song').get(pk=pk)
            serializer = GenreSerializer(genre)
            return Response(serializer.data)
        except Genre.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
   
    def list(self, request):
        """Handle GET requests to get all genres

        Returns:
            Response -- JSON serialized list of genres
        """
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized genre instance
         """

        genre = Genre.objects.create(
            description=request.data["description"] 
        )
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            genre = Genre.objects.get(pk=pk)
            genre.description = request.data["description"]
       
            genre.save()

            serializer = GenreSerializer(genre)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Genre.DoesNotExist:
            return Response(
            {"message": "Genre not found."},
            status=status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            return Response(
            {"message": f"Missing required field: {e.args[0]}"},
            status=status.HTTP_400_BAD_REQUEST
            )
    def destroy(self, request, pk):
        event = Genre.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class SongSerializer(serializers.ModelSerializer):
    artist_id = serializers.IntegerField(source='artist.id')
    """JSON serializer for song genres
    """
    class Meta:
        model = Song
        depth =2
        fields = ('id', 'title', 'artist_id', 'album', 'length')

class GenreSerializer(serializers.ModelSerializer):
    """JSON serializer for genres
    """
    songs = serializers.SerializerMethodField()
    class Meta:
        model = Genre
        depth = 1
        fields = ('id', 'description', 'songs')
        
    def get_songs(self, obj):
        # Fetch related songs through the SongGenre join table
        related_songs = Song.objects.filter(songgenre__genre=obj)
        return SongSerializer(related_songs, many=True).data
