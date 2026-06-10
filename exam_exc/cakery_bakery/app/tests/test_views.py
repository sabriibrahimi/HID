from django.urls import reverse
from django.urls import resolve
from django.urls.exceptions import Resolver404

from app.models import Cake

from .base import CakeryTestCase as TestCase
from .factories import make_baker, make_cake


def _add_url():
    for name in ("add_cake", "add", "cake_add", "add_new_cake", "create_cake", "new_cake"):
        try:
            return reverse(name)
        except Exception:
            continue
    for url in ("/add/", "/add-cake/", "/cakes/add/", "/cake/add/"):
        try:
            resolve(url)
            return url
        except Resolver404:
            continue
    return "/add/"


class IndexViewTest(TestCase):
    def test_home_returns_200_and_displays_all_cakes(self):
        baker = make_baker()
        cake_a = make_cake(baker, name="Chocolate Wonder")
        cake_b = make_cake(baker, name="Vanilla Dream")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, cake_a.name)
        self.assertContains(response, cake_b.name)

    def test_home_context_contains_cakes(self):
        baker = make_baker()
        cake = make_cake(baker)
        response = self.client.get("/")
        context_values = response.context.flatten().values()
        found = any(
            hasattr(value, "__iter__") and cake in list(value)
            for value in context_values
            if not isinstance(value, (str, bytes, dict))
        )
        self.assertTrue(found, "home-page context does not contain the cake queryset")


class AddCakeViewTest(TestCase):
    def setUp(self):
        self.baker = make_baker()

    def test_add_page_returns_200(self):
        self.client.force_login(self.baker.user)
        self.assertEqual(self.client.get(_add_url()).status_code, 200)

    def test_post_creates_cake_for_logged_in_baker(self):
        self.client.force_login(self.baker.user)
        response = self.client.post(
            _add_url(),
            {
                "name": "Posted Cake",
                "price": 120,
                "weight": 2,
                "description": "Created from the public form",
            },
        )
        self.assertIn(response.status_code, (200, 302))
        cake = Cake.objects.filter(name="Posted Cake").first()
        self.assertIsNotNone(cake)
        self.assertEqual(cake.baker, self.baker)

    def test_anonymous_user_cannot_create_cake(self):
        self.client.post(
            _add_url(),
            {"name": "Anonymous Cake", "price": 10, "weight": 1, "description": "x"},
        )
        self.assertFalse(Cake.objects.filter(name="Anonymous Cake").exists())
