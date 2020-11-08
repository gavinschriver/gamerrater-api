from django.http.response import HttpResponseServerError
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework.response import Response
from gamerraterapi.models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label')

class CategoryViewSet(ViewSet):
    def list(self, req):
        categories = Category.objects.all()
        serialzier = CategorySerializer(categories, many=True, context={'reuqest': req})
        return Response(serialzier.data)