from django.contrib.auth.models import User
from django.db import models as dj_models

from app.models import Baker, Cake

from .base import CakeryTestCase as TestCase
from .factories import make_baker, make_cake


def _field(model, name):
    return model._meta.get_field(name)


class BakerModelStructureTest(TestCase):
    def test_has_user_relation_to_auth_user(self):
        field = _field(Baker, "user")
        self.assertIsInstance(field, (dj_models.ForeignKey, dj_models.OneToOneField))
        self.assertIs(field.related_model, User)

    def test_has_required_profile_fields(self):
        expected = {
            "name": dj_models.CharField,
            "surname": dj_models.CharField,
            "contact_phone": dj_models.CharField,
            "email": dj_models.EmailField,
        }
        for name, field_type in expected.items():
            self.assertIsInstance(_field(Baker, name), field_type)

    def test_baker_can_be_created(self):
        baker = make_baker()
        self.assertEqual(Baker.objects.count(), 1)
        self.assertEqual(baker.user.username, "baker")


class CakeModelStructureTest(TestCase):
    def test_has_required_fields(self):
        expected = {
            "name": dj_models.CharField,
            "description": (dj_models.TextField, dj_models.CharField),
            "picture": dj_models.ImageField,
        }
        for name, field_type in expected.items():
            self.assertIsInstance(_field(Cake, name), field_type)
        self.assertIsInstance(
            _field(Cake, "price"),
            (dj_models.FloatField, dj_models.DecimalField, dj_models.IntegerField),
        )
        self.assertIsInstance(
            _field(Cake, "weight"),
            (dj_models.FloatField, dj_models.DecimalField, dj_models.IntegerField),
        )

    def test_has_baker_foreign_key(self):
        field = _field(Cake, "baker")
        self.assertIsInstance(field, dj_models.ForeignKey)
        self.assertIs(field.related_model, Baker)

    def test_cake_can_be_created(self):
        baker = make_baker()
        cake = make_cake(baker)
        self.assertEqual(Cake.objects.count(), 1)
        self.assertEqual(cake.baker, baker)
