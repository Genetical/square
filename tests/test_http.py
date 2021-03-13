# -*- coding: utf-8 -*-
import unittest


class TestHttp(unittest.TestCase):
    def test_format(self):
        from square.http import generate_route

        route = generate_route("https://connect.squareupsandbox.com/v2/")
        r = route("GET", "customers/{user}/{value}", user="Genetical", value=10)

        self.assertEqual(
            "https://connect.squareupsandbox.com/v2/customers/Genetical/10", r.url
        )
