from django.urls import reverse

from .base import RealEstateTestCase as TestCase
from .factories import assign_feature, make_feature, make_property


class IndexViewTest(TestCase):
    def test_index_returns_200(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_index_displays_only_unsold_properties_larger_than_100_square_meters(self):
        visible = make_property(name="Visible House", area=150, sold=False)
        small = make_property(name="Small Flat", area=70, sold=False)
        sold = make_property(name="Sold Villa", area=180, sold=True)

        response = self.client.get(reverse("index"))

        self.assertContains(response, visible.name)
        self.assertNotContains(response, small.name)
        self.assertNotContains(response, sold.name)

    def test_index_displays_feature_based_price(self):
        prop = make_property(name="Priced House", area=160, sold=False)
        assign_feature(prop, make_feature("Elevator", 10000))
        assign_feature(prop, make_feature("Pool", 25000))

        response = self.client.get(reverse("index"))

        self.assertContains(response, "Priced House")
        self.assertContains(response, "35000")


class EditViewTest(TestCase):
    def test_edit_page_returns_200_for_existing_property(self):
        prop = make_property()
        response = self.client.get(reverse("edit.html", kwargs={"id": prop.id}))
        self.assertEqual(response.status_code, 200)

    def test_edit_page_displays_comma_separated_features_and_price(self):
        prop = make_property(name="Feature House")
        assign_feature(prop, make_feature("Garage", 15000))
        assign_feature(prop, make_feature("Garden", 8000))

        response = self.client.get(reverse("edit.html", kwargs={"id": prop.id}))

        self.assertContains(response, "Garage")
        self.assertContains(response, "Garden")
        self.assertContains(response, ",")
        self.assertContains(response, "23000")

    def test_post_updates_property_information(self):
        prop = make_property(name="Old Name", area=130, sold=False)
        response = self.client.post(
            reverse("edit.html", kwargs={"id": prop.id}),
            {
                "name": "Updated Name",
                "description": "Updated location",
                "area": 155,
                "date": prop.date,
                "reserved": "on",
                "sold": "",
                "feature": prop.feature or "",
            },
        )
        self.assertIn(response.status_code, (200, 302))
        prop.refresh_from_db()
        self.assertEqual(prop.name, "Updated Name")
        self.assertEqual(prop.area, 155)
