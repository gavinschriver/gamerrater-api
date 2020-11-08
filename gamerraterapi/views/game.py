from django.http.response import HttpResponseServerError
from rest_framework import status
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework.response import Response
from gamerraterapi.models import Game, Category, GameCategory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label')

class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        url = HyperlinkedIdentityField(view_name='game', lookup_field='id')
        fields = ('id', 'title', 'description', 'designer', 'year_realeased', 'number_of_players', 'time_to_play', 'age_recommendation', 'url')
        depth = 1


class GamesViewSet(ViewSet):
    def create(self, req):
        game = Game()
        game.title = req.data["title"]
        game.time_to_play = req.data["time_to_play"]
        game.age_recommendation = req.data["age_recommendation"]
        game.description = req.data["description"]
        game.designer = req.data["designer"]
        game.number_of_players = req.data["number_of_players"]
        game.year_realeased = req.data["year_realeased"]
        game.save()

        category = Category.objects.get(pk=req.data["category_id"])
        gamecategory = GameCategory(game=game, category=category)
        gamecategory.save()

        try:
            serialzier = GameSerializer(game, context={'request': req})
            return Response(serialzier.data, status=status.HTTP_201_CREATED)
        except:
            return Response({'message': 'something didnt work'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        

    def list(self, req):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True, context={'request': req})
        return Response(serializer.data)

    def retrieve(self, req, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            categories = Category.objects.all()
            gamescategories = GameCategory.objects.filter(game_id=pk)
            categoryIds = []
            for gc in gamescategories:
                categoryIds.append(gc.category_id)
            matchingCategories = ([c for c in categories if c.id in categoryIds])
            
            gameserializer = GameSerializer(game, context={'request': req})
            categoriesserializer = CategorySerializer(matchingCategories, many=True, context={'request': req})
            gameDict = gameserializer.data
            gameDict["categories"] = categoriesserializer.data
            return Response(gameDict)
        except Exception as ex:
            return HttpResponseServerError