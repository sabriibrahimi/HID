from django import forms
from .models import *


class EditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)

        if 'feature' in self.fields:
            self.fields['feature'].disabled = True

        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model=Property
        fields = '__all__'

