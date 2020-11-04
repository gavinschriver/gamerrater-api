from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.files import ImageField

class Pics(models.Model):
    caption = models.CharField(max_length=100)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    player = models.ForeignKey('Player', on_delete=CASCADE)
    game = models.ForeignKey('Game', on_delete=CASCADE)