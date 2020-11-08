from gamerraterapi.models.rating import Rating
from django.db import models
from django.db.models.fields import CharField, IntegerField

class Game(models.Model):
    title = CharField(max_length=50)
    description = CharField(max_length=200)
    designer = CharField(max_length=50)
    year_realeased = IntegerField()
    number_of_players = IntegerField()
    time_to_play = IntegerField()
    age_recommendation = IntegerField()

    @property
    def average_rating(self):
        ratings = Rating.objects.filter(game=self)
        total_score = 0
        for rating in ratings:
            total_score += rating.rating
        if total_score > 0:
            return total_score / len(ratings)
        else:
            return 0
    
    @property
    def rated(self):
        return self.__rated

    @rated.setter
    def rated(self, value):
        self.__rated = value


    

