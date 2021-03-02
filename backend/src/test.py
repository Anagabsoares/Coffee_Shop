import os
import sys
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from database.models import setup_db, Drink
from auth.auth import AuthError, requires_auth
from api import create_app



class CoffeTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.testing = True
        self.client = self.app.test_client

        """ test database name """
    
        self.DATABASE_PATH = 'postgresql+psycopg2://anagabrielesoares:postgres@localhost:5432/coffeeShop'
        setup_db(self.app, self.DATABASE_PATH)

        """ test tokens """
        self.TOKEN_BARIST="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlYyZ2ZNSGxmRGRJRXRNbkUxNzhFMCJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZXByb2plY3R1ZGFjaXR5LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExNTUyMjU1OTcxNzkwOTU4MzcyMSIsImF1ZCI6Imh0dHA6Ly9sb2NhbGhvc3Q6NTAwMCIsImlhdCI6MTYxNDY0NTE4MiwiZXhwIjoxNjE0NzMxNTgyLCJhenAiOiI5ZndPVGV1czhrNVpzZ0Y1dGhQdTJpY1phM05SaGRhVCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmRyaW5rcy1kZXRhaWwiXX0.XvEy4gy5bs4265hFFc5cv5KrgzZlQmaP-GTR_Xc-ttqJFE8IZD1zKM9OWawrW0xNldqLGq4MuPtuoJCaq-xa6CpbnmXhXEOkBARtiWJTn_wCK1puh0bg0czZwB1WhVxUkFwnLkrIiX2C9UVfWRSshVkfhtaxwaiKrPXKvWPaFmC0w4LRY76tCNH0PvYxiXQPVX6It5I7vQnQPzSMRX02MKt4F0eTSheDV7H7Rl6woWVqI8A0B9BHOxibOsGPbrUI6avrWIf52FnUQ53nnPS7B8c1wKcKdcgGLFQVhPBmAOUPdQb_uAS-3zLjMjh-tiMdv2auD_8vUXHOAzj01BvnUg"
        self.TOKEN_MANAGER= 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlYyZ2ZNSGxmRGRJRXRNbkUxNzhFMCJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZXByb2plY3R1ZGFjaXR5LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDAwYzgxMjE1MjIxODAwNmEzYzc0MzUiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE2MTQ2NDUyMzAsImV4cCI6MTYxNDczMTYzMCwiYXpwIjoiOWZ3T1RldXM4azVac2dGNXRoUHUyaWNaYTNOUmhkYVQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZHJpbmtzIl19.tDmqVGyJe_cAu9SZJeEABBOZDtxfomtQYgVrxUS4ZgdLHbRATjuzYHupC1rkcZZhzvpTCeREC9IunI3KaZ866zv-JzSJ5PF8nsftMlauXaOjoHAHxe7ODBkHCJm6Mc34mXW5TnEL806OrJds1h13psc6Gm2-jIFHenJW16AkJL4nNhxsqUlRG386qNW0FEGAlZShXvSeW2WvCFn3RAPQYDcGYWBDhH92af2jXIHPI6b3B0F4UkLBcjsZSWRgt_O-_KDqA1TiMUeZgW_OsVar-QZ6I9_Vo-1b5FPSYK-sX0kxEqj6OcKpspk6ruuilHurcFVBfbsW90c1XdeIqvFlKg'
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
        print('GET DATA', data)

        self.assertEqual(data["success"], True)
        self.assertTrue(data["drinks"])
        

    def test_get_drinks_detail(self):
       res = self.client().get('/drinks-detail', headers = {'Authorization':'Bearer {}'.format(self.TOKEN_BARIST)})
       data = json.loads(res.data)
       print('GET DETAILS', data)

       self.assertEqual(res.status_code, 200)
       self.assertEqual(data['success'], True)
       self.assertTrue(data["drinks"])
       

    def test_get_drinks_detail(self):
       res = self.client().get('/drinks-detail', headers = {'Authorization':'Bearer {}'.format(self.TOKEN_MANAGER)})
       data = json.loads(res.data)
     
       self.assertEqual(res.status_code, 200)
       self.assertEqual(data["success"], True)
       self.assertTrue(data["drinks"])
      
    
    def test_get_drinks_detail_error(self):
       res = self.client().get('/drinks-detail', headers = {'Authorization':'Bearer{}'.format(self.FAKE_TOKEN)})
       data = json.loads(res.data)
       print('data drink detail ERROR', data)

       self.assertEqual(res.status_code, 401)
       self.assertEqual(data["code"], "invalid_header")
       self.assertTrue(data['description'], 'Authorization header must start with "Bearer"')
    
    
    def test_post_drink(self):
        # title should be unique- make sure to change it before running the test file
      new_drink= {
            "title":"A_new_drink_to_drink_6",
            "recipe": {
                'color' : "white",
                'name' : 'vodca',
                'parts': '1'} 
            }
 
      res = self.client().post("/drinks-post",  headers = {'Authorization':'Bearer {}'.format(self.TOKEN_MANAGER)}, json=new_drink)
      data = json.loads(res.data)
      print("POST DATA", data)
     
      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertTrue(data['newly_created_drink'])

    
    def test_post_drink_error(self):
        #  # title should be unique- make sure to change it before running  test file
      new_drink = {
          "title":"A_new_drink_to_drink_6",
          "recipe": {
                'color' : 'black',
                'name' : 'coffee',
                'parts': '2'} 
      }   
      res = self.client().post("/drinks-post",  headers = {'Authorization':'Bearer {}'.format(self.TOKEN_BARIST)}, json=new_drink)
      data = json.loads(res.data)
      print('POST DRINK ERROR', data)

      self.assertEqual(res.status_code, 401)
      self.assertEqual(data["code"], 'unauthorized')
      
    
    def test_delete_drink(self):
        # make sure to enter a correct id
        res = self.client().delete('/drinks-delete/1', headers = {'Authorization':'Bearer  {}'.format(self.TOKEN_MANAGER)} )
        data = json.loads(res.data)
        print('DELETE DATA', data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'] )
        
       
    def test_delete_drink_error_not_found(self):
       res = self.client().delete('/drinks-delete/' , headers = {'Authorization':'Bearer  {}'.format(self.TOKEN_MANAGER)} )
       data = json.loads(res.data)
       print("DELETE DATA", data)

       self.assertEqual(data["success"], False) 
       self.assertEqual(data["message"], "Not found")

    def test_delete_questions_error_unauthorized(self):
       res = self.client().delete('/drinks-delete/29', headers = {'Authorization':'Bearer  {}'.format(self.TOKEN_BARIST)} )
       data = json.loads(res.data)
       print('anaut delete', data)

       self.assertEqual(res.status_code, 401)
       self.assertEqual(data["code"], 'unauthorized')
       self.assertEqual(data["message"], 'Permission not found')
     
    def test_patch_name_drink(self):
        updated_drink =  {
          "title":"A_new_drink_to_drink_updated",
          "recipe": {
                'color' : 'black',
                'name' : 'coffee',
                'parts': '2'} 
        }   
         
        res = self.client().patch('/drinks-update/5', headers = {'Authorization':'Bearer {}'.format(self.TOKEN_MANAGER)}, json  = updated_drink )
        data = json.loads(res.data)
        print('UPDATED', data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['drinks'])
       

    def test_patch_drink_error_not_found(self):
       updated_drink =  {
          "title":" new_drink_update_error",
          "recipe": {
                'color' : 'black',
                'name' : 'coffee',
                'parts': '2'} }
       res = self.client().patch('/drinks-update/908', headers = {'Authorization':'Bearer  {}'.format(self.TOKEN_MANAGER)}, json = updated_drink )
       data = json.loads(res.data)
       print('error update', data)
    
    
       self.assertEqual(data["success"], False) 
       self.assertEqual(data["message"], "Not found")

    def test_patch_questions_error_unauthorized(self):


       updated_drink =  {
          "title":"A_new_drink_to_drink_18",
          "recipe": {
                'color' : 'black',
                'name' : 'coffee',
                'parts': '2'} 
       }
       res = self.client().patch('/drinks-update/41', headers = {'Authorization':'Bearer  {}'.format(self.TOKEN_BARIST)}, json = updated_drink)
       data = json.loads(res.data)
      
       self.assertEqual(res.status_code, 401)
       self.assertTrue(data['message'], "Permission not found")
       
     

# # Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()