# -*- coding: utf-8 -*-
import unittest
import warnings
from square import http


class TestHttpRoute(unittest.TestCase):
    def test_base(self):
        self.assertIn(http.Route.BASE,
                      ("https://connect.squareupsandbox.com/v2/", "https://connect.squareup.com/v2/"))

    def test_unknown_method(self):
        self.assertWarnsRegex(UserWarning, r"Unknown HTTP method 'INVALIDMETHOD'\. Expect a 501 response\.",
                              http.Route, 'INVALIDMETHOD', 'http://127.0.0.1')

    def test_known_method(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            for method in ('GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'):
                http.Route(method, "http://127.0.0.1")

                self.assertEqual(len(w), 0)

    def test_format(self):
        r = http.Route("GET", "customers/{user}/{value}", user="Genetical", value=10)

        self.assertEqual(r.url, "https://connect.squareupsandbox.com/v2/customers/Genetical/10")

    def test_no_base(self):
        _ = http.Route.BASE
        http.Route.BASE = None
        self.assertRaisesRegex(NotImplementedError, r"Route\.BASE must be set\.", http.Route, "GET", "customers")
        http.Route.BASE = _
