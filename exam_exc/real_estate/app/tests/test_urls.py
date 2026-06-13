from django.urls import resolve, reverse

from .base import RealEstateTestCase as TestCase


class UrlRoutingTest(TestCase):
    def test_index_route_exists(self):
        self.assertEqual(reverse("index"), "/index/")
        self.assertEqual(resolve("/index/").url_name, "index")

    def test_edit_route_exists_with_id_kwarg(self):
        url = reverse("edit.html", kwargs={"id": 1})
        self.assertEqual(url, "/edit.html/1/")
        match = resolve("/edit.html/1/")
        self.assertEqual(match.url_name, "edit.html")
        self.assertIn("id", match.kwargs)

    def test_admin_route_exists(self):
        self.assertEqual(resolve("/admin/").url_name, "index")
