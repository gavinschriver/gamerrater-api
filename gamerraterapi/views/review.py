from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from gamerraterapi.models import Review, Game, Player

class ReviewViewSet(ViewSet):
    def list(self, request):
        reviews = Review.objects.all()

        game_id = self.request.query_params.get('gameId', None)
        if game_id is not None:
            reviews = Review.objects.filter(game_id=game_id)
        serialization = ReviewSerializer(reviews, many=True)

        return Response(serialization.data, status=status.HTTP_200_OK)

class ReviewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ReviewPlayerSerializier(serializers.ModelSerializer):
    user = ReviewUserSerializer(many=False)
    class Meta:
        model = Player
        fields = ('user',)

class ReviewGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['title', 'number_of_players']

class ReviewSerializer(serializers.ModelSerializer):
    player = ReviewPlayerSerializier(many=False)
    game = ReviewGameSerializer(many=False)
    class Meta:
     model = Review
     fields = ('timestamp', 'text', 'player', 'game')
