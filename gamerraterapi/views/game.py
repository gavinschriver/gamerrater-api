from gamerraterapi.models.pics import Pics
from gamerraterapi.models.player import Player
from django.http.response import HttpResponseServerError
from rest_framework import status
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework.response import Response
from gamerraterapi.models import Game, Category, GameCategory
from django.db.models import Q

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label')

class PicsGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pics
        fields = ['id', 'image']

class GameSerializer(serializers.HyperlinkedModelSerializer):
    categories = CategorySerializer(many=True)
    class Meta:
        model = Game
        url = HyperlinkedIdentityField(view_name='game', lookup_field='id')
        fields = ('rated', 'id', 'average_rating', 'title', 'description', 'designer', 'year_realeased', 'number_of_players', 'time_to_play', 'age_recommendation', 'url', 'categories')

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

        search_term = self.request.query_params.get('q', None)
        if search_term is not None:
            if search_term == "":
                games = {}    
            else:
                games = games.filter(Q(title__contains=search_term) | Q(description__contains=search_term) | Q(designer__contains=search_term))

        serializer = GameSerializer(games, many=True, context={'request': req})
        return Response(serializer.data)

    def retrieve(self, req, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            # categories = Category.objects.all()
            # using related name for category on GameCategory model ('GamesCategories')
            matchingCategories = Category.objects.filter(combo__game=game)
            player = Player.objects.get(user=req.auth.user)
            pics = Pics.objects.filter(game=game)

            gameserializer = GameSerializer(game, context={'request': req})
            categoriesserializer = CategorySerializer(matchingCategories, many=True, context={'request': req})
            picsserialzier = PicsGameSerializer(pics, many=True, context={'request': req})
            gameDict = gameserializer.data
            gameDict["categories"] = categoriesserializer.data
            gameDict["pics"] = picsserialzier.data
            return Response(gameDict)
        except Exception as ex:
            return HttpResponseServerError