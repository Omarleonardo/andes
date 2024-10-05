"""Pokemon model"""

from django.db import models


class Pokemon(models.Model):
    """Model to define pokemon"""

    pokedex_number = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    abilities = models.JSONField()
    sprites = models.JSONField()
    types = models.JSONField()

    def __str__(self):
        return self.name
