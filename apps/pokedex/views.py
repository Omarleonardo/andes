"""get pokedex api view"""

# Django
from django.http import JsonResponse

# Django rest framework
from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

# Pokemon app
from .models.pokemons import Pokemon
from .serializers.pokemons import PokemonSerializer

# Utils
import requests


@swagger_auto_schema(
    tags=["pokedex"],
    method="POST",
    operation_summary="Load pokemon",
    operation_description="This endpoint loads Pokemon from the Oak public API and stores them in the database.",
    responses={
        201: openapi.Response("Pokemon loaded successfully."),
        500: openapi.Response("Unable to fetch data"),
    },
)
@api_view(["POST"])
def load_pokemons(request):
    """View to load pokemon

    Description:
        Charge the numbers of pokemon desired in order to edit its
        info and having in your local or remote database

    """
    limit = request.GET.get("limit")
    api_oak = f"https://pokeapi.co/api/v2/pokemon?limit={limit}"

    response = requests.get(api_oak)
    if response.status_code == 200:
        data = response.json()
        for pokemon in data["results"]:
            details_response = requests.get(pokemon["url"])
            if details_response.status_code == 200:
                details_data = details_response.json()

                Pokemon.objects.update_or_create(
                    pokedex_number=details_data["id"],
                    defaults={
                        "name": details_data["name"],
                        "abilities": details_data["abilities"],
                        "sprites": details_data["sprites"],
                        "types": details_data["types"],
                    },
                )
        return Response({"message": "Pokémon loaded successfully."}, status=201)
    return Response({"error": "Unable to fetch data"}, status=500)


@swagger_auto_schema(
    tags=["pokedex"],
    method="GET",
    operation_summary="get_all_pokemon",
    operation_description="Get list of pokemon with its name and the url to know more about it.",
    responses={
        200: openapi.Response(
            description="A list of Pokémon",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "name": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Name of the Pokémon"
                        ),
                        "resource": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="URL for more details about the Pokémon",
                        ),
                    },
                ),
            ),
        ),
        404: "Not Found",
    },
)
@api_view(["GET"])
def get_pokedex_oak(request):
    """View to get all pokemon

    Description:
        The modification of data is managed by PokedexMiddleware
    """

    return JsonResponse({"message": "Route to get all pokemon"})


@swagger_auto_schema(
    tags=["pokedex"],
    method="GET",
    operation_summary="get_pokemon_detail",
    operation_description="Get details of a specific pokemon by name or pokedex number.",
    manual_parameters=[
        openapi.Parameter(
            "pokemon",
            openapi.IN_PATH,
            description="Pokemon name or ID",
            type=openapi.TYPE_STRING,
        ),
    ],
    responses={
        200: openapi.Response(
            description="Details of the specific Pokémon",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "name": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Name of the Pokémon"
                    ),
                    "abilities": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "ability": openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    description="Ability object",
                                    properties={
                                        "name": openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Name of the ability",
                                        ),
                                        "url": openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="URL for the ability",
                                        ),
                                    },
                                ),
                            },
                        ),
                    ),
                    "pokedex_number": openapi.Schema(
                        type=openapi.TYPE_INTEGER, description="Pokédex number"
                    ),
                    "sprites": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Sprites of the Pokémon"
                    ),
                    "types": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "type": openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    description="Type object",
                                    properties={
                                        "name": openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Type name",
                                        ),
                                        "url": openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="URL for the type",
                                        ),
                                    },
                                ),
                            },
                        ),
                    ),
                },
            ),
        ),
        404: "Pokemon not found",
    },
)
@api_view(["GET"])
def get_pokemon_detail(request, pokemon):
    """View to get pokemon's detail

    Description:
        The modification of data is managed by PokedexMiddleware to return
        the desired format
    """

    return JsonResponse({"message": "Pokemon details by name or id"})


@swagger_auto_schema(
    tags=["pokedex"],
    method="PUT",
    operation_summary="Edit Pokemon",
    operation_description=(
        "This endpoint allows you to edit information about a Pokémon already stored in the database."
        "Data that can be updated includes name, skills, sprites, and types."
    ),
    manual_parameters=[
        openapi.Parameter(
            "pk",
            openapi.IN_PATH,
            description="Pokemon pokedex number",
            type=openapi.TYPE_INTEGER,
        ),
    ],
)
@api_view(["PUT", "PATCH"])
def edit_pokemon(request, pk):
    try:
        pokemon = Pokemon.objects.get(pk=pk)

    except Pokemon.DoesNotExist:
        return Response(
            {"error": "Pokemon not found"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = PokemonSerializer(pokemon, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
