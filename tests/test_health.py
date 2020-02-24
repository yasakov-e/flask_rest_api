import os
import sys
import unittest
import json

sys.path.insert(0, '..')

from config import db, basedir, connexion_app, app


class TestHealth(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, 'test.db')

        # Hardcode application start time for testing
        app.config.app_start_time = 1

        self.app = app.test_client()

        db.drop_all()
        db.create_all()

    def tearDown(self):
        pass

    def test_health(self):

        response = self.app.get('/health',
                                headers={'Accept': 'application/json',
                                         'Content-Type': 'application/json'})

        response_data = json.loads(response.get_data(as_text=True))

        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json', response.content_type)

        # Check if response json contains all expected keys
        self.assertTrue(all(key in ('application_run_time', 'status')
                            for key in response_data.keys()))
