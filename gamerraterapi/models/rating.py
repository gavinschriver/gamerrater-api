from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import IntegerField
from django.db.models.fields.related import ForeignKey

class Rating(models.Model):
    rating = IntegerField()
    player = ForeignKey('Player', on_delete=CASCADE)
    game = ForeignKey('Game', on_delete=CASCADE)