import unittest
import requests
import json


class TransferTester(unittest.TestCase):
    url = 'http://localhost:5000'
    headers = {'Content-type': 'application/json'}

    def test_valid_request(self):
        data = [
            {'couple': 1234567890, 'company': 1},
            {'couple': 1234567890, 'company': None}
        ]
        for string in data:
            try:
                response = requests.post(
                    self.url + '/transfer/',
                    headers=self.headers,
                    json=json.dumps(string),
                    timeout=0.1
                )
            except requests.Timeout:
                self.fail('Test timed out')
            self.assertEqual(response.status_code, 200)
            print(response.content)

    # @unittest.skip('testing')
    def test_invalid_request(self):
        data = [
            '{}', '{couple: 1234567890}', '{company: mtel}',
            '{"couple": "Mtel", "company": 1234567890}',
            '{"couple": "1234567890", "company": "Mtel"}',
            '{asdjkfh,234998;23sf_jkjsd}',
            '{couple:"","company":""}',
            'something incorrect',
            'юникод',
            ''
        ]
        for string in data:
            try:
                response = requests.post(
                    self.url + '/transfer/',
                    headers=self.headers,
                    json=string,
                    timeout=0.1
                )
            except requests.Timeout:
                self.fail('Test timed out')
            self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
