import json
from rest_framework import status
from rest_framework.test import APITestCase
from gamerraterapi.models import Category

class GameTests(APITestCase):
    def setUp(self):
        url = "/register"
        data = {
            "username": "gav",
            "password": "gav",
            "email": "gav@gav.gav",
            "first_name": "gav",
            "last_name": "gav"
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        category = Category()
        category.label = "thiscateogry"
        category.save()

    def test_create_game(self):
        url = "/games"
        data = {
            "category_id": 1,
            "title": "testgame",
            "time_to_play": 13345,
            "age_recommendation": 5,
            "description": "pretty cool test game",
            "designer": "Milfin bradmonk",
            "number_of_players": 4,
            "year_realeased": 1388
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        res = self.client.post(url, data, format='json')
        json_res = json.loads(res.content)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
