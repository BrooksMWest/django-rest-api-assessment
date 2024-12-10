"""View module for handling requests about artists"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist


class ArtistView(ViewSet):
    """Level up artist view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single artis type
      
        Returns:
            Response -- JSON serialized artist
        """

        try:
            artist = Artist.objects.get(pk=pk)
            serializer = ArtistSerializer(artist)
            return Response(serializer.data)
        except Artist.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all artists

        Returns:
            Response -- JSON serialized list of artists
        """
        artists = Artist.objects.prefetch_related('songs').all()

        song_id = request.query_params.get('song', None)
        if song_id is not None:
            artists = artists.filter(song__id=song_id)

        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
         """

        artist = Artist.objects.create(
            name=request.data["name"],
            age=request.data["age"],
            bio=request.data["bio"],    
        )
        serializer = ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
      """Handle PUT requests for updating an artist

      Returns:
        Response -- JSON serialized artist instance with 200 status
      """
      try:
          # Fetch the artist by primary key
          artist = Artist.objects.get(pk=pk)

          # Update fields
          artist.name = request.data["name"]
          artist.age = request.data["age"]
          artist.bio = request.data["bio"]
          artist.save()

          # Serialize the updated artist
          serializer = ArtistSerializer(artist)

          # Return updated artist data with 200 OK
          return Response(serializer.data, status=status.HTTP_200_OK)
      except Artist.DoesNotExist:
        return Response(
            {"message": "Artist not found."},
            status=status.HTTP_404_NOT_FOUND)
        
      except KeyError as e:
        return Response(
            {"message": f"Missing required field: {e.args[0]}"},
            status=status.HTTP_400_BAD_REQUEST)

    
    def destroy(self, request, pk):
        event = Artist.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for artists
    """
    song_count = serializers.SerializerMethodField()
    class Meta:
        model = Artist
        depth = 1
        fields = ('id', 'name', 'age', 'bio', 'songs', 'song_count')

    def get_song_count(self, obj):
        return obj.songs.count()
