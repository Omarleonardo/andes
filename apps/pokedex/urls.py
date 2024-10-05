# Django
from django.urls import path

# pokedex app
from apps.pokedex.views import (
    get_pokedex_oak,
    get_pokemon_detail,
    load_pokemons,
    edit_pokemon,
)


pokedex_enpoints = (
    path("pokedex/", get_pokedex_oak, name="pokedex"),
    path("pokedex/<str:pokemon>/", get_pokemon_detail, name="pokedex_detail"),
    path("api/pokemon/load/", load_pokemons, name="load_pokemons"),
    path("api/pokemon/<int:pk>/edit/", edit_pokemon, name="edit_pokemon"),
    path(
        "api/pokemon/load/",
        load_pokemons,
        name="load_pokemons-export",
    ),
)
