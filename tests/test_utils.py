import logging
import structlog
import unittest

import pyakeneo
import pyakeneo.utils

logger = structlog.get_logger()


class TestUtils(unittest.TestCase):
    def test_urljoin(self):
        self.assertEqual(
            pyakeneo.utils.urljoin("http://a.com/", "b/", "c/", "d"),
            "http://a.com/b/c/d",
        )
        self.assertEqual(
            pyakeneo.utils.urljoin("http://a.com/", "b//", "c//", "d"),
            "http://a.com/b/c/d",
        )
        self.assertEqual(
            pyakeneo.utils.urljoin("http://a.com/", "b", "c", "d"), "http://a.com/b/c/d"
        )
        self.assertEqual(
            pyakeneo.utils.urljoin("http://a.com/", "/b/", "c", "d"),
            "http://a.com/b/c/d",
        )
