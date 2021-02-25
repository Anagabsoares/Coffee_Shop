import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from ..src.api import create_app
from ..src.database.models import db_drop_and_create_all, setup_db, Drink



class CoffeTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.testing = True
        self.client = self.app.test_client

        """ test database name """
        self.DB_HOST = os.getenv('DB_HOST', 'localhost:5432')  
        self.DB_USER = os.getenv('DB_USER', 'anagabrielesoares')  
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')  
        self.DB_NAME = os.getenv('DB_NAME', 'test_coffee')  
        self.DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME)
        setup_db(self.app, self.DB_PATH)

        """ test tokens """
        self.TOKEN_BARIST = os.getenv('TOKEN_BARIST')
        self.TOKEN_MANAGER = os.getenv('TOKEN_MANAGER')
        self.FAKE_TOKEN = 'JDSKJKS'


        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_drinks(self):
        res = self.client().get("/drinks")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["drinks"])
    
    def test_get_drinks_not_found(self):
        res = self.client().get("/drinks")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")


    def test_get_drinks_detail(self):
       res = self.client().get('/drinks-detail', headers = {'Authorization':'Bearer  {}'.format(self.TOKEN_BARIST)})
       data = json.loads(res.data)

       self.assertEqual(res.status_code, 200)
       self.assertEqual(data['success'], True)
       self.assertTrue(data['drinks'])


    def test_get_drinks_detail(self):
       res = self.client().get('/drinks-detail', headers = {'Authorization':'Bearer  {}'.format(self.TOKEN_MANAGER)})
       data = json.loads(res.data)

       self.assertEqual(res.status_code, 200)
       self.assertEqual(data['success'], True)
       self.assertTrue(data['drinks'])

    
    def test_get_drinks_detail_error(self):
       res = self.client().get('/drinks-detail', headers = {'Authorization':'Bearer  {}'.format(self.FAKE_TOKEN)})
       data = json.loads(res.data)

       self.assertEqual(res.status_code, 401)
       self.assertEqual(data["success"], False)
       self.assertEqual(data["message"], {
                         'code': 'unauthorized', 'description':
                         'Permission not found.'})

    def test_post_drink(self):
      new_drink= {
            "title":" margarita",
            "recipe": {
                'color' : "black",
                'name' : 'coffee',
                'parts': '2'

            } 
        }
      res = self.client().post("/drinks",  headers = {'Authorization':'Bearer  {}'.format(self.TOKEN_MANAGER)}, json=new_drink)
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data["success"], True)
    
    def test_post_drink_error(self):
      new_drink = {
          "title":" margarita",
          "recipe": {
                'color' : "black",
                'name' : 'coffee',
                'parts': '2'} 
      }   
      res = self.client().post("/drinks",  headers = {'Authorization':'Bearer  {}'.format(self.TOKEN_BARIST)}, json=new_drink)
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 401)
      self.assertEqual(data["success"], False)
      self.assertEqual(data["message"], {
                         'code': 'unauthorized', 'description':
                         'Permission not found.'})


    def test_post_drink_error(self):
        something_inexistent = {}
        res = self.client().post("/drinks",headers = {'Authorization':'Bearer  {}'.format(self.TOKEN_MANAGER)}, json=something_inexistent)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_delete_drink(self):
        res = self.client().delete('/drinks/1', headers = {'Authorization':'Bearer  {}'.format(self.TOKEN_MANAGER)} )
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertTrue(data['drinks'])
       

    def test_delete_questions_error_not_found(self):
       res = self.client().delete('/drinks/198282', headers = {'Authorization':'Bearer  {}'.format(self.TOKEN_MANAGER)} )
       data = json.loads(res.data)
       self.assertEqual(data["success"], False)
       self.assertEqual(data["message"], "unprocessable")

    def test_delete_questions_error_unauthorized(self):
       res = self.client().delete('/drinks/198282', headers = {'Authorization':'Bearer  {}'.format(self.TOKEN_BARIST)} )
       data = json.loads(res.data)

       self.assertEqual(res.status_code, 401)
       self.assertEqual(data["success"], False)
       self.assertEqual(data["message"], {
                         'code': 'unauthorized', 'description':
                         'Permission not found.'})
     

    
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