#!/usr/bin/env python3

import unittest
import requests


class EntryTester(unittest.TestCase):
    url = 'http://localhost:5000/new/'
    headers = {'Content-type': 'application/json'}

    @unittest.skip('testing')
    def test_valid_request(self):
        data = {
            # month may be without a zero
            # types: cardio, medical, telemonitoring
            'device': {
                'id': 1234567890, 'delivery_date': '2017-05-15',
                'provider': 'Amazon', 'type': 'cardio', 'model': 'B',
                'serial': 12345678901214
            },
            'sim': {'couple': 1234567890, 'company': -1}
        }

        for string in data:
            with self.subTest():
                try:
                    response = requests.post(
                        self.url,
                        headers=self.headers,
                        json=string,
                        timeout=0.3
                    )
                except requests.Timeout:
                    self.fail('Test timed out')
                self.assertEqual(
                    response.status_code, response_code, msg=string
                )

    def test_invalid_request(self):
        pass


class TransferTester(unittest.TestCase):
    url = 'http://localhost:5000/transfer/'
    headers = {'Content-type': 'application/json'}

    def submitter(self, data, response_code):
        for string in data:
            with self.subTest():
                try:
                    response = requests.post(
                        self.url,
                        headers=self.headers,
                        json=string,
                        timeout=0.3
                    )
                except requests.Timeout:
                    self.fail('Test timed out')
                self.assertEqual(
                    response.status_code, response_code, msg=string
                )
                # print(response.content)

    def test_valid_request(self):
        data = [
            {'couple': 1234567890, 'company': 1},
            {'couple': 1234567890, 'company': -1}
        ]

        self.submitter(data, 200)

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
            '{"couple": 1234567890.123, "company": 1}',
            '{"couple": 1234567890, "company": 3}',
            '{"couple": 12345678.123, "company": 1}',
            ''
        ]

        self.submitter(data, 400)

if __name__ == '__main__':
    unittest.main()
