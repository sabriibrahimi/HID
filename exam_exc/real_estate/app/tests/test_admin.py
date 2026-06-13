from datetime import date, timedelta

from django.contrib.admin.sites import site
from django.test import RequestFactory

from .base import RealEstateTestCase as TestCase
from .factories import assign_agent, assign_feature, make_agent, make_feature, make_property, make_user, model


def _admin_for(model_name):
    return site._registry.get(model(model_name))


def _request(user):
    request = RequestFactory().get("/admin/")
    request.user = user
    return request


class AdminRegistrationTest(TestCase):
    def test_models_are_registered(self):
        self.assertIsNotNone(_admin_for("Agent"))
        self.assertIsNotNone(_admin_for("Feature"))
        self.assertIsNotNone(_admin_for("Property"))


class AgentAndFeaturePermissionTest(TestCase):
    def setUp(self):
        self.superuser = make_user("super", is_superuser=True)
        self.normal = make_user("normal")

    def test_only_superusers_can_add_agents(self):
        admin = _admin_for("Agent")
        self.assertTrue(admin.has_add_permission(_request(self.superuser)))
        self.assertFalse(admin.has_add_permission(_request(self.normal)))

    def test_only_superusers_can_add_features(self):
        admin = _admin_for("Feature")
        self.assertTrue(admin.has_add_permission(_request(self.superuser)))
        self.assertFalse(admin.has_add_permission(_request(self.normal)))


class PropertyAdminPermissionTest(TestCase):
    def setUp(self):
        self.admin = _admin_for("Property")
        self.owner = make_agent("owner")
        self.other = make_agent("other")
        self.superuser = make_user("super_property", is_superuser=True)
        self.prop = make_property()
        assign_agent(self.prop, self.owner)

    def test_only_agents_can_add_property_listings(self):
        self.assertTrue(self.admin.has_add_permission(_request(self.owner.user)))
        self.assertFalse(self.admin.has_add_permission(_request(make_user("plain"))))

    def test_save_model_assigns_current_agent_on_create(self):
        prop = model("Property")(name="New Listing", area=180, date=date.today(), description="Center")
        self.admin.save_model(_request(self.owner.user), prop, form=None, change=False)
        self.assertTrue(model("PropertyAgent").objects.filter(property=prop, agent=self.owner).exists())

    def test_responsible_agent_can_change_listing(self):
        self.assertTrue(self.admin.has_change_permission(_request(self.owner.user), self.prop))

    def test_other_agent_can_view_but_not_change_listing(self):
        self.assertFalse(self.admin.has_change_permission(_request(self.other.user), self.prop))
        queryset_ids = set(self.admin.get_queryset(_request(self.other.user)).values_list("id", flat=True))
        self.assertIn(self.prop.id, queryset_ids)

    def test_listing_can_only_be_deleted_without_features(self):
        self.assertTrue(self.admin.has_delete_permission(_request(self.owner.user), self.prop))
        assign_feature(self.prop, make_feature("Pool", 25000))
        self.assertFalse(self.admin.has_delete_permission(_request(self.owner.user), self.prop))

    def test_superuser_sees_only_today_listings(self):
        today = make_property(name="Today", listed_date=date.today())
        old = make_property(name="Old", listed_date=date.today() - timedelta(days=1))
        ids = set(self.admin.get_queryset(_request(self.superuser)).values_list("id", flat=True))
        self.assertIn(today.id, ids)
        self.assertNotIn(old.id, ids)
