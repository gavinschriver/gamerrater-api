from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.files import ImageField

class Pics(models.Model):
    caption = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gamepics', height_field=None, width_field=None, null=True, max_length=None)
    player = models.ForeignKey('Player', on_delete=CASCADE)
    game = models.ForeignKey('Game', on_delete=models.DO_NOTHING, related_name='pictures')