from django.urls import resolve, reverse
from django.urls.exceptions import Resolver404

from .base import CakeryTestCase as TestCase


class UrlRoutingTest(TestCase):
    def test_home_route_exists(self):
        try:
            url = reverse("index")
        except Exception:
            url = "/"
        self.assertIsNotNone(resolve(url))

    def test_add_cake_route_exists(self):
        for name in ("add_cake", "add", "cake_add", "add_new_cake", "create_cake", "new_cake"):
            try:
                self.assertIsNotNone(resolve(reverse(name)))
                return
            except Exception:
                continue
        for url in ("/add/", "/add-cake/", "/cakes/add/", "/cake/add/"):
            try:
                self.assertIsNotNone(resolve(url))
                return
            except Resolver404:
                continue
        self.fail("no add-cake route was found")

    def test_admin_route_exists(self):
        self.assertIsNotNone(resolve("/admin/"))
