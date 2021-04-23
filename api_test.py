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
        
    def test_matches_by_title(self):   
        response = self.application.post('/get_matches_by_title', data=dict(
            title='something',
            condition='all',
            textFormat='contains'
            ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_matches_by_title_content(self):   
        response = self.application.post('/get_matches_by_title', data=dict(
            title='something',
            condition='all',
            textFormat='contains'
            ), follow_redirects=True)
        self.assertEqual(response.content_type, 'application/json') 
        
    def test_matches_by_title_on_medals(self):
        response = self.application.post('/get_matches_by_title', data=dict(
            title='on medals',
            condition='all',
            textFormat='contains'
            ), follow_redirects=True)
        
        data = response.data
        data_string = data.decode('utf-8')
        data_dict = json.loads(data_string)
        self.assertEqual(len(data_dict), 63)
        
    def test_matches_by_title_garbage_input(self):
        response = self.application.post('/get_matches_by_title', data=dict(
            title='asdf;lajsdf98qefj1opil4j2139f81pjuf12f',
            condition='all',
            textFormat='contains'
            ), follow_redirects=True)
        
        data = response.data
        data_string = data.decode('utf-8')
        data_dict = json.loads(data_string)
        self.assertEqual(len(data_dict), 0)
        
    def test_matches_by_headword(self):   
        response = self.application.post('/get_matches_by_headword', data=dict(
            headword='the',
            condition='all',
            textFormat='contains'
            ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)    
        
    def test_matches_by_headword_content(self):   
        response = self.application.post('/get_matches_by_headword', data=dict(
            headword='the',
            condition='all',
            textFormat='contains'
            ), follow_redirects=True)
        self.assertEqual(response.content_type, 'application/json') 
        
    def test_matches_by_headword_contains(self):   
        response = self.application.post('/get_matches_by_headword', data=dict(
            headword='the',
            condition='all',
            textFormat='contains'
            ), follow_redirects=True)
        
        data = response.data
        data_string = data.decode('utf-8')
        data_dict = json.loads(data_string)
        self.assertEqual(len(data_dict), 1856)  
        
    def test_matches_by_headword_exact(self):   
        response = self.application.post('/get_matches_by_headword', data=dict(
            headword='the',
            condition='all',
            textFormat='exact'
            ), follow_redirects=True)
        
        data = response.data
        data_string = data.decode('utf-8')
        data_dict = json.loads(data_string)
        self.assertEqual(len(data_dict), 23) 
        
    def test_matches_by_headword_startswith(self):   
        response = self.application.post('/get_matches_by_headword', data=dict(
            headword='the',
            condition='all',
            textFormat='startswith'
            ), follow_redirects=True)
        
        data = response.data
        data_string = data.decode('utf-8')
        data_dict = json.loads(data_string)
        self.assertEqual(len(data_dict), 381)  
        
    def test_matches_by_author(self):   
        response = self.application.post('/get_matches_by_author', data=dict(
            author='shakespeare',
            condition='all',
            textFormat='contains'
            ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)  
        
    def test_matches_by_author_content(self):   
        response = self.application.post('/get_matches_by_author', data=dict(
            author='shakespeare',
            condition='all',
            textFormat='contains'
            ), follow_redirects=True)
        self.assertEqual(response.content_type, 'application/json') 
        
    def test_matches_by_author_shakespeare(self):
        response = self.application.post('/get_matches_by_author', data=dict(
            author='shakespeare',
            condition='all',
            textFormat='contains'
            ), follow_redirects=True)
        
        data = response.data
        data_string = data.decode('utf-8')
        data_dict = json.loads(data_string)
        self.assertEqual(len(data_dict), 15541)
        
    def test_matches_by_random(self):   
        response = self.application.post('/get_matches_by_random', data=dict(
            number=1,
            condition='all'
            ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    
    def test_matches_by_random_content(self):   
        response = self.application.post('/get_matches_by_random', data=dict(
            number=1,
            condition='all'
            ), follow_redirects=True)
        self.assertEqual(response.content_type, 'application/json') 
    
    def test_matches_by_random_10(self):
        response = self.application.post('/get_matches_by_random', data=dict(
            number=10,
            condition='all'
            ), follow_redirects=True)
        
        data = response.data
        data_string = data.decode('utf-8')
        data_dict = json.loads(data_string)
        self.assertEqual(len(data_dict), 10) 
    
    def test_matches_by_random_25(self):
        response = self.application.post('/get_matches_by_random', data=dict(
            number=25,
            condition='all'
            ), follow_redirects=True)
        
        data = response.data
        data_string = data.decode('utf-8')
        data_dict = json.loads(data_string)
        self.assertEqual(len(data_dict), 25) 
        
    def test_matches_by_random_100(self):
        response = self.application.post('/get_matches_by_random', data=dict(
            number=100, 
            condition='all'
            ), follow_redirects=True)
        
        data = response.data
        data_string = data.decode('utf-8')
        data_dict = json.loads(data_string)
        self.assertEqual(len(data_dict), 100) 
        
if __name__ == "__main__":
    unittest.main()