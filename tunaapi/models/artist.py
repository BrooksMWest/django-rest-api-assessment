from django.db import models

class Artist(models.Model):

    name = models.CharField(max_length=50)
    age = models.CharField(max_length=50)
    bio = models.CharField(max_length=50)
