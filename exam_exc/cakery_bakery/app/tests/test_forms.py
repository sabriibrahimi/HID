from app.forms import CakeForm

from .base import CakeryTestCase as TestCase


class CakeFormTest(TestCase):
    def test_form_excludes_baker(self):
        self.assertNotIn("baker", CakeForm().fields)

    def test_form_contains_all_editable_cake_fields(self):
        fields = CakeForm().fields
        for name in ("name", "price", "weight", "description", "picture"):
            self.assertIn(name, fields)

    def test_widgets_have_bootstrap_form_control_class(self):
        for name, field in CakeForm().fields.items():
            self.assertIn(
                "form-control",
                field.widget.attrs.get("class", ""),
                f"field {name!r} is missing the Bootstrap form-control class",
            )
