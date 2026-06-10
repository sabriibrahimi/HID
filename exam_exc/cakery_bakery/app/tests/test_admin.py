from django.contrib.admin.sites import site
from django.test import RequestFactory

from app.models import Baker, Cake

from .base import CakeryTestCase as TestCase
from .factories import make_baker, make_cake, make_user


def _admin_for(model):
    return site._registry.get(model)


def _request(user):
    request = RequestFactory().get("/admin/")
    request.user = user
    return request


class AdminRegistrationTest(TestCase):
    def test_baker_registered(self):
        self.assertIsNotNone(_admin_for(Baker))

    def test_cake_registered(self):
        self.assertIsNotNone(_admin_for(Cake))


class BakerPermissionTest(TestCase):
    def setUp(self):
        self.admin = _admin_for(Baker)
        self.superuser = make_user("super", is_superuser=True)
        self.normal = make_user("normal")
        self.baker = make_baker("target")

    def test_only_superuser_can_add_baker(self):
        self.assertTrue(self.admin.has_add_permission(_request(self.superuser)))
        self.assertFalse(self.admin.has_add_permission(_request(self.normal)))

    def test_only_superuser_can_change_baker(self):
        self.assertTrue(self.admin.has_change_permission(_request(self.superuser), self.baker))
        self.assertFalse(self.admin.has_change_permission(_request(self.normal), self.baker))

    def test_only_superuser_can_delete_baker(self):
        self.assertTrue(self.admin.has_delete_permission(_request(self.superuser), self.baker))
        self.assertFalse(self.admin.has_delete_permission(_request(self.normal), self.baker))


class BakerQuerysetTest(TestCase):
    def test_superuser_sees_only_bakers_with_fewer_than_five_cakes(self):
        superuser = make_user("superq", is_superuser=True)
        low = make_baker("low")
        full = make_baker("full")
        for index in range(4):
            make_cake(low, name=f"Low {index}")
        for index in range(5):
            make_cake(full, name=f"Full {index}")
        ids = set(_admin_for(Baker).get_queryset(_request(superuser)).values_list("id", flat=True))
        self.assertIn(low.id, ids)
        self.assertNotIn(full.id, ids)


class CakePermissionTest(TestCase):
    def setUp(self):
        self.admin = _admin_for(Cake)
        self.owner = make_baker("owner")
        self.other = make_baker("other")
        self.superuser = make_user("supercake", is_superuser=True)
        self.cake = make_cake(self.owner)

    def test_owner_and_superuser_can_change_cake(self):
        self.assertTrue(self.admin.has_change_permission(_request(self.owner.user), self.cake))
        self.assertTrue(self.admin.has_change_permission(_request(self.superuser), self.cake))

    def test_other_baker_cannot_change_cake(self):
        self.assertFalse(self.admin.has_change_permission(_request(self.other.user), self.cake))

    def test_other_baker_cannot_delete_cake(self):
        self.assertFalse(self.admin.has_delete_permission(_request(self.other.user), self.cake))

    def test_other_baker_can_see_cake(self):
        ids = set(self.admin.get_queryset(_request(self.other.user)).values_list("id", flat=True))
        self.assertIn(self.cake.id, ids)

    def test_save_model_assigns_current_baker_on_create(self):
        cake = Cake(name="New", price=10, weight=1, description="x")
        self.admin.save_model(_request(self.owner.user), cake, form=None, change=False)
        cake.refresh_from_db()
        self.assertEqual(cake.baker, self.owner)

    def test_baker_cannot_add_more_than_ten_cakes(self):
        for index in range(10):
            make_cake(self.owner, name=f"Cake {index}")
        permission_denied = not self.admin.has_add_permission(_request(self.owner.user))
        form = self.admin.get_form(_request(self.owner.user))(
            data={
                "name": "Eleventh Cake",
                "price": 1,
                "weight": 1,
                "description": "x",
            }
        )
        if permission_denied or not form.is_valid():
            return
        cake = form.save(commit=False)
        rejected = False
        try:
            self.admin.save_model(_request(self.owner.user), cake, form=form, change=False)
        except Exception:
            rejected = True
        self.assertTrue(rejected, "the admin allowed a baker with 10 cakes to add another")

    def test_baker_cannot_exceed_total_price_10000(self):
        make_cake(self.owner, name="Expensive", price=9900)
        form = self.admin.get_form(_request(self.owner.user))(
            data={
                "name": "Too Much",
                "price": 101,
                "weight": 1,
                "description": "x",
            }
        )
        if form.is_valid():
            cake = form.save(commit=False)
            rejected = False
            try:
                self.admin.save_model(_request(self.owner.user), cake, form=form, change=False)
            except Exception:
                rejected = True
            self.assertTrue(rejected, "cake pushing the baker total above 10,000 was accepted")

    def test_duplicate_cake_name_is_rejected(self):
        make_cake(self.owner, name="Unique Name")
        form = self.admin.get_form(_request(self.owner.user))(
            data={
                "name": "Unique Name",
                "price": 20,
                "weight": 1,
                "description": "duplicate",
            }
        )
        if form.is_valid():
            duplicate = form.save(commit=False)
            rejected = False
            try:
                self.admin.save_model(_request(self.owner.user), duplicate, form=form, change=False)
            except Exception:
                rejected = True
            self.assertTrue(rejected, "a second cake with the same name was accepted")
