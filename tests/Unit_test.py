#Unit_test.py
import unittest
import requests
import json  # To parse the JSON response

class TestFakeNewsAPI(unittest.TestCase):

    def test_real_news_1(self):
        response = requests.get('http://localhost:8080/predict?text=This is real news')
        data = json.loads(response.text)  # Parse the JSON response
        print(f"Test real_news_1 response: {data}")  # Log the parsed response
        self.assertEqual(data['prediction'], 0)  # Expect 0 for REAL news

    def test_real_news_2(self):
        response = requests.get('http://localhost:8080/predict?text=Genuine report on environmental issues')
        data = json.loads(response.text)  # Parse the JSON response
        print(f"Test real_news_2 response: {data}")
        self.assertEqual(data['prediction'], 0)  # Expect 0 for REAL news

    def test_fake_news_1(self):
        response = requests.get('http://localhost:8080/predict?text=This is fake news')
        data = json.loads(response.text)  # Parse the JSON response
        print(f"Test fake_news_1 response: {data}")
        self.assertEqual(data['prediction'], 1)  # Expect 1 for FAKE news

    def test_fake_news_2(self):
        response = requests.get('http://localhost:8080/predict?text=Totally fabricated story about celebrities')
        data = json.loads(response.text)  # Parse the JSON response
        print(f"Test fake_news_2 response: {data}")
        self.assertEqual(data['prediction'], 1)  # Expect 1 for FAKE news

if __name__ == '__main__':
    unittest.main()
