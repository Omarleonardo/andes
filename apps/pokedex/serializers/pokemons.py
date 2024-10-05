"""Pokemon serializer"""

from rest_framework import serializers
from ..models.pokemons import Pokemon


class PokemonSerializer(serializers.ModelSerializer):
    """Serializer to manage data of pokemon"""

    class Meta:
        model = Pokemon
        fields = ["pokedex_number", "name", "abilities", "sprites", "types"]
