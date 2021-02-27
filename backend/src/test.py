import os
import sys
sys.path.append(os.getcwd())
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
    
        self.DATABASE_PATH = 'postgresql+psycopg2://anagabrielesoares:postgres@localhost:5432/newly'
        setup_db(self.app, self.DATABASE_PATH)

        """ test tokens """
        self.TOKEN_BARIST="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlYyZ2ZNSGxmRGRJRXRNbkUxNzhFMCJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZXByb2plY3R1ZGFjaXR5LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExNTUyMjU1OTcxNzkwOTU4MzcyMSIsImF1ZCI6Imh0dHA6Ly9sb2NhbGhvc3Q6NTAwMCIsImlhdCI6MTYxNDM4NzIxNSwiZXhwIjoxNjE0NDczNjE1LCJhenAiOiI5ZndPVGV1czhrNVpzZ0Y1dGhQdTJpY1phM05SaGRhVCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmRyaW5rcy1kZXRhaWwiXX0.nfhYEeJOwY5RjCKBIQmXqG3yv6BIVkjMLktq3frJdYhyTrH5RSC-VKCH3FfJ1DTyUcCkyOmvaIcLedwBmpmrRmt2k3t08xeLvo6YxLcpRWufZ3qXKXnZ-GEaRql81oNCni-F55fjPufWqOZGkukRTeFrGu82jAXqOWK0fkCb5PTcgfGb1RN9UbHgLghGKuSDfZQWeUyN47XybG3K6qLFK9BWSLVKhIGpJ56o8ZlNXAVL4uTmWxWQ8lHSDuhVfQaxbd39YI_tkc8ZRVkSUIoXvI--v0kS85F-ZVAUwrtdJ8XmCcxTWLWAqTS2obvbP03S-lFvDQ7uIGJJLQump84uig"
        self.TOKEN_MANAGER= "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlYyZ2ZNSGxmRGRJRXRNbkUxNzhFMCJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZXByb2plY3R1ZGFjaXR5LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDAwYzgxMjE1MjIxODAwNmEzYzc0MzUiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE2MTQzODc0NjMsImV4cCI6MTYxNDQ3Mzg2MywiYXpwIjoiOWZ3T1RldXM4azVac2dGNXRoUHUyaWNaYTNOUmhkYVQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZHJpbmtzIl19.PcUkqGB-12ENcu8kCIDECzatZ0hu_qrpbcatkCqAJohwZkyyLsucqsaPrG4gznWYeImHv3gKnd2cfTF6qwM4zg6Q7X1BD2BDe6FvF5AGcqH_2kCTFoxlSBfI-F3h7o3_Eg9eKUaN96kU4-QUtR1tBlEP3dLWmeauN7eERWUjlMjLLpRxIaIwljaPsJ32QFfwHfLbBy1bP35DH_DMabc_c0ccf6xFe-bHmhLPnJbkBSQVi4Cwk6X71IbE5kBbyizgtevRWhOzF7u0uHSR1rB6qO9mk0JNruvMitN1R21ptbWBjZMsfwKCYWZCYp23DEjsqlPLA8V2Kw6Oy4qH45mQSA"
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
 
    


    # def test_get_drinks_detail(self):
    #    res = self.client().get('/drinks-detail', headers = {'Authorization':'Bearer{}'.format(self.TOKEN_BARIST)})
    #    data = json.loads(res.data)

    #    self.assertEqual(res.status_code, 200)
    #    self.assertEqual(data["success"], True) 
       


    def test_get_drinks_detail(self):
       res = self.client().get('/drinks-detail', headers = {'Authorization':'Bearer {}'.format(self.TOKEN_MANAGER)})
       data = json.loads(res.data)

       self.assertEqual(res.status_code, 200)
       self.assertEqual(data["success"], True)
      
    
    # def test_get_drinks_detail_error(self):
    #    res = self.client().get('/drinks-detail', headers = {'Authorization':'Bearer{}'.format(self.FAKE_TOKEN)})
    #    data = json.loads(res.data)

    #    self.assertEqual(res.status_code, 401)
    
    
    def test_post_drink(self):
      new_drink= {
            "title":"newLYNEW",
            "recipe": {
                'color' : "white",
                'name' : 'vodca',
                'parts': '1'} 
            }
 
      res = self.client().post("/drinks-post",  headers = {'Authorization':'Bearer {}'.format(self.TOKEN_MANAGER)}, json=new_drink)
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)
      self.assertTrue(data["newly_created_drink"])
   
    

    
    # def test_post_drink_error(self):
    #   new_drink = {
    #       "title":" margaritas",
    #       "recipe": {
    #             'color' : 'black',
    #             'name' : 'coffee',
    #             'parts': '2'} 
    #   }   
    #   res = self.client().post("/drinks-post",  headers = {'Authorization':'Bearer {}'.format(self.TOKEN_BARIST)}, json=new_drink)
    #   data = json.loads(res.data)

    #   self.assertEqual(res.status_code, 401)
    #   self.assertEqual(data["success"], False)
    #   self.assertEqual(data["message"], "unauthorized")
    

    # def test_post_drink_error(self):
        
    #     res = self.client().post("/drinks-post",headers = {'Authorization':'Bearer{}'.format(self.TOKEN_MANAGER)}, json={})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 401)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "unprocessable")

    
    # def test_delete_drink(self):
    #     res = self.client().delete('/drinks-delete/3', headers = {'Authorization':'Bearer  {}'.format(self.TOKEN_MANAGER)} )
    #     data = json.loads(res.data)

    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['deleted'])
    #     self.assertTrue(data['drinks'])
       

    # def test_delete_questions_error_not_found(self):
    #    res = self.client().delete('/drinks-delete/198282', headers = {'Authorization':'Bearer  {}'.format(self.TOKEN_MANAGER)} )
    #    data = json.loads(res.data)
    #    self.assertEqual(data["success"], False)
    #    self.assertEqual(data["message"], "unprocessable")

    # def test_delete_questions_error_unauthorized(self):
    #    res = self.client().delete('/drinks-delete/1', headers = {'Authorization':'Bearer  {}'.format(self.TOKEN_BARIST)} )
    #    data = json.loads(res.data)

    #    self.assertEqual(res.status_code, 401)
    #    self.assertEqual(data["success"], False)
    #    self.assertEqual(data["message"], {
    #                      'code': 'unauthorized', 'description':
    #                      'Permission not found.'})
     
    # def test_patch_name_drink(self):
    #     res = self.client().delete('/drinks-update/2', headers = {'Authorization':'Bearer  {}'.format(self.TOKEN_MANAGER)}, json  = { 'title' : " newDrink"} )
    #     data = json.loads(res.data)

    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['deleted'])
    #     self.assertTrue(data['drinks'])
       

    # def test_patch_drink_error_not_found(self):
    #    res = self.client().delete('/drinks-update/198282', headers = {'Authorization':'Bearer  {}'.format(self.TOKEN_MANAGER)}, json = { 'title' : " newDrink"} )
    #    data = json.loads(res.data)
    #    self.assertEqual(data["success"], False)
    #    self.assertEqual(data["message"], "unprocessable")

    # def test_patch_questions_error_unauthorized(self):
    #    res = self.client().delete('/drinks-update/1', headers = {'Authorization':'Bearer  {}'.format(self.TOKEN_BARIST)}, json  = { 'title' : " newDrink"} )
    #    data = json.loads(res.data)

    #    self.assertEqual(res.status_code, 401)
    #    self.assertEqual(data["success"], False)
    #    self.assertEqual(data["message"], {
    #                      'code': 'unauthorized', 'description':
    #                      'Permission not found.'})
     


# # Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()