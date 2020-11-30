import json
from rest_framework import status
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase
from gamerraterapi.models import Category, Game

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

        #this step does A LOT - fakes a client request to this url and makes our
        #req body content json, THEN runs through all our the steps
        # of our view to that path, and returns the same response obj we'd get back
        # (e.g exactly what the client would be getting)
        res = self.client.post(url, data, format='json')

        #then we gotta turn around and take what we'd be sending to the client
        #and turn it BACK into something python can read for the sake of the testing;
        #so we're basically "catching" what we would be serializing and giving to the 
        #client 
        json_res = json.loads(res.content)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_res["title"], "testgame")
        self.assertEqual(json_res["time_to_play"], 13345)
        self.assertEqual(json_res["age_recommendation"], 5)
        self.assertEqual(json_res["description"], "pretty cool test game")
        self.assertEqual(json_res["designer"], "Milfin bradmonk")
        self.assertEqual(json_res["number_of_players"], 4)
        self.assertEqual(json_res["year_realeased"], 1388)


    def test_get_single_game(self):
        game = Game()
        game.category_id = 1
        game.title = 'testgame'
        game.time_to_play = 1234
        game.age_recommendation = 123
        game.description = "yes"
        game.designer = "nope"
        game.number_of_players = 3
        game.year_realeased = 2004

        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(f"/games/{game.id}")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["title"],'testgame')
        self.assertEqual(json_response["time_to_play"],1234)
        self.assertEqual(json_response["age_recommendation"], 123)
        self.assertEqual(json_response["description"],'yes')
        self.assertEqual(json_response["designer"],'nope')
        self.assertEqual(json_response["number_of_players"], 3)
    
    def test_get_multiple_games(self):
        game = Game()
        game.category_id = 1
        game.title = 'testgame'
        game.time_to_play = 1234
        game.age_recommendation = 123
        game.description = "yes"
        game.designer = "nope"
        game.number_of_players = 3
        game.year_realeased = 2004

        game.save()

        game = Game()
        game.category_id = 1
        game.title = 'testgame2'
        game.time_to_play = 12345
        game.age_recommendation = 1234
        game.description = "yesyes"
        game.designer = "nopenope"
        game.number_of_players = 4
        game.year_realeased = 2005

        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get("/games")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["title"],'testgame')
        self.assertEqual(json_response["time_to_play"],1234)
        self.assertEqual(json_response["age_recommendation"], 123)
        self.assertEqual(json_response["description"],'yes')
        self.assertEqual(json_response["designer"],'nope')
        self.assertEqual(json_response["number_of_players"], 3)