#!/usr/bin/env python3

import unittest
import requests


class LibraryClass(unittest.TestCase):
    '''Contains commonly used methods and attributres to be inherited'''
    url = 'http://localhost:5000/'
    headers = {'Content-type': 'application/json'}

    def submitter(self, data, response_code, path=''):
        for string in data:
            with self.subTest():
                try:
                    response = requests.post(
                        self.url + path,
                        headers=self.headers,
                        json=string,
                        timeout=0.3
                    )
                except requests.Timeout:
                    self.fail('Test timed out')
                self.assertEqual(
                    response.status_code, response_code, msg=string
                )


@unittest.skip('Not implemented')
class URLTester(LibraryClass):
    '''Test if you can get 200 on unallowed paths'''
    def test_wrong_url(self):
        pass


class EntryTester(LibraryClass):
    '''Tests the /enter/ path'''
    # test for each individual correct case?
    @classmethod
    def setUp(cls):
        cls.url += 'new/'
        # print('done')

    def flatten(self, data):
        # could use variable renaming
        output = []
        for path, the_dict in data.items():  # path and the dictionary
            for key, options in the_dict.items():  # each attribute
                for value in options:  # each value
                    temp = {
                        a: b[0] for a, b in the_dict.items()
                    }
                    temp[key] = value
                    output.append(temp)
            yield output, path
            output = []

    # @unittest.skip('testing')
    def test_valid_request(self):
        data = {
            # types: cardio, medical, telemonitoring
            'device': {
                'id': [1000000000, 999999999],
                'delivery_date': ['2017-05-15', '2016-05-15'],
                'provider': ['Amazon', 'NewEgg'],
                'type': ['cardio', 'medical', 'telemonitoring'],
                'model': ['B', 'A'],
                'serial': [10000000000000, 99999999999999]
            },
            'sim': {
                'delivery_date': ['2017-05-15', '2016-05-15'],
                'carrier': ['Mtel', 'Vivacom', 'Telenor'],
                'number': ['088379707', '0878903817']
            }
        }

        for payload, path in self.flatten(data):
            # print(payload, '\n', path)
            self.submitter(payload, 200, path)

    # def test_invalid_request(self):
    #     pass


@unittest.skip('testing other class')
class TransferTester(LibraryClass):
    '''Tests the /transfer/ path'''
    @classmethod
    def setUpClass(cls):
        cls.url += 'transfer/'

    def test_valid_request(self):
        data = [
            {'couple': 1234567890, 'company': 1},
            {'couple': 1234567890, 'company': -1}
        ]

        self.submitter(data, 200)

    # @unittest.skip('not needed')
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
