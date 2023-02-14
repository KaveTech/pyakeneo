import akeneo_api_client
import akeneo_api_client.utils

import unittest

import logging
import logzero


class TestUtils(unittest.TestCase):
    def setUp(self):
        logzero.loglevel(logging.DEBUG)
    
    def test_urljoin(self):
        self.assertEqual(
            akeneo_api_client.utils.urljoin('http://a.com/', 'b/', 'c/', 'd'),
            'http://a.com/b/c/d'
        )
        self.assertEqual(
            akeneo_api_client.utils.urljoin('http://a.com/', 'b//', 'c//', 'd'),
            'http://a.com/b/c/d'
        )
        self.assertEqual(
            akeneo_api_client.utils.urljoin('http://a.com/', 'b', 'c', 'd'),
            'http://a.com/b/c/d'
        )
        self.assertEqual(
            akeneo_api_client.utils.urljoin('http://a.com/', '/b/', 'c', 'd'),
            'http://a.com/b/c/d'
        )
