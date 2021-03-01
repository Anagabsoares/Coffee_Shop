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
    
        self.DATABASE_PATH = 'postgresql+psycopg2://anagabrielesoares:postgres@localhost:5432/coffee_test'
        setup_db(self.app, self.DATABASE_PATH)

        """ test tokens """
        self.TOKEN_BARIST="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlYyZ2ZNSGxmRGRJRXRNbkUxNzhFMCJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZXByb2plY3R1ZGFjaXR5LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExNTUyMjU1OTcxNzkwOTU4MzcyMSIsImF1ZCI6Imh0dHA6Ly9sb2NhbGhvc3Q6NTAwMCIsImlhdCI6MTYxNDU1ODY1NywiZXhwIjoxNjE0NjQ1MDU3LCJhenAiOiI5ZndPVGV1czhrNVpzZ0Y1dGhQdTJpY1phM05SaGRhVCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmRyaW5rcy1kZXRhaWwiXX0.DJDKtCWEH2AL85nUVg15V85osR90kMICBJZuM-rZHyH5zM8ixhaS1unWLBkyaKyJECV_sGWWVnHVXccXHuZS8BYwYgPcY7QW-H5oUpvaHp8w6qDxtk0pzaPNldhJyV_ROEQ1a7vlF2I0RBJsiSQDZeKL-ZRADuteADmQPDyElwf4ZV0Qk3FJX54WQDZTXya9aUInI4t2DGjCLOF7SrquUK0WWz5A7kIBtETSTwzt8-SD3zu6q0_VOE4RpMMl7FxA2wxe65zj3_J30iYJZrCbv9K-FrHJmi1-6EpXZxgKrO-WzE8R1Dc-YOdQwZOInbTMxeABEG4SzDPK9Sq8927dgg"
        self.TOKEN_MANAGER= "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlYyZ2ZNSGxmRGRJRXRNbkUxNzhFMCJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZXByb2plY3R1ZGFjaXR5LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDAwYzgxMjE1MjIxODAwNmEzYzc0MzUiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE2MTQ1NTg3NTAsImV4cCI6MTYxNDY0NTE1MCwiYXpwIjoiOWZ3T1RldXM4azVac2dGNXRoUHUyaWNaYTNOUmhkYVQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZHJpbmtzIl19.HoX7alTy5b3OQ65ah2F4Z5QqrnfWQUxMsLPZw2KuVyEZ4REFAxVbS3N-vzrZ5B0u0Lw3sHrtx8A-YngMQuSOHOBH6IjRBIMkThuZP9wwEXFjeXE2Qklv6XSk_OGXU337geupp-bESRqbdi_NptGiTXmARkVW4t3w9NT9KpRxqK4dIb808n4HeZAjvJrMzxKyyOU1ooNHmSVZGh_dxKo-c4Cnjgy7zSvHUtsx-V-5oHs16jzePx2YAy0I6KH-vuYFyqwECJUvmXYhra4AkkKrsT36vt89mnohJHKQnjtXK0X5x73zcclkwCrXEZwVpr4-p4yPOc_Dnam-SsAaMmQdKw"
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
            "title":"A_new_drink_to_drink_4",
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