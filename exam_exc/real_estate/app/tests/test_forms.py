from django import forms

from .base import RealEstateTestCase as TestCase


class EditFormTest(TestCase):
    def _form_class(self):
        from app.forms import EditForm
        return EditForm

    def test_form_is_model_form(self):
        self.assertTrue(issubclass(self._form_class(), forms.ModelForm))

    def test_form_exposes_property_fields_but_not_agent_or_feature_relations(self):
        form = self._form_class()()
        self.assertIn("name", form.fields)
        self.assertIn("description", form.fields)
        self.assertIn("area", form.fields)
        self.assertIn("image", form.fields)
        self.assertIn("reserved", form.fields)
        self.assertIn("sold", form.fields)
        self.assertNotIn("propertyagent", form.fields)
        self.assertNotIn("propertyfeature", form.fields)

    def test_feature_summary_is_not_user_editable(self):
        form = self._form_class()()
        if "feature" in form.fields:
            self.assertTrue(
                form.fields["feature"].disabled or form.fields["feature"].widget.attrs.get("readonly"),
                "feature names may be displayed, but the public edit.html form must not edit.html feature assignments",
            )

    def test_non_checkbox_widgets_have_bootstrap_class(self):
        form = self._form_class()()
        for field in form.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                self.assertIn("form-control", field.widget.attrs.get("class", ""))
