from django.db import models
from django.db.models.fields.related import OneToOneField
from django.contrib.auth.models import User

class Player(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    