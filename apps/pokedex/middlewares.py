"""Pokedex Middleware"""

# Django
from django.http import JsonResponse


# Utils
import re
import requests


class PokedexMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.process_pokemon_detail(request)
        if response:
            return response

        response = self.process_pokedex_list(request)
        if response:
            return response

        return self.get_response(request)

    def process_pokemon_detail(self, request):
        """Filter data for a specific pokemon

        :Parameters:
            request: contains the request's data which have the pokemon id or name
            in the path

        :Returns:
            return pokemon's detail in json format for its name, abilities, pokedex_number,
            sprites and types

        """
        api_oak_base_url = "https://pokeapi.co/api/v2/pokemon"

        pokemon_match = re.match(r"^/pokedex/(?P<pokemon>[\w-]+)/?$", request.path)

        if pokemon_match:
            pokemon_name_or_id = pokemon_match.group("pokemon")
            response = requests.get(f"{api_oak_base_url}/{pokemon_name_or_id}")

            if response.status_code == 200:
                pokemon_data = response.json()
                return JsonResponse(
                    {
                        "name": pokemon_data["name"],
                        "abilities": pokemon_data["abilities"],
                        "pokedex_number": pokemon_data["id"],
                        "sprites": pokemon_data["sprites"],
                        "types": pokemon_data["types"],
                    },
                    safe=False,
                )
            else:
                return JsonResponse({"error": "Pokemon not found"}, status=404)

        return None

    def process_pokedex_list(self, request):
        """Get a list of pokemon

        :Parameters:
            request: contains the request's data which have the api path

        :Returns:
            return a list of pokemon with its name and resource url

        """
        api_oak_base_url = "https://pokeapi.co/api/v2/pokemon"

        if request.path.startswith("/pokedex"):
            response = requests.get(api_oak_base_url)
            if response.status_code == 200:
                data = response.json()
                filtered_data = [
                    {"name": pokemon["name"], "resource": pokemon["url"]}
                    for pokemon in data.get("results", [])
                ]
                return JsonResponse(filtered_data, safe=False)

        return None
