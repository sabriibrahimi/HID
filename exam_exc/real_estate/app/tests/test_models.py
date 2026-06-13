from django.apps import apps
from django.contrib.auth.models import User
from django.db import models

from .base import RealEstateTestCase as TestCase


def get_model(name):
    return apps.get_model("app", name)


def field(model, name):
    return model._meta.get_field(name)


class PropertyModelStructureTest(TestCase):
    def setUp(self):
        self.Property = get_model("Property")

    def test_has_required_fields(self):
        expected = {
            "name": models.CharField,
            "description": models.TextField,
            "area": models.FloatField,
            "date": models.DateField,
            "image": models.ImageField,
            "reserved": models.BooleanField,
            "sold": models.BooleanField,
        }
        for name, field_type in expected.items():
            self.assertIsInstance(field(self.Property, name), field_type)

    def test_feature_summary_field_exists_for_edit_display(self):
        self.assertIsInstance(field(self.Property, "feature"), models.CharField)

    def test_string_contains_name_area_and_description(self):
        prop = self.Property(name="Lake House", area=140, description="Near lake")
        text = str(prop)
        self.assertIn("Lake House", text)
        self.assertIn("140", text)
        self.assertIn("Near lake", text)


class AgentModelStructureTest(TestCase):
    def setUp(self):
        self.Agent = get_model("Agent")

    def test_has_required_profile_fields(self):
        expected = {
            "name": models.CharField,
            "surname": models.CharField,
            "contact_phone": models.CharField,
            "linked_in_profile": models.CharField,
            "completed_sales": models.IntegerField,
            "email": models.EmailField,
        }
        for name, field_type in expected.items():
            self.assertIsInstance(field(self.Agent, name), field_type)

    def test_has_user_one_to_one_to_auth_user(self):
        user_field = field(self.Agent, "user")
        self.assertIsInstance(user_field, models.OneToOneField)
        self.assertEqual(user_field.remote_field.model, User)

    def test_completed_sales_defaults_to_zero(self):
        self.assertEqual(field(self.Agent, "completed_sales").default, 0)

    def test_string_contains_first_and_last_name(self):
        agent = self.Agent(name="Ana", surname="Stone")
        self.assertIn("Ana", str(agent))
        self.assertIn("Stone", str(agent))


class FeatureModelStructureTest(TestCase):
    def setUp(self):
        self.Feature = get_model("Feature")

    def test_has_name_and_value_fields(self):
        self.assertIsInstance(field(self.Feature, "name"), models.CharField)
        self.assertIsInstance(field(self.Feature, "value"), models.FloatField)

    def test_string_contains_name_and_value(self):
        feature = self.Feature(name="Pool", value=25000)
        self.assertIn("Pool", str(feature))
        self.assertIn("25000", str(feature))


class ThroughModelStructureTest(TestCase):
    def test_property_agent_links_property_and_agent(self):
        PropertyAgent = get_model("PropertyAgent")
        self.assertIsInstance(field(PropertyAgent, "property"), models.ForeignKey)
        self.assertEqual(field(PropertyAgent, "property").remote_field.model, get_model("Property"))
        self.assertIsInstance(field(PropertyAgent, "agent"), models.ForeignKey)
        self.assertEqual(field(PropertyAgent, "agent").remote_field.model, get_model("Agent"))

    def test_property_feature_links_property_and_feature(self):
        PropertyFeature = get_model("PropertyFeature")
        self.assertIsInstance(field(PropertyFeature, "property"), models.ForeignKey)
        self.assertEqual(field(PropertyFeature, "property").remote_field.model, get_model("Property"))
        self.assertIsInstance(field(PropertyFeature, "feature"), models.ForeignKey)
        self.assertEqual(field(PropertyFeature, "feature").remote_field.model, get_model("Feature"))
