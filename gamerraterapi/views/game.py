from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from gamerraterapi.models import Game

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'title', 'description', 'designer', 'year_realeased', 'number_of_players', 'time_to_play', 'age_recommendation')

class GamesViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
