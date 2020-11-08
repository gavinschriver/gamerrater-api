from django.contrib.auth.models import User
from django.http import request
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from gamerraterapi.models import Rating, Game, Player

class RatingViewSet(ViewSet):
    def list(self, req):
        ratings = Rating.objects.all()
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        rating = Rating()
        player = Player.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["gameId"])
        rating.player = player
        rating.game = game
        rating.rating = request.data["rating"]
        try:
            rating.save()
            return Response({'message': 'rating added'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'message': 'rating not saved!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('rating', 'player')
        depth = 1