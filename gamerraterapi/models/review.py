from django.db import models

class Review(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=100)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)