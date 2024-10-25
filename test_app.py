import unittest
from app import app  # Import your Flask app

class FlaskAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()  # Create a test client
        cls.app.testing = True  # Enable testing mode

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Rule Engine!', response.data)

    def test_create_rule(self):
        response = self.app.post('/create_rule', json={'rule_string': 'Sample Rule'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Rule created!')

    def test_combine_rules(self):
        rules = ['Rule 1', 'Rule 2']
        response = self.app.post('/combine_rules', json={'rules': rules})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Rules combined!')

    def test_combine_rules_insufficient(self):
        response = self.app.post('/combine_rules', json={'rules': ['Rule 1']})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'At least two rules are required to combine')

if __name__ == '__main__':
    unittest.main()
