from rest_framework.test import APITestCase
from rest_framework import status
from game.models import Game

class DevMindGameTests(APITestCase):

    def test_start_game(self):
        """Start a game and verify initial question and URL"""
        response = self.client.post("/game/start", {
            "name": "Alice",
            "difficulty": 2
        }, format='json')

        print(response.status_code, response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("question", response.data)
        self.assertIn("submit_url", response.data)

    def test_submit_answer_and_get_next_question(self):
        """Start a game, submit answer, and get next question"""
        start_response = self.client.post("/game/start", {
            "name": "Bob",
            "difficulty": 1
        }, format='json')

        self.assertEqual(start_response.status_code, status.HTTP_200_OK)

        game_id = start_response.data['submit_url'].split('/')[2]

        submit_response = self.client.post(f"/game/{game_id}/submit", {
            "answer": 42
        }, format='json')

        self.assertEqual(submit_response.status_code, status.HTTP_200_OK)
        self.assertIn("result", submit_response.data)
        self.assertIn("next_question", submit_response.data)
        self.assertIn("current_score", submit_response.data)

    def test_end_game_blocks_submission(self):
        """Ensure submissions are blocked after game is ended"""
        start_response = self.client.post("/game/start", {
            "name": "Charlie",
            "difficulty": 3
        }, format='json')

        self.assertEqual(start_response.status_code, status.HTTP_200_OK)

        game_id = start_response.data['submit_url'].split('/')[2]

        #End the game
        end_response = self.client.get(f"/game/{game_id}/end")
        self.assertEqual(end_response.status_code, status.HTTP_200_OK)
        self.assertIn("history", end_response.data)

        #Try to submit after ending
        submit_response = self.client.post(f"/game/{game_id}/submit", {
            "answer": 999
        }, format='json')

        self.assertEqual(submit_response.status_code, 400)
        self.assertIn("error", submit_response.data)

    def test_end_game_summary_output(self):
        """Verify the game summary includes required fields"""
        start_response = self.client.post("/game/start", {
            "name": "Dana",
            "difficulty": 1
        }, format='json')

        self.assertEqual(start_response.status_code, status.HTTP_200_OK)

        game_id = start_response.data['submit_url'].split('/')[2]

        self.client.post(f"/game/{game_id}/submit", {
            "answer": 1
        }, format='json')

        end_response = self.client.get(f"/game/{game_id}/end")
        self.assertEqual(end_response.status_code, status.HTTP_200_OK)

        data = end_response.data
        self.assertIn("name", data)
        self.assertIn("difficulty", data)
        self.assertIn("current_score", data)
        self.assertIn("total_time_spent", data)
        self.assertIn("history", data)
