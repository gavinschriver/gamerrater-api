from django.contrib.auth.models import User
from django.http import request
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from gamerraterapi.models import Pics, Player, Game
import uuid
import base64
from django.core.files.base import ContentFile

class GamePicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title']

class PicSerializer(serializers.ModelSerializer):
    game = GamePicsSerializer(many=False)
    class Meta:
        model = Pics
        fields = ['id', 'image', 'game']

class PicsViewSet(ViewSet):        
    def list(self, request):
        return Response({'message':'testresponse'}, status=status.HTTP_200_OK)

    def create(self, request):
        try:
            player = Player.objects.get(user=request.auth.user)
            game = Game.objects.get(pk=request.data["gameId"])

            pic = Pics()

            pic.player = player
            pic.game = game
            pic.caption = "No captions yet..."

            format, imagestr = request.data["base64ImageString"].split(';base64,')
            fileExt = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imagestr), name=f'{request.data["gameId"]}-{uuid.uuid4()}.{fileExt}')
            pic.image = data
            pic.save()
            serializer = PicSerializer(pic, many=False, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response({'message': 'did not save'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    



