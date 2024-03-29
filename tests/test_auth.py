import json
import logging

import structlog
from time import time

import requests
from vcr_unittest import VCRTestCase

from pyakeneo.auth import Auth
from pyakeneo.utils import urljoin

logger = structlog.getLogger()


class TestAuthIntegrationMock(VCRTestCase):
    client_id = "1_5hoodnvr69kwkw0cgkkwgwwoo8skwog4k8wsscgc0o0css8ggo"
    secret = "5k677icg34owogww0wocoows8g4004so40skk0s0s88g4ws8gg"
    username = "admin"
    password = "admin"
    base_url = "http://localhost:8080"

    def _get_vcr(self, **kwargs):
        myvcr = super(TestAuthIntegrationMock, self)._get_vcr(**kwargs)
        myvcr.match_on = ["method", "host", "port", "path", "query", "body", "headers"]
        myvcr.record_mode = "none"
        return myvcr

    def test_valid(self):
        auth = Auth(
            self.base_url, self.client_id, self.secret, self.username, self.password
        )
        auth._request_a_token()
        auth._refresh_the_token()

    def test_invalid_request(self):
        auth = Auth(
            self.base_url, self.client_id, "fake secret", self.username, self.password
        )
        with self.assertRaises(requests.exceptions.HTTPError):
            auth._request_a_token()

    def test_invalid_refresh(self):
        auth = Auth(
            self.base_url, self.client_id, self.secret, self.username, self.password
        )
        auth._request_a_token()
        with self.assertRaises(requests.exceptions.HTTPError):
            auth._refresh_token = "coucou"
            auth._refresh_the_token()

    def test_should_refresh_request(self):
        auth = Auth(
            self.base_url, self.client_id, self.secret, self.username, self.password
        )
        auth._request_a_token()
        self.assertFalse(auth._should_refresh_token())
        auth._expiry_date = time() - 100
        self.assertTrue(auth._should_refresh_token())

    def test_query_products_with_auth(self):
        auth = Auth(
            self.base_url, self.client_id, self.secret, self.username, self.password
        )
        r = requests.get(urljoin(self.base_url, "/api/rest/v1/products"), auth=auth)
        json_data = json.loads(r.text)
