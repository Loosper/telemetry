import unittest
import requests


class TransferTester(unittest.TestCase):
    url = 'http://localhost:5000'
    headers = {'Content-type': 'application/json'}

    def test_valid_request(self):
        data = [
            {'couple': 1234567890, 'company': 1},
            {'couple': 1234567890, 'company': -1}
        ]
        for string in data:
            with self.subTest():
                try:
                    response = requests.post(
                        self.url + '/transfer/',
                        headers=self.headers,
                        json=string,
                        timeout=0.3
                    )
                except requests.Timeout:
                    self.fail('Test timed out')
                self.assertEqual(response.status_code, 200, msg=string)
                # print(response.content)

    # @unittest.skip('testing')
    def test_invalid_request(self):
        data = [
            '{}', '{couple: 1234567890}', '{company: mtel}',
            '{"couple": "Mtel", "company": 1234567890}',
            '{"couple": "1234567890", "company": "Mtel"}',
            '{asdjkfh,234998;23sf_jkjsd}',
            '{couple:"","company":""}',
            'something incorrect',
            '{"couple": -1234567890, "company": 1}',
            '{"couple": 1234567890.123, "compan": 1}',
            '{"couple": 12345678.123, "company": 1}',
            ''
        ]
        for string in data:
            with self.subTest():
                try:
                    response = requests.post(
                        self.url + '/transfer/',
                        headers=self.headers,
                        json=string,
                        timeout=0.1
                    )
                except requests.Timeout:
                    self.fail('Test timed out')
                self.assertEqual(response.status_code, 400, msg=string)


if __name__ == '__main__':
    unittest.main()
