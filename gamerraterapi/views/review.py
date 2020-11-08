from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import request
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from gamerraterapi.models import Review, Game, Player
from datetime import datetime

class ReviewViewSet(ViewSet):
    def list(self, request):
        reviews = Review.objects.all()

        game_id = self.request.query_params.get('gameId', None)
        if game_id is not None:
            reviews = Review.objects.filter(game_id=game_id)
        serialization = ReviewSerializer(reviews, many=True, context={'reuqest': request})

        return Response(serialization.data, status=status.HTTP_200_OK)

    def create(self, request):
        review = Review()
        player = Player.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["gameId"])
        review.text = request.data["text"]
        review.timestamp = datetime.now()
        review.game = game
        review.player = player
        review.save()
        serializer = ReviewSerializer(review, context={'request': request})
        try:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response({'message': 'something wassanogood'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
