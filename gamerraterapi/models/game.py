from django.db import models
from django.db.models.fields import CharField, DurationField, IntegerField

class Game(models.Model):
    title = CharField(max_length=50)
    description = CharField(max_length=200)
    designer = CharField(max_length=50)
    year_realeased = IntegerField()
    number_of_players = IntegerField()
    time_to_play = DurationField()
    age_recommendation = IntegerField()