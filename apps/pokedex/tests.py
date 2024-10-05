"""Pokedex tests"""

# Django rest framework
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase


class PokedexTestCase(APITestCase):
    """Test to check the response of every route"""

    def test_get_all_pokemon(self):
        url = reverse("pokedex")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if response.json():
            for pokemon in response.json():
                self.assertIn("name", pokemon)
                self.assertIn("resource", pokemon)

    def test_get_detail_pokemon(self):
        url = reverse(
            "pokedex_detail",
            kwargs={
                "pokemon": "charmander",
            },
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["name"], "charmander")
        self.assertEqual(data["pokedex_number"], 4)
        self.assertIn("sprites", data)
        self.assertIn("types", data)

        self.assertEqual(data["abilities"][0]["ability"]["name"], "blaze")
        self.assertEqual(data["abilities"][1]["ability"]["name"], "solar-power")
