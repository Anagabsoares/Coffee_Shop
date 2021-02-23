import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from ..src.api import create_app
from ..src.database.models import db_drop_and_create_all, setup_db, Drink

TOKEN_BARIST = ""
TOKEN_MANAGER = ""



class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        """ test database name """
        self.DB_HOST = os.getenv('DB_HOST', 'localhost:5432')  
        self.DB_USER = os.getenv('DB_USER', 'anagabrielesoares')  
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')  
        self.DB_NAME = os.getenv('DB_NAME', 'test_coffee')  
        self.DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME)
        setup_db(self.app, self.DB_PATH)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertTrue(data["total"])

    def test_get_question_id(self):
       res = self.client().get('/questions/1')
       data = json.loads(res.data)

       self.assertEqual(data['success'], True)
       self.assertTrue(data['question'])

    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["category"])

    def test_get_questions_beyond(self):
        res = self.client().get("/questions?page=200")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")

    # def test_delete_questions(self):
    #     res = self.client().delete('/questions/6')
    #     data = json.loads(res.data)

    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['deleted'])
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'])

    def test_delete_questions_error(self):
        res = self.client().delete("/questions/7777")
        data = json.loads(res.data)

        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_post_question(self):
        new_question = {
            "question": "did we",
            "answer": "test_answer",
            "category": "1",
            "difficulty": 1,
        }
        res = self.client().post("/questions", json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_post_error(self):
        something_inexistent = {}
        res = self.client().post("/questions", json=something_inexistent)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_question_search(self):
        res = self.client().post("/questions/search", json={"searchTerm": "did"})
        data = json.loads(res.data)
        print(res)
        self.assertEqual(data["success"], True)
        self.assertEqual(res.status_code, 200)

    def test_question_search_error(self):
        res = self.client().post("/questions/search", json={"searchTerm": "kskdmks"})
        data = json.loads(res.data)

        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "Not found")

    def test_get_question_by_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertEqual(res.status_code, 200)

    def test_get_questions_by_category_error(self):
        res = self.client().get("/categories/2/questions")
        data = json.loads(res.data)

        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "Not found")

    def test_quizz_game(self):
        res = self.client().post(
            "/quizzes",
            json={
                "previous_questions": [2, 6],
                "quiz_category": {"type": "", "id": ""},
            },
        )
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertEqual(res.status_code, 200)

    def test_quizz_error(self):
        res = self.client().post(
            "/quizzes",
            json={
                "previous_questions": [999, 699],
                "quiz_category": {"type": "Enterta", "id": "99"},
            },
        )
        data = json.loads(res.data)

        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["message"], "bad request")


# # Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()