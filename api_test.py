import unittest
from johnson_api import application
import json

class FlaskTest(unittest.TestCase):
    #check for response 200
    def setUp(self):
        application.config['TESTING'] = True
        application.config['DEBUG'] = False
        self.application = application.test_client()
        
    def tearDown(self):
        pass
    
    def test_login(self):   
        response = self.application.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_login_content(self):   
        response = self.application.get('/login', follow_redirects=True)
        self.assertEqual(response.content_type, 'application/json')  
    
    def test_login_success(self):   
        response = self.application.post('/login', data=dict(
            username='silveresque',
            password='password123'
            ), follow_redirects=True)
        
        data = response.data
        data_string = data.decode('utf-8')
        data_dict = json.loads(data_string)
        self.assertEqual(data_dict['message'], 'success')
        
    def test_login_failure1(self):   
        response = self.application.post('/login', data=dict(
            username='silveresques',
            password='password123'
            ), follow_redirects=True)
        
        data = response.data
        data_string = data.decode('utf-8')
        data_dict = json.loads(data_string)
        self.assertEqual(data_dict['message'], 'username or password is invalid')
        
    def test_login_failure2(self):   
        response = self.application.post('/login', data=dict(
            username='silveresque',
            password='password132'
            ), follow_redirects=True)
        
        data = response.data
        data_string = data.decode('utf-8')
        data_dict = json.loads(data_string)
        self.assertEqual(data_dict['message'], 'username or password is invalid')
        
    def test_matches_by_title(self):   
        response = self.application.post('/get_matches_by_title', data=dict(
            title='something'
            ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_matches_by_title_content(self):   
        response = self.application.post('/get_matches_by_title', data=dict(
            title='something'
            ), follow_redirects=True)
        self.assertEqual(response.content_type, 'application/json') 
        
    def test_matches_by_title_tobit(self):
        response = self.application.post('/get_matches_by_title', data=dict(
            title='tobit'
            ), follow_redirects=True)
        
        data = response.data
        data_string = data.decode('utf-8')
        data_dict = json.loads(data_string)
        self.assertEqual(len(data_dict), 2)
        
    def test_matches_by_title_on_medals(self):
        response = self.application.post('/get_matches_by_title', data=dict(
            title='on medals'
            ), follow_redirects=True)
        
        data = response.data
        data_string = data.decode('utf-8')
        data_dict = json.loads(data_string)
        self.assertEqual(len(data_dict), 63)
        
    def test_matches_by_title_garbage_input(self):
        response = self.application.post('/get_matches_by_title', data=dict(
            title='asdf;lajsdf98qefj1opil4j2139f81pjuf12f'
            ), follow_redirects=True)
        
        data = response.data
        data_string = data.decode('utf-8')
        data_dict = json.loads(data_string)
        self.assertEqual(len(data_dict), 0)
        
    def test_matches_by_random(self):   
        response = self.application.post('/get_matches_by_random', data=dict(
            number=1
            ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    
    def test_matches_by_random_content(self):   
        response = self.application.post('/get_matches_by_random', data=dict(
            number=1
            ), follow_redirects=True)
        self.assertEqual(response.content_type, 'application/json') 
    
    def test_matches_by_random_10(self):
        response = self.application.post('/get_matches_by_random', data=dict(
            number=10
            ), follow_redirects=True)
        
        data = response.data
        data_string = data.decode('utf-8')
        data_dict = json.loads(data_string)
        self.assertEqual(len(data_dict), 10) 
    
    def test_matches_by_random_25(self):
        response = self.application.post('/get_matches_by_random', data=dict(
            number=25
            ), follow_redirects=True)
        
        data = response.data
        data_string = data.decode('utf-8')
        data_dict = json.loads(data_string)
        self.assertEqual(len(data_dict), 25) 
        
    def test_matches_by_random_100(self):
        response = self.application.post('/get_matches_by_random', data=dict(
            number=100
            ), follow_redirects=True)
        
        data = response.data
        data_string = data.decode('utf-8')
        data_dict = json.loads(data_string)
        self.assertEqual(len(data_dict), 100) 
        
    
        
if __name__ == "__main__":
    unittest.main()