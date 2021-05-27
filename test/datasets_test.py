from sentiment.app import app

import unittest


class DatasetsTestCase(unittest.TestCase):

    def test_dataset_get(self):
        tester = app.test_client(self)
        response = tester.get('/api/db/dataset?page=1&bool=true&per_page=10', content_type='application/json')
        self.assertEqual(response.status_code, 200)

